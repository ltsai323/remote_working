#!/usr/bin/env python3
import ExternalFileMgr
import ROOT
from makehisto_Run2022_workingpoint import *

def DataHistsSR_truth_values(df):

    hists = []

    df0 = DefineJetTruth(df)
    def fill_hist(hists, dF, hNAME):
        hists.append( dF.Histo1D(h_BDT(hNAME, 'bdt_score'), 'photon_mva', 'wgt') )

    fill_hist(hists, df0.Filter("isLJet")  , 'BDT_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet")  , 'BDT_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet")  , 'BDT_bjet_truthvalue')

    fill_hist(hists, df0.Filter("isLJet").Filter('WPc_loose')  , 'BDTWPcL_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPc_loose')  , 'BDTWPcL_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPc_loose')  , 'BDTWPcL_bjet_truthvalue')

    fill_hist(hists, df0.Filter("isLJet").Filter('WPc_medium') , 'BDTWPcM_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPc_medium') , 'BDTWPcM_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPc_medium') , 'BDTWPcM_bjet_truthvalue')

    fill_hist(hists, df0.Filter("isLJet").Filter('WPc_tight')  , 'BDTWPcT_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPc_tight')  , 'BDTWPcT_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPc_tight')  , 'BDTWPcT_bjet_truthvalue')


    fill_hist(hists, df0.Filter("isLJet").Filter('WPb_loose')  , 'BDTWPbL_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPb_loose')  , 'BDTWPbL_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPb_loose')  , 'BDTWPbL_bjet_truthvalue')

    fill_hist(hists, df0.Filter("isLJet").Filter('WPb_medium') , 'BDTWPbM_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPb_medium') , 'BDTWPbM_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPb_medium') , 'BDTWPbM_bjet_truthvalue')

    fill_hist(hists, df0.Filter("isLJet").Filter('WPb_tight')  , 'BDTWPbT_ljet_truthvalue')
    fill_hist(hists, df0.Filter("isCJet").Filter('WPb_tight')  , 'BDTWPbT_cjet_truthvalue')
    fill_hist(hists, df0.Filter("isBJet").Filter('WPb_tight')  , 'BDTWPbT_bjet_truthvalue')
    return hists
def DataHistsSR_fake(df):
    hists = []

    df0 = df
    dfCl= df.Filter('WPc_loose')
    dfCm= df.Filter('WPc_medium')
    dfCt= df.Filter('WPc_tight')

    dfBl= df.Filter('WPb_loose')
    dfBm= df.Filter('WPb_medium')
    dfBt= df.Filter('WPb_tight')

    def fill_hist(hists, dF, hNAME):
        hists.append( dF.Histo1D(h_BDT(hNAME, 'bdt_score'), 'photon_mva', 'wgt') )

    fill_hist(hists, df0  , 'BDT_data_signalRegion')

    fill_hist(hists, dfCl , 'BDTWPcL_data_signalRegion')
    fill_hist(hists, dfCm , 'BDTWPcM_data_signalRegion')
    fill_hist(hists, dfCt , 'BDTWPcT_data_signalRegion')

    fill_hist(hists, dfBl , 'BDTWPbL_data_signalRegion')
    fill_hist(hists, dfBm , 'BDTWPbM_data_signalRegion')
    fill_hist(hists, dfBt , 'BDTWPbT_data_signalRegion')

    return hists

def main_func(
        dataERA,
        pETAbin, jETAbin,
        pPTlow, pPThigh
        ):
    inFILEs = ExternalFileMgr.GetEstimateSRFile_GJet(dataERA)
    info(f'[GotExternalFile] data era = "{ dataERA }, xPhotonFiles {inFILEs}')

    info(f'[LoadRDataframe] Loading dataframe from input files...')
    rdf_dataSR = ROOT.RDataFrame('tree', inFILEs.sign)
    info(f'[LoadRDataframe] Loading dataframe from input files... Finished')

    rdf_dataSR = define_working_points(rdf_dataSR)


    binned_dataSR = Binning(rdf_dataSR,  pETAbin,jETAbin,pPTlow,pPThigh)

    data_histsSR = DataHistsSR_fake(binned_dataSR)
    truthhistsSR = DataHistsSR_truth_values(binned_dataSR)


    newfile = ROOT.TFile('out_makehisto.root', 'recreate')
    for h in data_histsSR: h.Write()
    for h in truthhistsSR: h.Write()
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


    main_func(dataERA, pETAbin, jETAbin, pPTlow, pPThigh)

