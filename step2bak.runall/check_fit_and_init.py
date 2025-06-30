#!/usr/bin/env python3
import ROOT

def get_hists(f) -> dict:
    def get_hist(f, theDIR, theBIN):
        return f.Get(f'{theBIN}_{theDIR}')
    def get_dir(f, theDIR) -> dict:
        return {
                'bin_0_0': get_hist(f, theDIR, 'bin_0_0'),
                'bin_0_1': get_hist(f, theDIR, 'bin_0_1'),
                'bin_1_0': get_hist(f, theDIR, 'bin_1_0'),
                'bin_1_1': get_hist(f, theDIR, 'bin_1_1'),
                    }
    return {
            'fracL': get_dir(f, 'fracL'),
            'fracC': get_dir(f, 'fracC'),
            'fracB': get_dir(f, 'fracB'),
            }
def SetHistVisualization(h,
        lineCOLOR=None, lineWIDTH=None,
        markerSIZE=None, markerCOLOR=None, markerSTYLE=None
        ):
    if lineCOLOR: h.SetLineColor(lineCOLOR)
    if lineWIDTH: h.SetLineWidth(lineWIDTH)
    if markerSIZE: h.SetMarkerSize(markerSIZE)
    if markerCOLOR: h.SetMarkerColor(markerCOLOR)
    if markerSTYLE: h.SetMarkerStyle(markerSTYLE)

    h.SetTitle("")
    h.SetStats(False)

