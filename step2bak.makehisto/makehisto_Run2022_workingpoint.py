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
NUM_SVMASS_BIN = 40
def h_SecVMass(hNAME, hDESC):
    return (hNAME, hDESC, NUM_SVMASS_BIN, 0., 5.)

def DataHistsSR(df):
    dfSR = df

    hists = []

    df0 = df
    dfCl= df.Filter('WPc_loose')
    dfCm= df.Filter('WPc_medium')
    dfCt= df.Filter('WPc_tight')

    dfBl= df.Filter('WPb_loose')
    dfBm= df.Filter('WPb_medium')
    dfBt= df.Filter('WPb_tight')

    def fill_hist(hists, dF, hNAME):
        hists.append( dF.Histo1D(h_BDT(hNAME, 'bdt_score'), 'photon_mva') )

    fill_hist(hists, df0  , 'BDT_data_signalRegion')

    fill_hist(hists, dfCl , 'BDTWPcL_data_signalRegion')
    fill_hist(hists, dfCm , 'BDTWPcM_data_signalRegion')
    fill_hist(hists, dfCt , 'BDTWPcT_data_signalRegion')

    fill_hist(hists, dfBl , 'BDTWPbL_data_signalRegion')
    fill_hist(hists, dfBm , 'BDTWPbM_data_signalRegion')
    fill_hist(hists, dfBt , 'BDTWPbT_data_signalRegion')

    return hists

def DataHistsSB(df):
    hists = []

    df0 = df
    dfCl= df.Filter('WPc_loose')
    dfCm= df.Filter('WPc_medium')
    dfCt= df.Filter('WPc_tight')

    dfBl= df.Filter('WPb_loose')
    dfBm= df.Filter('WPb_medium')
    dfBt= df.Filter('WPb_tight')

    def fill_hist(hists, dF, hNAME):
        hists.append( dF.Histo1D(h_BDT(hNAME, 'bdt_score'), 'photon_mva') )

    fill_hist(hists, df0  , 'BDT_data_dataSideband')

    fill_hist(hists, dfCl , 'BDTWPcL_data_dataSideband')
    fill_hist(hists, dfCm , 'BDTWPcM_data_dataSideband')
    fill_hist(hists, dfCt , 'BDTWPcT_data_dataSideband')

    fill_hist(hists, dfBl , 'BDTWPbL_data_dataSideband')
    fill_hist(hists, dfBm , 'BDTWPbM_data_dataSideband')
    fill_hist(hists, dfBt , 'BDTWPbT_data_dataSideband')

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

    df0 = dfSR
    dfCl= dfSR.Filter('WPc_loose')
    dfCm= dfSR.Filter('WPc_medium')
    dfCt= dfSR.Filter('WPc_tight')

    dfBl= dfSR.Filter('WPb_loose')
    dfBm= dfSR.Filter('WPb_medium')
    dfBt= dfSR.Filter('WPb_tight')


    def fill_hist(hists, df, hNAME):
        hists.append( df.Histo1D(h_BDT(hNAME, 'bdt_score'), 'photon_mva', 'wgt') )
        hists.append( df.Histo1D(h_BDT(f'{hNAME}_shapeUncUp', 'bdt_score ShapeUp'), 'photon_mva_orig', 'wgt') )
        hists.append( GetShapeDown(       f'{hNAME}_shapeUncDown', hists[-2], hists[-1]) )


    hists = []
    fill_hist(hists, df0,  'BDT_gjet_signalRegion')
    fill_hist(hists, dfCl, 'BDTWPcL_gjet_signalRegion')
    fill_hist(hists, dfCm, 'BDTWPcM_gjet_signalRegion')
    fill_hist(hists, dfCt, 'BDTWPcT_gjet_signalRegion')

    fill_hist(hists, dfBl, 'BDTWPbL_gjet_signalRegion')
    fill_hist(hists, dfBm, 'BDTWPbM_gjet_signalRegion')
    fill_hist(hists, dfBt, 'BDTWPbT_gjet_signalRegion')


    return hists


def define_working_points(df):
    return df \
            .Define('WPc_loose' , 'ParTCvsL > 0.039 && ParTCvsB > 0.067' ) \
            .Define('WPc_medium', 'ParTCvsL > 0.117 && ParTCvsB > 0.128' ) \
            .Define('WPc_tight' , 'ParTCvsL > 0.358 && ParTCvsB > 0.095' ) \
            .Define('WPb_loose' , 'ParTB > 0.0897') \
            .Define('WPb_medium', 'ParTB > 0.4510') \
            .Define('WPb_tight' , 'ParTB > 0.8604')



def main_func(
        dataERA,
        pETAbin, jETAbin,
        pPTlow, pPThigh
        ):
    inFILEs = ExternalFileMgr.GetEstimateSRFile_GJet(dataERA)
    info(f'[GotExternalFile] data era = "{ dataERA }, xPhotonFiles {inFILEs}')

    info(f'[LoadRDataframe] Loading dataframe from input files...')
    rdf_dataSR = ROOT.RDataFrame('tree', inFILEs.dataSR)
    rdf_dataSB = ROOT.RDataFrame('tree', inFILEs.dataSB)
    rdf_sign = ROOT.RDataFrame('tree', inFILEs.sign)
    #rdf_fake = ROOT.RDataFrame('tree', inFILEs.fake)
    info(f'[LoadRDataframe] Loading dataframe from input files... Finished')

    rdf_dataSR = define_working_points(rdf_dataSR)
    rdf_dataSB = define_working_points(rdf_dataSB)
    rdf_sign   = define_working_points(rdf_sign  )
    #rdf_fake = ROOT.RDataFrame('tree', inFILEs.fake)


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

