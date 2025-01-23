#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint

def info(mesg):
    print(f'i@ {mesg}')


class ObjMap:
    def __init__(self, iNAME, oDIR, oNAME, normFACTOR):
        self.iname = iNAME
        self.odir = oDIR
        self.oname = oNAME
        self.norm = normFACTOR
        self.h = None
    def normalize_hist(self, iFILE):
        if isinstance(self.norm, str):
            try:
                norm_source = iFILE.Get(self.norm)
                self.h.Scale(1./norm_source.Integral())
                return
            except AttributeError as e:
                raise AttributeError(f'[Unable to Calculate Normalization] Got a string norm factor, but histogram name "{ self.norm }" does not in input TFile.') from e
        if self.norm < 0: return
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
    sum_entries = get_entries(iFile,output_hist_definitions[0])

    dcard_template = datacardTEMPLATE
    info(f'[ReadTemplate] tempelate "{ dcard_template }" is required for create output datacard')
    with open(dcard_template, 'r') as fIN:
        fill_datacard = fIN.read().format( iFILE = outputROOT, nDATA = sum_entries )
        info(f'[Output Files] datacard "{dcard_out}"')
        fout = open(dcard_out, 'w')
        fout.write(fill_datacard)
        fout.close()
        info(f'[Output Files] datacard "{dcard_out}" exported.')

    root_out = ROOT.TFile(outputROOT, 'recreate')
    info(f'[Output Files] Root file "{root_out.GetName()}"')
    root_out_folders = {}

    global RECORDED_INTEGRATION_INFO
    RECORDED_INTEGRATION_INFO = {}
    for output_hist_definition in output_hist_definitions:
        dirname = output_hist_definition.odir
        if dirname not in root_out_folders:
            root_out_folders[dirname] = root_out.mkdir(dirname)

        out_dir = root_out_folders.get(dirname)
        output_hist_definition.get_output_hist(iFile)
        output_hist_definition.write_hist_to(out_dir)
        RECORDED_INTEGRATION_INFO[output_hist_definition.oname] = output_hist_definition.entries

        

    info(f'[Output Files] Root file "{root_out.GetName()}" generated')
    root_out.Close()
    iFile.Close()

def export_composition(oFILEname:str):
    if len(RECORDED_INTEGRATION_INFO) == 0: raise IOError(f'[NothingInside] Nothing recorded in the integration information.')

    if 'cjet' in RECORDED_INTEGRATION_INFO.keys() and 'bjet' in RECORDED_INTEGRATION_INFO.keys():
        return export_composition_LCBjets(oFILEname)
    else:
        return export_composition_inclusive_photon(oFILEname)

def export_composition_inclusive_photon(oFILEname:str):
    if len(RECORDED_INTEGRATION_INFO) == 0: raise IOError(f'[NothingInside] Nothing recorded in the integration information.')



    composition_fake = 0.2
    composition_sign = 1.-composition_fake
    composition_l = 0.
    composition_c = 0.
    composition_b = 0.
    
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
            'nFAKE': { 'composition': composition_sign, 'value': nsign },
            'nDATA': { 'value': ndata },
    }
    with open(oFILEname, "w") as f_out:
        yaml.dump(v, f_out, default_flow_style=False)
    info(f'[Output Files] yaml file "{ oFILEname }" generated for inclusive photon')

def export_composition_LCBjets(oFILEname:str):
    tot = RECORDED_INTEGRATION_INFO['cjet'] + RECORDED_INTEGRATION_INFO['bjet'] + RECORDED_INTEGRATION_INFO['ljet']

    v = {
            'nL': { 'composition': RECORDED_INTEGRATION_INFO['ljet'] / tot },
            'nC': { 'composition': RECORDED_INTEGRATION_INFO['cjet'] / tot },
            'nB': { 'composition': RECORDED_INTEGRATION_INFO['bjet'] / tot },
    }

    composition_fake = 0.2
    composition_sign = 1.-composition_fake
    composition_l = 0.
    composition_c = 0.
    composition_b = 0.

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
    with open(oFILEname, "w") as f_out:
        yaml.dump(v, f_out, default_flow_style=False)
    info(f'[Output Files] yaml file "{ oFILEname }" generated for LCB jets')

def convert_input_dict(config:dict):
    from pprint import pprint
    pprint(config)
    config['load_data'] = [
        ObjMap(ldata['histSOURCE'], config['channel'],ldata['name'], ldata['normalize'])
        for ldata in config['load_data'] ]


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
if __name__ == "__main__":
    if len(sys.argv) > 1:
        inARGs = namedtuple('inARGs', 'inYAML')
        arg = inARGs(*sys.argv[1:])
        with open(arg.inYAML, 'r') as fIN:
            config = yaml.safe_load(fIN)
    else:
        config= test_dict()
        info(f'[TestMode] No argument filled, use default input data')

    convert_input_dict(config)



    inputFILE = config['inputFILE']
    datacardTEMPLATE = config['datacardTEMPLATE']
    outputDATACARD = config['outputDATACARD']
    outputROOT = config['outputROOT']
    outputYAML = config['outputYAML']
    output_hist_definitions = config['load_data']

    maked_datacard_and_hists(inputFILE,
            datacardTEMPLATE, outputDATACARD, outputROOT,
            output_hist_definitions)
    export_composition(outputYAML)
