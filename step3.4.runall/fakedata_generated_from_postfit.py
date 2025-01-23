#!/usr/bin/env python3

import ROOT
FILE_IDENTIFIER = 'fakedata_generated_from_postfit.py'
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')


def GetInputHists(iF, postfitDIR):
    return {
            'TotalProcs': iF.Get(f'{postfitDIR}/TotalProcs'),
            'TotalBkg'  : iF.Get(f'{postfitDIR}/TotalBkg'),
            'SB'        : iF.Get(f'{postfitDIR}/SB'),
            'ljet'      : iF.Get(f'{postfitDIR}/ljet'),
            'cjet'      : iF.Get(f'{postfitDIR}/cjet'),
            'bjet'      : iF.Get(f'{postfitDIR}/bjet'),
            'TotalSig'  : iF.Get(f'{postfitDIR}/TotalSig'),
            'data_obs'  : iF.Get(f'{postfitDIR}/data_obs'),
            }
def replace_psuedodata(histSOURCEs:dict):
    num_entries = histSOURCEs['data_obs'].Integral()
    histSOURCEs['data_obs'].Reset()
    histSOURCEs['data_obs'].FillRandom(histSOURCEs['TotalProcs'], int(num_entries))

def testfunc_replace_psuedodata(histSOURCEs:dict):
    canv = ROOT.TCanvas("c1", "", 800, 600)
    histSOURCEs['data_obs'].Draw()
    canv.SaveAs("hdata_source.png")

    replace_psuedodata(histSOURCEs)

    histSOURCEs['data_obs'].Draw()
    canv.SaveAs("hdata_psuedodata.png")


def save_output_file( outFILEname:str, histREC:dict ):
    info(f'[Export] Generating ROOT file "{ outFILEname }"')
    f_out = ROOT.TFile(outFILEname, 'recreate')
    for dirNAME, histDICT in histREC.items():
        dir_rec = f_out.mkdir(dirNAME)
        info(f'[Export] Saving content to folder "{ dirNAME }"')
        dir_rec.cd()
        for hNAME, hist in histDICT.items():
            hist.Write()
    f_out.Close()
    info(f'[Export] Generating ROOT file "{ outFILEname }" finished')

if __name__ == "__main__":
    inFILE = 'postfit.root'
    iF = ROOT.TFile.Open(inFILE)
    hist_cvsl = GetInputHists(iF, 'cvsl_postfit')
    hist_cvsb = GetInputHists(iF, 'cvsb_postfit')
    hist_btag = GetInputHists(iF, 'btag_postfit')
    hist_gjet = GetInputHists(iF, 'gjet_postfit')

    replace_psuedodata(hist_cvsl)
    #testfunc_replace_psuedodata(hist_cvsl)
    replace_psuedodata(hist_cvsb)
    replace_psuedodata(hist_btag)
    replace_psuedodata(hist_gjet)

    outFILEname = 'postfit.psuedodata.root'
    save_output_file( outFILEname, {
            'cvsl_postfit': hist_cvsl,
            'cvsb_postfit': hist_cvsb,
            'btag_postfit': hist_btag,
            'gjet_postfit': hist_gjet,
            } )

    iF.Close()
