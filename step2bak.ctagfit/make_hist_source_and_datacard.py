#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint
import logging

log = logging.getLogger(__name__)

def info(mesg):
    print(f'i@ {mesg}')


class ObjMap:
    def __init__(self, iNAME, oDIR, oNAME, normFACTOR):
        self.iname = iNAME
        self.odir = oDIR
        self.oname = oNAME
        self.norm = normFACTOR
        self.h = None
    def __repr__(self): return self.__str__()
    def __str__(self):
        return f'ObjMap(rootname=self.iname, norm_required="{self.norm}", hcombine_output_channel="{self.odir}" hcombine_obj_name="{self.oname}")'


    def normalize_hist(self, iFILE):
        if isinstance(self.norm, str):
            try:
                norm_source = iFILE.Get(self.norm)
                self.h.Scale(1./norm_source.Integral())
                return
            except AttributeError as e:
                raise AttributeError(f'[Unable to Calculate Normalization] Got a string norm factor, but histogram name "{ self.norm }" does not in input TFile.') from e
        if self.norm < 0: return
        if self.h.Integral() > 0.: ## prevent empty histogram
            self.h.Scale(1./self.h.Integral())

    def get_output_hist(self, iFILE):
        self.h = iFILE.Get(self.iname)
        self.h.SetName(self.oname)
        self.entries = self.h.Integral()

        self.normalize_hist(iFILE)
    def write_hist_to(self, fOUT):
        fOUT.cd()
        self.h.Write()


def get_entries(tFILE:ROOT.TFile,objMAP:ObjMap):
    h = tFILE.Get(objMAP.iname)
    return h.Integral()


RECORDED_INTEGRATION_INFO = {}
def maked_datacard_and_hists( inFILE:str,
        datacardTEMPLATE:str, outputDATACARD:str, outputROOT:str,
        fitCHANNEL:str,
        histDEFs:list):
    '''

    Parameters:
        inputFILE(str): Input TFile contains all needed histograms
        channel(str): Channel name used as bin name in datacard. Also create a directory in output root file
        histDEFs(list): Use LoadSOMETHING() function takes input hist name from inputFILE and renamed to output root file. The first entry should be data (Required).
    Returns:
        No return but this function exports the output datacard and output root file.
    '''

    iFile = ROOT.TFile.Open(inFILE)
    dcard_out = outputDATACARD
    output_hist_definitions = histDEFs

    dcard_template = datacardTEMPLATE
    log.info(f'[ReadTemplate] tempelate "{ dcard_template }" is required for create output datacard')

    channel = fitCHANNEL # used for locals()
    iFILE=outputROOT # used for locals()

    for hNAME, hist_def in output_hist_definitions.items():
        locals()[hNAME] = iFile.Get(hist_def.iname)


    with open(dcard_template, 'r') as fIN:

        fill_datacard = eval(f'f"""{fIN.read()}"""') ## evaluate f-string here
        log.info(f'[Output Files] datacard "{dcard_out}"')
        fout = open(dcard_out, 'w')
        fout.write(fill_datacard)
        fout.close()
        log.info(f'[Output Files] datacard "{dcard_out}" exported.')

    root_out = ROOT.TFile(outputROOT, 'recreate')
    log.info(f'[Output Files] Root file "{root_out.GetName()}"')
    root_out_folders = {}

    global RECORDED_INTEGRATION_INFO
    RECORDED_INTEGRATION_INFO = {}
    log.debug(f'[LoadVars] output_hist_definitions:')
    for hist_name, output_hist_definition in output_hist_definitions.items():
        log.debug(f'[LoadVars] -> hist "{hist_name}" and definition {output_hist_definition}')
        dirname = output_hist_definition.odir
        if dirname not in root_out_folders: ## use "higgs combine channel" as output folder name. If folder does not created, create one
            root_out_folders[dirname] = root_out.mkdir(dirname)

        out_dir = root_out_folders.get(dirname)
        output_hist_definition.get_output_hist(iFile)
        output_hist_definition.write_hist_to(out_dir)
        RECORDED_INTEGRATION_INFO[output_hist_definition.oname] = output_hist_definition.entries
        log.debug(f'[LoadVars] -> hist with integration {output_hist_definition.entries}')



    log.info(f'[Output Files] Root file "{root_out.GetName()}" generated')
    root_out.Close()
    iFile.Close()

def export_composition(oYAMLfile:str, oBASHfile:str):
    if len(RECORDED_INTEGRATION_INFO) == 0: raise IOError(f'[NothingInside] Nothing recorded in the integration information.')

    if 'cjet' in RECORDED_INTEGRATION_INFO.keys() and 'bjet' in RECORDED_INTEGRATION_INFO.keys():
        return export_composition_LCBjets(oYAMLfile, oBASHfile)
    else:
        return export_composition_inclusive_photon(oYAMLfile, oBASHfile)

