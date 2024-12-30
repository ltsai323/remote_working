#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint

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

        self.normalize_hist(iFILE)
    def write_hist_to(self, fOUT):
        fOUT.cd()
        self.h.Write()


def get_entries(tFILE:ROOT.TFile,objMAP:ObjMap):
    print(objMAP.iname)
    h = tFILE.Get(objMAP.iname)
    return h.Integral()


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
    print(f'[ReadTemplate] tempelate "{ dcard_template }" is required for create output datacard')
    with open(dcard_template, 'r') as fIN:
        fill_datacard = fIN.read().format( iFILE = outputROOT, nDATA = sum_entries )
        print(f'[Output Files] datacard "{dcard_out}" is generating.')
        fout = open(dcard_out, 'w')
        fout.write(fill_datacard)
        fout.close()
        print(f'[Output Files] datacard "{dcard_out}" exported.')

    root_out = ROOT.TFile(outputROOT, 'recreate')
    print(f'[Output Files] Root file "{root_out.GetName()}" is generating.')
    root_out_folders = {}
    for output_hist_definition in output_hist_definitions:
        dirname = output_hist_definition.odir
        if dirname not in root_out_folders:
            root_out_folders[dirname] = root_out.mkdir(dirname)

        out_dir = root_out_folders.get(dirname)
        output_hist_definition.get_output_hist(iFile)
        output_hist_definition.write_hist_to(out_dir)

    print(f'[Output Files] Root file "{root_out.GetName()}" exported.')
    root_out.Close()
    iFile.Close()


def test_dict(argv=None):
    yaml_content = '''
inputFILE: out_makehisto.root
channel: SBbtag
datacardTEMPLATE: data/datacard_SBbtag_template.txt
outputDATACARD: datacard_SBbtag.txt
outputROOT:     datacard_SBbtag.root
load_data:
    - name: data_obs
      histSOURCE: jettag0_data_dataSideband
      normalize: -1
    - name: ljet
      histSOURCE: jettag0_gjet_signalRegion
      normalize:  1
    - name: cjet
      histSOURCE: jettag0_gjet_signalRegion
      normalize: 1
    - name: bjet
      histSOURCE: jettag0_gjet_signalRegion
      normalize: 1
    - name: bjet_shapeUp
      histSOURCE: jettag0_gjet_signalRegion
      normalize: jettag0_gjet_signalRegion
    - name: bjet_shapeDown
      histSOURCE: jettag0_gjet_signalRegion
      normalize: jettag0_gjet_signalRegion
    '''
    return yaml.safe_load(yaml_content)
def convert_input_dict(config:dict):
    config['load_data'] = [
        ObjMap(ldata['histSOURCE'], config['channel'],ldata['name'], ldata['normalize'])
        for ldata in config['load_data'] ]


if __name__ == "__main__":
    #config= test_dict()

    with open(sys.argv[1], 'r') as fIN:
        config = yaml.safe_load(fIN)

    convert_input_dict(config)
    pprint(config)
    inputs = config


    inputFILE = inputs['inputFILE']
    datacardTEMPLATE = inputs['datacardTEMPLATE']
    outputDATACARD = inputs['outputDATACARD']
    outputROOT = inputs['outputROOT']
    output_hist_definitions = inputs['load_data']

    maked_datacard_and_hists(inputFILE,
            datacardTEMPLATE, outputDATACARD, outputROOT,
            output_hist_definitions)
