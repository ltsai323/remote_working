#!/usr/bin/env python3
import ROOT
### used for miniAOD v12

import ExternalFileMgr
def info(mesg):
    print(f'i@ {mesg}')

'''
WP_PNET = {
        'loose' : 'PNetCvsL > 0.054 && PNetCvsB > 0.182',
        'medium': 'PNetCvsL > 0.160 && PNetCvsB > 0.304',
        'tight' : 'PNetCvsL > 0.491 && PNetCvsB > 0.258',
        }

WP_PART = {
        'loose' : 'ParTCvsL > 0.039 && ParTCvsB > 0.067',
        'medium': 'ParTCvsL > 0.117 && ParTCvsB > 0.128',
        'tight' : 'ParTCvsL > 0.358 && ParTCvsB > 0.095',
        }
def cut_WP(algo:str, wpTYPE:str):
    if algo == 'PNet': return WP_PNET[wpTYPE]
    if algo == 'ParT': return WP_PART[wpTYPE]
    raise IOError(f'[InvalidInput] algorithm "{ algo }" does not support in the working point')
'''

BRANCH_NAME = {
        'PNet': { 'CvsB': 'PNetCvsB', 'bScore': 'PNetB', 'CvsL': 'PNetCvsL' },
        'ParT': { 'CvsB': 'ParTCvsB', 'bScore': 'ParTB', 'CvsL': 'ParTCvsL' },
            }
def branchname(algo, var):
    return BRANCH_NAME[algo][var]
def load_var(var):
    algo = 'ParT'
    return BRANCH_NAME[algo][var]


def Binning(df, jETAbin, pPTlow, pPThigh=-1):
    ### if pPThigh < 0, disable the upper bond of photon pt
    #phoEtaCut = 'fabs(photon_eta)<1.5' if pETAbin == 0 else 'fabs(photon_eta)>1.5'
    jetEtaCut = 'fabs(jet_eta)<1.5 && jet_pt>0' if jETAbin == 0 else 'fabs(jet_eta)>1.5 && jet_pt>0'
    #phoPtCut = f'photon_pt>{pPTlow} && photon_pt<{pPThigh}' if pPThigh > 0 else f'photon_pt>{pPTlow}'
    return jetEtaCut
    #return df.Filter( '&&'.join([phoEtaCut,jetEtaCut, phoPtCut]) )



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
    #hists.append( dfSR.Histo1D(h_BDT('BDT_data_signalRegion', 'bdt_score'), 'photon_mva') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag0_data_signalRegion', 'bScore'), load_var('bScore')) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag1_data_signalRegion', 'CvsL'  ), load_var('CvsL')  ) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag2_data_signalRegion', 'CvsB'  ), load_var('CvsB')  ) )
    return hists

def DataHistsSB(df):
    dfSB = df
    hists = []
    #hists.append( dfSB.Histo1D(h_BDT('BDT_data_dataSideband', 'bdt_score'), 'photon_mva') )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag0_data_dataSideband', 'bScore'), load_var('bScore')) )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag1_data_dataSideband', 'CvsL'  ), load_var('CvsL')  ) )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag2_data_dataSideband', 'CvsB'  ), load_var('CvsB')  ) )

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

        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag0_gjet{tag}_signalRegion', 'bScore'), load_var('bScore'), 'wgt') )
        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag1_gjet{tag}_signalRegion', 'CvsL'  ), load_var('CvsL')  , 'wgt'  ) )
        hists.append( df_SR.Histo1D(h_CTagVar(f'jettag2_gjet{tag}_signalRegion', 'CvsB'  ), load_var('CvsB')  , 'wgt'  ) )

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
        jETAbin,
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


    binned_dataSR = Binning(rdf_dataSR,  jETAbin,pPTlow,pPThigh)
    binned_dataSB = Binning(rdf_dataSB,  jETAbin,pPTlow,pPThigh)
    binned_sign = Binning(rdf_sign,  jETAbin,pPTlow,pPThigh)
    #binned_fake = Binning(rdf_fake,  jETAbin,pPTlow,pPThigh)

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
    inARGs = namedtuple('inARGs', 'dataERA jETAbin pPTlow pPThigh')
    in_args = inARGs(*sys.argv[1:])
    dataERA = in_args.dataERA
    pETAbin = 0
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

    #main_func(dataERA, pETAbin, jETAbin, pPTlow, pPThigh)
    main_func(dataERA, jETAbin, pPTlow, pPThigh)

