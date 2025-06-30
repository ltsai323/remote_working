#!/usr/bin/env python

import sys,os
from math import sqrt
import ROOT as rt
import libPython.CMS_lumi, libPython.tdrstyle

LOG_Y_SCALE = False

#libPython.tdrstyle.setTDRStyle()

debug_mode = True
def BUG(mesg):
    if debug_mode:
        print(f'[BUG] {mesg}')


def show_bins(h):
    print(f'hist {h.GetName()} has # bins {h.GetNbinsX()} with edge {h.GetBinLowEdge(1)} and {h.GetBinLowEdge(h.GetNbinsX()+2)}')

infile = 'dataMCcomp.root'
#variables = [ 'phoPt', 'phoEta', 'phoPhi', 'chiso', 'nVtx', 'jetPt' ]
variables = [ 'phoEta' ]

tfile = rt.TFile.Open(infile)

def ratioPlotConfigs(hist):
    hist.GetYaxis().SetRangeUser(0.5,1.5)
    hist.SetStats(False)
def get_stacked_hist(hSTACKPLOT:rt.THStack) -> rt.TH1:
    if not isinstance(hSTACKPLOT,rt.THStack):
        raise IOError(f'get_stacked_hist() requires a THStack object, input variable has type "{type(hSTACKPLOT)}"')
    stacked_hists = hSTACKPLOT.GetHists()
    h = None
    for hist in stacked_hists:
        if not h:
            h = hist
        else:
            h.Add(hist)
    if h == None:
        raise IOError(f'get_stacked_hist() No any hist in stackplot. Abort...')
    h.SetDirectory(0)
    return h



def takeRatio(hNUMERATOR:rt.TH1, hDENOMIATOR:rt.TH1, configFUNC ) -> rt.TH1:
    ratio_hist = hNUMERATOR.Clone()
    ratio_hist.SetName('ratio')
    ratio_hist.Divide(hDENOMIATOR)

    configFUNC(ratio_hist)
    return ratio_hist




def find_k_factor(tFILE, folderPOSFIX):
    nDATA = tFILE.Get(f'expdata/phoEta').Integral()
    nSIGN = tFILE.Get(f'sign{folderPOSFIX}/phoEta').Integral()
    nFAKE = tFILE.Get(f'fake{folderPOSFIX}/phoEta').Integral()
    k_factor = (nDATA-nSIGN) / nFAKE
    BUG(f'k factor is {k_factor:.3f}')
    return k_factor
for folder_postfix in ( 'ALL', '0', '1','2','3' ):
    k_factor = find_k_factor(tfile, folder_postfix)
    for var in variables:
        c = rt.TCanvas( 'canv', 'hi', 800, 1000)
        libPython.CMS_lumi.lumi_13TeV = "36.33 fb^{-1}"
        libPython.CMS_lumi.CMS_lumi(c, 4, 10)
        c.SetTopMargin(0.10)
        c.SetBottomMargin(0.30)
        c.SetLeftMargin(0.12)
        legend = rt.TLegend(0.15,0.80,0.95,0.90)
        legend.SetFillColor(4000)
        legend.SetFillStyle(4000)
        legend.SetBorderSize(0)
        legend.SetNColumns(3)

        datahist = tfile.Get(f'expdata/{var}')
        datahist.SetMarkerSize(1)
        datahist.SetMarkerStyle(34)
        datahist.SetLineWidth(2)
        datahist.SetLineColor(1)

        signhist = tfile.Get(f'sign{folder_postfix}/{var}')
        signhist.Sumw2()
        signhist.SetFillColor(46)
        signhist.SetLineColor(0)

        fakehist = tfile.Get(f'fake{folder_postfix}/{var}')
        fakehist.Sumw2()
        fakehist.SetFillColor(14)
        fakehist.SetLineColor(0)

        sumhist = signhist.Clone()
        sumhist.Add(fakehist)
        chi2_ndf = datahist.Chi2Test(sumhist, "UW OF P CHI2/NDF")
        chi2_per_ndof = f'{chi2_ndf:.1f}'.replace('.', 'p')
        if LOG_Y_SCALE:
            c.SetLogy()
            maxY = datahist.GetMaximum() * 1e2
            minY = datahist.GetMinimum()
        else:
            maxY = datahist.GetMaximum() * 1.4
            minY = datahist.GetMinimum()

        #datahist.GetYaxis.SetRangeUser(minY,maxY)
        #signhist.GetYaxis.SetRangeUser(minY,maxY)
        #fakehist.GetYaxis.SetRangeUser(minY,maxY)




        fakehist.Scale(k_factor)

        stackplot = rt.THStack('hs', f'\chi^{2}/DoF = {chi2_ndf:.1f}')
        stackplot.Add(fakehist)
        stackplot.Add(signhist)
        stackplot.SetMaximum(maxY)
        stackplot.Draw()



        if debug_mode:
            stacked_hist = get_stacked_hist(stackplot)
            h = takeRatio(datahist, stacked_hist, ratioPlotConfigs)
            stacked_hists = stackplot.GetHists()

            h.Draw("EP")


        else:
            ratioplot = rt.TRatioPlot(stackplot, datahist)
            ratioplot.Draw()

            ratioplot.GetLowYaxis().SetNdivisions(505)
            ratioplot.GetLowerRefYaxis().SetRangeUser(0.5,1.5)

            ratioplot.GetXaxis().SetTitle('aasdfasdlf')
            ratioplot.GetLowerRefXaxis().SetTitle('aasdfasdlf')

        legend.AddEntry(datahist, 'data', 'p')
        legend.AddEntry(signhist, 'signal', 'f')
        legend.AddEntry(fakehist, 'QCD', 'f')

        legend.SetHeader(f'k-factor {k_factor:.3f}')
        legend.Draw()


        c.Print(f'checkplot{folder_postfix}_{var}.pdf')

        if debug_mode:
            c.SaveAs("hi.png")
            exit()
        del c




