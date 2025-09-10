#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint
import logging
import math

log = logging.getLogger(__name__)

def info(mesg):
    print(f'i@ {mesg}')

def flatten_TH2(hist2D, newHISTname):
    # Get the 2D histogram
    hist2d = hist2D
    histname = newHISTname

    # Create the 1D histogram with 100 bins
    nbinx = hist2d.GetNbinsX()
    nbiny = hist2d.GetNbinsY()
    if nbinx != nbiny: raise IOError(f'[InvalidBinning] 2Dhist {histname} got binX({nbinX}) and binY({binbY}). They should be the same')
    hist1d = ROOT.TH1D(newHISTname, "Flattened Histogram;X;Counts", nbinx*nbinx, 0, 1*nbinx)
    log.info(f'[FlattenTH2] hist {newHISTname} flattened from {hist2d.GetName()}')

    # Loop over bins of the 2D histogram and flatten them into the 1D histogram
    for x_bin in range(nbinx):
        for y_bin in range(nbinx):
            # Get the content of the current 2D bin
            binvalue = hist2d.GetBinContent(x_bin+1, y_bin+1)
            binerror = hist2d.GetBinError  (x_bin+1, y_bin+1)

            # Determine the corresponding bin in the TH1D histogram
            target_bin = x_bin * nbinx + y_bin
            # Fill the 1D histogram
            hist1d.SetBinContent(target_bin + 1, binvalue)
            hist1d.SetBinError  (target_bin + 1, binerror)
    return hist1d


def get_1d_bin_number(v):
    """
    Converts a 1D histogram bin count into the square-rooted X-dimension
    for a 2D histogram (TH2) assuming square binning.

    Since TH2 can be flattened into a 1D histogram with total bins N,
    this function checks if N is a perfect square and returns sqrt(N)
    if valid. Otherwise returns -1.

    :param v: The total number of bins in the 1D histogram.
    :type v: int
    :return: -1 if `v` is not a perfect square, otherwise sqrt(`v`) as int.
    :rtype: int

    :Examples:

        >>> get_1d_bin_number(36)
        6
        >>> get_1d_bin_number(30)
        -1
    """
    sqr_val = math.isqrt(v)
    if sqr_val*sqr_val == v: return -1 # not a squared value, return invalid value
    return sqr_val


def restore_histogram(hist1D, out2DHISTname):
    # Get the 1D histogram
    hist1d = hist1D
    nbins = hist1d.GetNbinsX()
    binx = get_1d_bin_number(nbins)
    if binx < 0: raise ValueError(f'[InvalidBinning] TH1 {hist1D.GetName()} got binX({nbins}) but this is not a perfect square number.')

    # Create a new 2D histogram with the same binning as the original
    hist2d = ROOT.TH2D(out2DHISTname, "Restored 2D Histogram;X;Y", binx, 0, 10, binx, 0, 10)

    # Loop over the bins of the 1D histogram and unpack them back into the 2D histogram
    for x_bin in range(binx):
        for y_bin in range(binx):
            # Calculate the target bin index in the 1D histogram
            target_bin = x_bin * binx + y_bin
            # Get the content from the 1D histogram
            binvalue = hist1d.GetBinContent(target_bin + 1)
            binerror = hist1d.GetBinContent(target_bin + 1)
            # Fill the corresponding bin in the TH2D histogram
            hist2d.SetBinContent(x_bin + 1, y_bin + 1, binvalue)
            hist2d.SetBinError  (x_bin + 1, y_bin + 1, binerror)

    return hist2d


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
        if self.h.IsA().InheritsFrom("TH2"):
            self.h = flatten_TH2(self.h, self.oname) # if a TH2 got, flatten them to 1D
        else:
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
        try:
            locals()[hNAME].GetName()
        except ReferenceError as e:
            raise ReferenceError(f'\n[LoadHist] {hist_def.iname} loaded but got error') from e
            


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
