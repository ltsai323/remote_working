#!/usr/bin/env python3
import ROOT
### used for miniAOD v12

import ExternalFileMgr
def info(mesg):
    print(f'i@ {mesg}')



def Binning(df, pETAbin, jETAbin, pPTlow, pPThigh=-1):
    ### if pPThigh < 0, disable the upper bond of photon pt
    phoEtaCut = 'fabs(photon_eta)<1.5' if pETAbin == 0 else 'fabs(photon_eta)>1.5'
    jetEtaCut = 'fabs(jet_eta)<1.5 && jet_pt>0' if jETAbin == 0 else 'fabs(jet_eta)>1.5 && jet_pt>0'
    phoPtCut = f'photon_pt>{pPTlow} && photon_pt<{pPThigh}' if pPThigh > 0 else f'photon_pt>{pPTlow}'
    return df.Filter( '&&'.join([phoEtaCut,jetEtaCut, phoPtCut]) )



def DefineJetTruth(df):
    return df \
        .Define('isLJet', 'isHadFlvr_L == 1') \
        .Define('isCJet', 'isHadFlvr_C == 1') \
        .Define('isBJet', 'isHadFlvr_B == 1')



NUM_HIST_BIN = 5
def h_BDT(hNAME, hDESC):
    return (hNAME, hDESC, NUM_HIST_BIN, -1.,1.)
def h_CTagVar(hNAME, hDESC):
    return (hNAME, hDESC, NUM_HIST_BIN,  0.,1.)

def DataHistsSR(df):
    dfSR = df

    hists = []
    hists.append( dfSR.Histo1D(h_BDT('BDT_data_signalRegion', 'bdt_score'), 'photon_mva') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag0_data_signalRegion', 'bScore'), 'ParTB') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag1_data_signalRegion', 'CvsL'  ), 'ParTCvsL'  ) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag2_data_signalRegion', 'CvsB'  ), 'ParTCvsB'  ) )
    return hists

def DataHistsSB(df):
    dfSB = df
    hists = []
    hists.append( dfSB.Histo1D(h_BDT('BDT_data_dataSideband', 'bdt_score'), 'photon_mva') )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag0_data_dataSideband', 'bScore'), 'ParTB') )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag1_data_dataSideband', 'CvsL'  ), 'ParTCvsL'  ) )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag2_data_dataSideband', 'CvsB'  ), 'ParTCvsB'  ) )

    return hists
def GJetHists(df):
    def GetShapeDown(newNAME, hNOMINAL, hUNCup):
        newHist = hNOMINAL.Clone()
        newHist.SetName(newNAME)
        for ibin in range(hNOMINAL.GetNbinsX()+2):
            nom = hNOMINAL.GetBinContent(ibin)
            unc = hUNCup.GetBinContent(ibin)
            uncLow = nom - (unc-nom)
            if uncLow < 0: uncLow = 1e-10
            newHist.SetBinContent(ibin, uncLow)
        return newHist


    df__ = DefineJetTruth(df)
    dfSR = df__

    dfSR_B = dfSR.Filter('isBJet')
    dfSR_C = dfSR.Filter('isCJet')
    dfSR_L = dfSR.Filter('isLJet')

    def fill_quark_hist(hists, df_SR, tag):
        hists.append( df_SR.Histo1D(h_BDT(f'BDT_gjet{tag}_signalRegion', 'bdt_score'), 'photon_mva', 'wgt') )
        hists.append( df_SR.Histo1D(h_BDT(f'BDT_gjet{tag}_signalRegion_shapeUncUp', 'bdt_score ShapeUp'), 'photon_mva_orig', 'wgt') )
        hists.append( GetShapeDown(f'BDT_gjet{tag}_signalRegion_shapeUncDown', hists[-2], hists[-1]) )

        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag0_gjet{tag}_signalRegion', 'bScore'), 'ParTB', 'wgt') )
        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag1_gjet{tag}_signalRegion', 'CvsL'  ), 'ParTCvsL', 'wgt'  ) )
        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag2_gjet{tag}_signalRegion', 'CvsB'  ), 'ParTCvsB', 'wgt'  ) )

    hists = []
    hists.append( dfSR.Histo1D(h_BDT(f'BDT_gjets_signalRegion', 'bdt_score'), 'photon_mva', 'wgt') )
    hists.append( dfSR.Histo1D(h_BDT(f'BDT_gjets_signalRegion_shapeUncUp', 'bdt_score ShapeUp'), 'photon_mva_orig', 'wgt') )
    hists.append( GetShapeDown(f'BDT_gjets_signalRegion_shapeUncDown', hists[-2], hists[-1]) )

    fill_quark_hist(hists, dfSR_B, 'B')
    fill_quark_hist(hists, dfSR_C, 'C')
    fill_quark_hist(hists, dfSR_L, 'L')


    return hists


def main_func(
        dataERA,
        pETAbin, jETAbin,
        pPTlow, pPThigh
        ):
    inFILEs = ExternalFileMgr.GetEstimateSRFile(dataERA)
    info(f'[GotExternalFile] data era = "{ dataERA }, xPhotonFiles {inFILEs}')

    info(f'[LoadRDataframe] Loading dataframe from input files...')
    rdf_dataSR = ROOT.RDataFrame('tree', inFILEs.dataSR)
    rdf_dataSB = ROOT.RDataFrame('tree', inFILEs.dataSB)
    rdf_sign = ROOT.RDataFrame('tree', inFILEs.sign)
    #rdf_fake = ROOT.RDataFrame('tree', inFILEs.fake)
    info(f'[LoadRDataframe] Loading dataframe from input files... Finished')


    binned_dataSR = Binning(rdf_dataSR,  pETAbin,jETAbin,pPTlow,pPThigh)
    binned_dataSB = Binning(rdf_dataSB,  pETAbin,jETAbin,pPTlow,pPThigh)
    binned_sign = Binning(rdf_sign,  pETAbin,jETAbin,pPTlow,pPThigh)
    #binned_fake = Binning(rdf_fake,  pETAbin,jETAbin,pPTlow,pPThigh)

    data_histsSR = DataHistsSR(binned_dataSR)
    data_histsSB = DataHistsSB(binned_dataSB)
    sign_hists = GJetHists(binned_sign)


    newfile = ROOT.TFile('out_makehisto.root', 'recreate')
    for h in data_histsSR: h.Write()
    for h in data_histsSB: h.Write()
    for h in sign_hists: h.Write()
    newfile.Close()

if __name__ == "__main__":
    import sys
    from collections import namedtuple
    inARGs = namedtuple('inARGs', 'dataERA pETAbin jETAbin pPTlow pPThigh')
    in_args = inARGs(*sys.argv[1:])
    dataERA = in_args.dataERA
    pETAbin = int(in_args.pETAbin)
    jETAbin = int(in_args.jETAbin)
    pPTlow = float(in_args.pPTlow)
    pPThigh = float(in_args.pPThigh)
    ### if pPThigh < 0, disable the upper bond of photon pt

    #dataERA = "UL2016PostVFP"
    #pETAbin = 0
    #jETAbin = 0
    #pPTlow = 200
    #pPThigh = 220
    # { return std::vector<float>({190,200,220,250,300,        600,    1000, 9999}); }

    main_func(dataERA, pETAbin, jETAbin, pPTlow, pPThigh)

