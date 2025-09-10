#!/usr/bin/env python3
import logging
import ROOT

# use title as legend label
def normalize_hist(hIN, normFACTOR):
    hIN.SetTitle(f'{hIN.GetName()}: {normFACTOR:.2f}')
    if normFACTOR > 0:
        hIN.Scale(1./normFACTOR)

log = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format='[basicCONFIG] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    import sys
    inHIST = sys.argv[1]
    outHIST = sys.argv[2]

    kinematic_vars = [
            'phopt', 'phoeta', 'phophi',
            'jetpt', 'jeteta', 'jetphi',
            ]
    hist_sources = [ 'data','gjet','sigL','sigC','sigB','side','fake' ]

    # histname example: kine_data_phophi
    histname = lambda k,h: f'kine_{h}_{k}'

    hists = []
    fIN = ROOT.TFile.Open(inHIST)
    for hsource in hist_sources:
        h0 = fIN.Get(histname('jetphi',hsource))
        norm_factor = h0.Integral()
        for kvar in kinematic_vars:
            hist = fIN.Get(histname(kvar,hsource))
            normalize_hist(hist,norm_factor)
            hists.append(hist)

    ofile = ROOT.TFile(outHIST,'RECREATE')
    ofile.cd()
    for hist in hists:
        hist.Write()
    ofile.Close()
    fIN.Close()


