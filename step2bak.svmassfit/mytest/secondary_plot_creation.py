#!/usr/bin/env python3
import logging
import ROOT
from collections import namedtuple
import sys
import yaml


class histCollection:
    def __init__(self):
        pass
    def WriteAllHists(self, fOUT):
        fOUT.cd()
        for hname, hinst in vars(self).items():
            hinst.Write()
class NameSet:
    def __init__(self, tag):
        ''' tag = allgjets_BDTAll'''
        def set_attribute(self, n):
            setattr(self, n, f'{n}_{tag}')
        set_attribute(self, 'data')
        set_attribute(self, 'sigL')
        set_attribute(self, 'sigC')
        set_attribute(self, 'sigB')
        set_attribute(self, 'fake')
        set_attribute(self, 'side')

        set_attribute(self, 'sumCB')
        set_attribute(self, 'sumLCB')
        set_attribute(self, 'stak')
        set_attribute(self, 'diff')
        set_attribute(self, 'diffLCB')
def take_ratio_in_obj(obj, histNAMEset:NameSet):
    h_data = getattr(obj, 'data')
    h_sigL = getattr(obj, 'sigL')
    h_sigC = getattr(obj, 'sigC')
    h_sigB = getattr(obj, 'sigB')
    h_fake = getattr(obj, 'fake')

    h_sumCB = h_sigB.Clone()
    h_sumCB.Add(h_sigC)
    h_sumCB.SetName(histNAMEset.sumCB)

    h_sumLCB = h_sigB.Clone()
    h_sumLCB.Add(h_sigC)
    h_sumLCB.Add(h_sigL)
    h_sumLCB.SetName(histNAMEset.sumLCB)

    h_stak = h_sigB.Clone()
    h_stak.Add(h_sigC)
    h_stak.Add(h_sigL)
    h_stak.Add(h_fake)
    h_stak.SetName(histNAMEset.stak)

    diff = TakeRatio(histNAMEset.diff, h_data, h_stak)
    diffLCB = TakeRatio(histNAMEset.diffLCB, h_data, h_sumLCB)

    setattr(obj,histNAMEset.sumCB , h_sumCB)
    setattr(obj,histNAMEset.sumLCB, h_sumLCB)
    setattr(obj,histNAMEset.stak  , h_stak)
    setattr(obj,histNAMEset.diff  , diff)
    setattr(obj,histNAMEset.diffLCB  , diffLCB)

def TakeRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER
    hL = hLOWER
    for ibin in range(1,hL.GetNbinsX()+2):
        if hL.GetBinContent(ibin) == 0: hL.SetBinContent(ibin, 1e-8)
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio

log = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='[basicCONFIG] %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

    inARGs = namedtuple('inARGs', 'inYAML')
    arg = inARGs(*sys.argv[1:])
    with open(arg.inYAML, 'r') as fIN:
        config = yaml.safe_load(fIN)




    iFILE = config['inputFILE']
    tag='allgjets_BDTAll'
    n = NameSet('allgjets_BDTAll')

    ifile = ROOT.TFile.Open(iFILE)
    hists = histCollection()

    setattr(hists, 'data', getattr(n,'data'))
    loadhist = lambda histTYPE: setattr(hists, histTYPE, ifile.Get( getattr(n,histTYPE) ))
    loadhist('data')
    loadhist('sigL')
    loadhist('sigC')
    loadhist('sigB')
    loadhist('fake')
    take_ratio_in_obj(hists,n)

    ofile = ROOT.TFile('secondary_plot_creation.root', 'recreate')
    hists.WriteAllHists(ofile)
    ofile.Close()
    