def orig_main():
    getfile = lambda fNAME: ROOT.TFile.Open(fNAME)
    root_init = getfile('initinfo.datasideband.root')
    root_fitv = getfile('fitinfo.datasideband.root')

    hists_init = get_hists(root_init)
    hists_fitv = get_hists(root_fitv)
    def set_hists_visualization(hists, colorCODE):
        def set_all_binned_hists(hDICT, **kwargs):
            SetHistVisualization(hDICT['bin_0_0'], **kwargs)
            SetHistVisualization(hDICT['bin_0_1'], **kwargs)
            SetHistVisualization(hDICT['bin_1_0'], **kwargs)
            SetHistVisualization(hDICT['bin_1_1'], **kwargs)

        set_all_binned_hists(hists['fracL'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 20 , markerCOLOR = colorCODE)
        set_all_binned_hists(hists['fracC'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 34 , markerCOLOR = colorCODE)
        set_all_binned_hists(hists['fracB'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 22 , markerCOLOR = colorCODE)
    set_hists_visualization(hists_init, colorCODE = 38)
    set_hists_visualization(hists_fitv, colorCODE = 46)




    canv = ROOT.TCanvas("c1", "", 800,600)
    def output_pdf_file(hists_init,hists_fitv,binnedINFO):
        hists_init['fracL']['bin_0_0'].GetYaxis().SetRangeUser(0.,1.)
        hists_init['fracL']['bin_0_0'].GetYaxis().SetTitle('Quark Flavour Compositions')
        hists_init['fracL']['bin_0_0'].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')

        hists_init['fracL']['bin_0_0'].Draw('HIST')
        hists_init['fracC']['bin_0_0'].Draw('HIST SAME')
        hists_init['fracB']['bin_0_0'].Draw('HIST SAME')

        hists_fitv['fracL']['bin_0_0'].Draw('HIST SAME')
        hists_fitv['fracC']['bin_0_0'].Draw('HIST SAME')
        hists_fitv['fracB']['bin_0_0'].Draw('HIST SAME')


        hists_init['fracL']['bin_0_0'].Draw('EP SAME')
        hists_init['fracC']['bin_0_0'].Draw('EP SAME')
        hists_init['fracB']['bin_0_0'].Draw('EP SAME')

        hists_fitv['fracL']['bin_0_0'].Draw('EP SAME')
        hists_fitv['fracC']['bin_0_0'].Draw('EP SAME')
        hists_fitv['fracB']['bin_0_0'].Draw('EP SAME')

        leg = ROOT.TLegend(0.15, 0.35, 0.85, 0.65)
        leg.SetNColumns(2)
        leg.SetBorderSize(0)
        leg.SetFillColor(4004)
        leg.SetFillStyle(4004)
        leg.AddEntry(hists_init['fracL']['bin_0_0'], 'L jet from QCD simulations', 'LP')
        leg.AddEntry(hists_fitv['fracL']['bin_0_0'], 'from di-jet enriched region', 'LP')
        leg.AddEntry(hists_init['fracC']['bin_0_0'], 'C jet from QCD simulations', 'LP')
        leg.AddEntry(hists_fitv['fracC']['bin_0_0'], 'from di-jet enriched region', 'LP')
        leg.AddEntry(hists_init['fracB']['bin_0_0'], 'B jet from QCD simulations', 'LP')
        leg.AddEntry(hists_fitv['fracB']['bin_0_0'], 'from di-jet enriched region', 'LP')
        leg.Draw()

        canv.SaveAs(f'compareSB_{binnedINFO}.pdf')
    output_pdf_file(hists_init, hists_fitv, 'bin_0_0')
    output_pdf_file(hists_init, hists_fitv, 'bin_0_1')
    output_pdf_file(hists_init, hists_fitv, 'bin_1_0')
    output_pdf_file(hists_init, hists_fitv, 'bin_1_1')

if __name__ == '__main__':
    getfile = lambda fNAME: ROOT.TFile.Open(fNAME)
    #root_init = getfile('initinfo.datasideband.root')
    root_fitv = getfile('fitinfo.signalregion.root')

    #hists_init = get_hists(root_init)
    hists_fitv = get_hists(root_fitv)

    def set_hists_visualization(hists, colorCODE):
        def set_all_binned_hists(hDICT, **kwargs):
            SetHistVisualization(hDICT['bin_0_0'], **kwargs)
            SetHistVisualization(hDICT['bin_0_1'], **kwargs)
            SetHistVisualization(hDICT['bin_1_0'], **kwargs)
            SetHistVisualization(hDICT['bin_1_1'], **kwargs)

        set_all_binned_hists(hists['fracL'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 20 , markerCOLOR = colorCODE)
        set_all_binned_hists(hists['fracC'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 34 , markerCOLOR = colorCODE)
        set_all_binned_hists(hists['fracB'],
                lineCOLOR = colorCODE, lineWIDTH = 3, markerSIZE = 1, markerSTYLE = 22 , markerCOLOR = colorCODE)

    set_hists_visualization(hists_fitv, colorCODE = 46)




    canv = ROOT.TCanvas("c1", "", 800,600)
    def output_pdf_file(hists_init,binnedINFO):
        hists_init['fracL'][binnedINFO].GetYaxis().SetRangeUser(0.,1.)
        hists_init['fracL'][binnedINFO].GetYaxis().SetTitle('Quark Flavour Compositions')
        hists_init['fracL'][binnedINFO].GetXaxis().SetTitle('p_{T}^{#gamma} (GeV)')

        hists_init['fracL'][binnedINFO].Draw('HIST')
        hists_init['fracC'][binnedINFO].Draw('HIST SAME')
        hists_init['fracB'][binnedINFO].Draw('HIST SAME')


        hists_init['fracL'][binnedINFO].Draw('EP SAME')
        hists_init['fracC'][binnedINFO].Draw('EP SAME')
        hists_init['fracB'][binnedINFO].Draw('EP SAME')

        leg = ROOT.TLegend(0.15, 0.35, 0.45, 0.65)
        #leg.SetNColumns(1)
        leg.SetBorderSize(0)
        leg.SetFillColor(4004)
        leg.SetFillStyle(4004)
        leg.AddEntry(hists_init['fracL'][binnedINFO], 'l jet', 'LP')
        leg.AddEntry(hists_init['fracC'][binnedINFO], 'c jet', 'LP')
        leg.AddEntry(hists_init['fracB'][binnedINFO], 'b jet', 'LP')
        leg.Draw()

        canv.SaveAs(f'compareSR_{binnedINFO}.pdf')
    output_pdf_file(hists_fitv, 'bin_0_0')
    output_pdf_file(hists_fitv, 'bin_0_1')
    output_pdf_file(hists_fitv, 'bin_1_0')
    output_pdf_file(hists_fitv, 'bin_1_1')
