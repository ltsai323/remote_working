#!/usr/bin/env python3

import ROOT


if __name__ == "__main__":
    #fIN = ROOT.TFile.Open("ggtree_data_1.root")
    #tIN = fIN.Get('ggNtuplizer/EventTree')

    tIN = ROOT.TChain('ggNtuplizer/EventTree')
    tIN.Add('/home/ltsai/cms3/CRAB_FILES/UL16PostVFP_data/SinglePhoton/crab_UL16PostVFP_NCHCData__SinglePhoton__Run2016G-UL2016_MiniAODv2-v3/230217_084830/0000/ggtree_data_1*.root')


    canv = ROOT.TCanvas("c1",'', 800,600)
    #canv.SetLogy()

    base_cut = '&&'.join([
                #'nGoodVtx>0',
                #'isPVGood',
                'nPho>0',
                'metFilters!=0',#'pfMET/phoCalibEt[0] < 3'
                ])
    barrelPho = 'fabs(phoSCEta[0])<1.4442'
    endcapPho = 'fabs(phoSCEta[0])>1.566 && fabs(phoSCEta[0])<2.5'
    MET_source = 'pfMET'
    '''
    tIN.Draw( f'{MET_source}/phoCalibEt[0] >> h_barrel(100, 0., 2.)', base_cut + '&&' + barrelPho)
    tIN.Draw( f'{MET_source}/phoCalibEt[0] >> h_endcap(100, 0., 2.)', base_cut + '&&' + endcapPho)


    leg = ROOT.TLegend(0.3,0.65,0.85,0.85)
    leg.SetBorderSize(0)
    leg.SetFillColor(4000)
    leg.SetFillStyle(4000)

    hbarrel = ROOT.gROOT.FindObject('h_barrel')
    hbarrel.Scale(1./hbarrel.GetMaximum())
    hbarrel.SetLineColor(1)
    hbarrel.SetMarkerColor(1)
    hbarrel.SetMarkerStyle(23)
    hbarrel.SetStats(False)
    hbarrel.GetXaxis().SetTitle('MET / p_{T}^{#gamma}')
    hbarrel.GetYaxis().SetTitle('Normalized Entries')
    hbarrel.SetTitle(f'Cut: {base_cut}')
    leg.AddEntry(hbarrel, 'Normalized barrel photon region', 'lp')

    hendcap = ROOT.gROOT.FindObject('h_endcap')
    hendcap.Scale(1./hendcap.GetMaximum())
    hendcap.SetLineColor(2)
    hendcap.SetMarkerColor(2)
    hendcap.SetMarkerStyle(23)
    hendcap.SetStats(False)
    hendcap.GetXaxis().SetTitle('MET / p_{T}^{#gamma}')
    hendcap.GetYaxis().SetTitle('Normalized Entries')
    hendcap.SetTitle(f'Cut: {base_cut}')
    leg.AddEntry(hendcap, 'Normalized endcap photon region', 'lp')


    hbarrel.Draw("EP")
    hendcap.Draw("EP SAME")

    leg.Draw()

    #canv.SaveAs(f"METCut_{MET_source}ToverPhoCalibEt.pdf")
    canv.SaveAs("hi.png")
    '''


    tIN.Draw( f'{MET_source}/phoCalibEt[0]:phoPhi[0]', base_cut + '&&' + barrelPho + '&&' + f'{MET_source}/phoCalibEt[0]<2.', "COLZ")
    canv.SaveAs("METCut_failedMETFilterEvent_got_cosmic_ray.pdf")