def export_composition_inclusive_photon(oYAMLfile:str, oBASHfile:str):
    if len(RECORDED_INTEGRATION_INFO) == 0: raise IOError(f'[NothingInside] Nothing recorded in the integration information.')



    composition_fake = 0.2
    composition_sign = 1.-composition_fake
    composition_l = 0.7
    composition_c = 0.2
    composition_b = 0.1
    
    ndata = RECORDED_INTEGRATION_INFO['data_obs']
    nfake = ndata * composition_fake
    nsign = ndata * composition_sign
    nl = nsign * composition_l
    nc = nsign * composition_c
    nb = nsign * composition_b
    log.debug(f'[Content] RECORDED_INTEGRATION_INFO = "{RECORDED_INTEGRATION_INFO}"')
    empty_fake = int(abs(RECORDED_INTEGRATION_INFO['fake'])<1e-5) if 'fake' in RECORDED_INTEGRATION_INFO else 0



    v = {
            'nL': { 'composition': composition_l, 'value': nl },
            'nC': { 'composition': composition_c, 'value': nc },
            'nB': { 'composition': composition_b, 'value': nb },
            'nFAKE': { 'composition': composition_fake, 'value': nfake },
            'emptyFAKE': empty_fake,
            #'nFAKE': { 'composition': composition_sign, 'value': nsign },
            'nDATA': { 'value': ndata },
            'nSIGN': { 'value': nsign },
    }
    with open(oYAMLfile, "w") as f_out:
        yaml.dump(v, f_out, default_flow_style=False)
    with open(oBASHfile, 'w') as f_out:
        f_out.write(f'#!/usr/bin/env sh\nnL={nl:.2f}\nnC={nc:.2f}\nnB={nb:.2f}\nnDATA={ndata:.2f}\nnSIGN={nsign:.2f}\nnFAKE={nfake:.2f}\nemptyFAKE={empty_fake}')
    info(f'[Output Files] yaml file "{ oYAMLfile }" and "{ oBASHfile }" generated for inclusive photon')

def export_composition_LCBjets(oYAMLfile:str, oBASHfile:str):
    tot = RECORDED_INTEGRATION_INFO['cjet'] + RECORDED_INTEGRATION_INFO['bjet'] + RECORDED_INTEGRATION_INFO['ljet']

    v = {
            'nL': { 'composition': RECORDED_INTEGRATION_INFO['ljet'] / tot },
            'nC': { 'composition': RECORDED_INTEGRATION_INFO['cjet'] / tot },
            'nB': { 'composition': RECORDED_INTEGRATION_INFO['bjet'] / tot },
    }

    composition_fake = 0.2
    composition_sign = 1.-composition_fake
    composition_l = 0.7
    composition_c = 0.2
    composition_b = 0.1

    ndata = RECORDED_INTEGRATION_INFO['data_obs']
    nfake = ndata * composition_fake
    nsign = ndata * composition_sign
    nl = nsign * composition_l
    nc = nsign * composition_c
    nb = nsign * composition_b


    v = {
            'nL': { 'composition': composition_l, 'value': nl },
            'nC': { 'composition': composition_c, 'value': nc },
            'nB': { 'composition': composition_b, 'value': nb },
            'nFAKE': { 'composition': composition_fake, 'value': nfake },
            'nSIGN': { 'composition': composition_sign, 'value': nsign },
            'nDATA': { 'value': ndata },
    }
    with open(oYAMLfile, "w") as f_out:
        yaml.dump(v, f_out, default_flow_style=False)
    with open(oBASHfile, 'w') as f_out:
        f_out.write(f'#!/usr/bin/env sh\nnL={nl:.2f}\nnC={nc:.2f}\nnB={nb:.2f}\nnDATA={ndata:.2f}\nnSIGN={nsign:.2f}\nnFAKE={nfake:.2f}')
    info(f'[Output Files] yaml file "{ oYAMLfile }" and "{ oBASHfile }" generated for LCB jets')

def convert_input_dict(config:dict):
    from pprint import pprint
    pprint(config)
    #config['load_data'] = [
    #    ObjMap(ldata['histSOURCE'], config['channel'],ldata['name'], ldata['normalize'])
    #    for ldata in config['load_data'] ]
    config['load_data'] = {
            histNAME: ObjMap(ldata['histSOURCE'], config['channel'],ldata['name'], ldata['normalize'])
            for histNAME, ldata in config['load_data'].items() }


def test_dict():
    yaml_content = '''
channel: SBbtag
inputFILE: out_makehisto.root
datacardTEMPLATE: data/datacard_SBbtag_template.txt
outputDATACARD:   datacard_SBbtag.txt
outputROOT:       datacard_SBbtag.root
outputYAML:       datacard_SBbtag.defaultValue.yaml
load_data:
    - name: data_obs
      histSOURCE: jettag0_data_dataSideband
      normalize: -1
    - name: ljet
      histSOURCE: jettag0_gjetL_signalRegion
      normalize:  1
    - name: cjet
      histSOURCE: jettag0_gjetC_signalRegion
      normalize: 1
    - name: bjet
      histSOURCE: jettag0_gjetB_signalRegion
      normalize: 1
    - name: bjet_shapeUp
      histSOURCE: jettag0_gjetB_signalRegion
      normalize: jettag0_gjetB_signalRegion
    - name: bjet_shapeDown
      histSOURCE: jettag0_gjetB_signalRegion
      normalize: jettag0_gjetB_signalRegion
    '''
    return yaml.safe_load(yaml_content)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    if len(sys.argv) > 1:
        inARGs = namedtuple('inARGs', 'inYAML')
        arg = inARGs(*sys.argv[1:])
        with open(arg.inYAML, 'r') as fIN:
            config = yaml.safe_load(fIN)
    else:
        config= test_dict()
        debug(f'[TestMode] No argument filled, use default input data')

    convert_input_dict(config)



    inputFILE = config['inputFILE']
    datacardTEMPLATE = config['datacardTEMPLATE']
    fitCHANNEL = config['channel']
    outputDATACARD = config['outputDATACARD']
    outputROOT = config['outputROOT']
    outputYAML = config['outputYAML']
    output_hist_definitions = config['load_data']

    outputBASH = config['outputBASH']

    maked_datacard_and_hists(inputFILE,
            datacardTEMPLATE, outputDATACARD, outputROOT,
            fitCHANNEL,
            output_hist_definitions)
    export_composition(outputYAML, outputBASH)
