#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint
import logging
import numpy as np


log = logging.getLogger(__name__)

def GetAllHists(theDIR) -> dict:
    hists = {}
    for theOBJ in theDIR.GetListOfKeys():
        obj = theOBJ.ReadObj()
        if obj.IsA().InheritsFrom("TH1"):
            hists[obj.GetName()] = obj
    return hists


def __create_toy(hist, histNOWGT): # Treat every bin as a compound poisson distribution
    newhist = hist.Clone(hist.GetName()+"_toy")

    for binidx in range(hist.GetNbinsX()):
        binIdx = binidx+1
        bin_content = hist.GetBinContent(binIdx)
        bin_error   = hist.GetBinError  (binIdx)
        if bin_content < 1e-8:
            newhist.SetBinContent(binIdx, 0)
            newhist.SetBinError  (binIdx, 0)
            continue

        mu = bin_content
        #N_event = int( ( bin_content / bin_error )**2 )
        N_events = ( bin_content / bin_error )**2

        mean_weight = mu / float(N_events)   # mean weight
        s2 = mu * mean_weight                # approximate variance ~ mu * mean weight
        lam_tilde = mu**2 / s2               # SPD poisson parameter
        scale = s2 / mu                      # SPD scale factor

        toy_data = np.random.poisson(lam_tilde, 1) * scale # generate toy data

        newhist.SetBinContent(binIdx, toy_data[0])
        newhist.SetBinError  (binIdx, s2**0.5)
    return newhist
def _create_psuedodata(oHISTname:str, norm:float, hist, histNOWGT):
    hToy = __create_toy(hist, histNOWGT)
    hToy.SetName(oHISTname)
    hToy.Scale(norm / hToy.Integral())
    return hToy

def ModifyPsuedoData(histDICT:dict) -> dict:
    loaded_hists = [ 'truthF',
        'truthL', 'Ljet', 'LjetNoWeight',
        'truthC', 'Cjet', 'CjetNoWeight',
        'truthB', 'Bjet', 'BjetNoWeight',
    ]
    has_key = [ 1 for k in loaded_hists if k not in histDICT ]
    if sum(has_key) != 0:
        log.warning(f'[UseOriginalHist] ModifyPsuedoData() requires all histograms in {loaded_hists}. So use original histogram')
        return histDICT

    # create psuedodata with the same integration accroding to Compound Poisson Distributions
    #truthL = _create_psuedodata('truthL', histDICT['truthL'].Integral(), histDICT['Ljet'], histDICT['LjetNoWeight'])
    #truthC = _create_psuedodata('truthC', histDICT['truthC'].Integral(), histDICT['Cjet'], histDICT['CjetNoWeight'])
    #truthB = _create_psuedodata('truthB', histDICT['truthB'].Integral(), histDICT['Bjet'], histDICT['BjetNoWeight'])
    truthL = _create_psuedodata('truthL', histDICT['truthL'].Integral(), histDICT['truthL'], histDICT['truthLNoWeight'])
    truthC = _create_psuedodata('truthC', histDICT['truthC'].Integral(), histDICT['truthC'], histDICT['truthCNoWeight'])
    truthB = _create_psuedodata('truthB', histDICT['truthB'].Integral(), histDICT['truthB'], histDICT['truthBNoWeight'])

    # create psuedo data from each components
    data_obs = histDICT['truthF'].Clone('data_obs')
    data_obs.Add(truthL)
    data_obs.Add(truthC)
    data_obs.Add(truthB)

    # update truth and psuedosample
    histDICT['truthL'] = truthL
    histDICT['truthC'] = truthC
    histDICT['truthB'] = truthB
    histDICT['data_obs'] = data_obs
    log.info(f'[PsuedoDataCreated] data / truth hists updated according to Compound Poisson Distributions')
    return histDICT










if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
    inROOT = sys.argv[1]
    outROOT = sys.argv[2]

    
    infile = ROOT.TFile.Open(inROOT)
    outfile = ROOT.TFile(outROOT, 'recreate')

    for inDIR in infile.GetListOfKeys():
        indir = inDIR.ReadObj()
        if indir.IsA().InheritsFrom("TDirectory"):
            log.info(f'[LoadDir] {indir.GetName()}')
            hist_dict = GetAllHists(indir)
            log.debug(f'[LoadedTH1] {hist_dict}')
            updated_psuedosample = ModifyPsuedoData(hist_dict)

            odir = outfile.mkdir(indir.GetName())
            odir.cd()
            for hname, new_hist in updated_psuedosample.items():
                new_hist.Write()
            odir.Write()
    outfile.Close()
    infile.Close()
    log.info(f'[FileExport] make_hist_source_and_datacard.toyData.py generates {outROOT}')
            

    

    

    

