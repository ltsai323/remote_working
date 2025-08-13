#!/usr/bin/env python3
import ROOT
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc, Define_NormalizeBTagSF
import makehisto_usefulfunc as extfunc
### used for miniAOD v12
DEBUG_MODE = False

def info(mesg):
    print(f'i@ {mesg}')

#from makehisto_usefulfunc import UsedDataFrames, histCollection
#from makehisto_usefulfunc import hBDTAll, hBDTAct, hSVmAll, hSVmAct
import makehisto_usefulfunc as frag

DATA_LUMINOSITY = 26.81 # 2022EE

def define_and_filter(usedDF: frag.UsedDataFrames, dfCUTfuncs:dict, dfDEFfuncs:dict, rescaleSIGN=False):
    the_data0 = usedDF.dfSR
    the_sign0 = usedDF.dfsign
    the_fake0 = usedDF.dffake
    the_side0 = usedDF.dfSB

    the_dataD = dfDEFfuncs['data'](the_data0)
    the_signD = dfDEFfuncs['sign'](the_sign0)
    the_fakeD = dfDEFfuncs['fake'](the_fake0)
    the_sideD = dfDEFfuncs['side'](the_side0)




    ############ defining variables #####################
    the_data1 = define_working_points(the_dataD)
    the_sign1 = define_working_points(the_signD)
    the_fake1 = define_working_points(the_fakeD)
    the_side1 = define_working_points(the_sideD)

    the_sign2 = DefineJetTruth(the_sign1)
    the_fake2 = DefineJetTruth(the_fake1)

    the_data = dfCUTfuncs['data'](the_data1)
    the_sign = dfCUTfuncs['sign'](the_sign2)
    the_fake = dfCUTfuncs['fake'](the_fake2)
    the_side = dfCUTfuncs['side'](the_side1)
    ############ defining variables end #################


    if rescaleSIGN:
        data_integral = the_data.Sum("event_weight").GetValue()
        sign_integral = the_sign.Sum("event_weight").GetValue()
        the_sign = the_sign \
                .Define('rescaling', f'{data_integral}/{sign_integral}') \
                .Define('event_weight_', 'event_weight') \
                .Redefine('event_weight', 'event_weight * rescaling')

    usedDF.dfSR = the_data
    usedDF.dfsign = the_sign
    usedDF.dffake = the_fake
    usedDF.dfSB = the_side
    return usedDF


def main_content_WPbL( usedDF: frag.UsedDataFrames, outputFILE):
    #used_df = define_and_filter(usedDF, dfCUTfuncs, dfDEFfuncs)
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB





    class NameSet:
        def __init__(self, varNAME):
            self.data = f'data_{varNAME}'
            self.gjet = f'gjet_{varNAME}'
            self.sigL = f'sigL_{varNAME}'
            self.sigC = f'sigC_{varNAME}'
            self.sigB = f'sigB_{varNAME}'
            self.fake = f'fake_{varNAME}'
            self.side = f'side_{varNAME}' # data sideband

            #print(f'[NameSet] Generating histograms: {self.data} {self.sign} {self.fake} {self.stak} {self.diff}')



    def plot_all_vars(oTAG, dfDATA, dfSIGN, dfFAKE, dfSIDE):
        if not dfSIGN.HasColumn(extfunc.evtwgt_WPbLCentral):
            raise RuntimeError(f'[NoWPbSF] Need to add btag sf to dfSIGN.')
        if not dfFAKE.HasColumn(extfunc.evtwgt_WPbLCentral):
            raise RuntimeError(f'[NoWPbSF] Need to add btag sf to dfFAKE.')
        dfSigL = dfSIGN.Filter('isLJet')
        dfSigC = dfSIGN.Filter('isCJet')
        dfSigB = dfSIGN.Filter('isBJet')

        names = NameSet(oTAG)
        hists = frag.histCollection()

        ### all entries
        hists.data_BDTAll = dfDATA.Histo1D( frag.hBDTAll(names.data), 'photon_mva', 'event_weight' )
        hists.gjet_BDTAll = dfSIGN.Histo1D( frag.hBDTAll(names.gjet), 'photon_mva', 'event_weight' )
        hists.sigL_BDTAll = dfSigL.Histo1D( frag.hBDTAll(names.sigL), 'photon_mva', 'event_weight' )
        hists.sigC_BDTAll = dfSigC.Histo1D( frag.hBDTAll(names.sigC), 'photon_mva', 'event_weight' )
        hists.sigB_BDTAll = dfSigB.Histo1D( frag.hBDTAll(names.sigB), 'photon_mva', 'event_weight' )
        hists.fake_BDTAll = dfFAKE.Histo1D( frag.hBDTAll(names.fake), 'photon_mva', 'event_weight' )
        hists.side_BDTAll = dfSIDE.Histo1D( frag.hBDTAll(names.side), 'photon_mva', 'event_weight' )

        hists.data_btag = dfDATA.Histo1D( frag.hbtag(names.data), 'ParTB', 'event_weight' )
        hists.sigL_btag = dfSigL.Histo1D( frag.hbtag(names.sigL), 'ParTB', extfunc.evtwgt_WPbLCentral )
        hists.sigC_btag = dfSigC.Histo1D( frag.hbtag(names.sigC), 'ParTB', extfunc.evtwgt_WPbLCentral )
        hists.sigB_btag = dfSigB.Histo1D( frag.hbtag(names.sigB), 'ParTB', extfunc.evtwgt_WPbLCentral )
        hists.fake_btag = dfFAKE.Histo1D( frag.hbtag(names.fake), 'ParTB', extfunc.evtwgt_WPbLCentral )
        hists.side_btag = dfSIDE.Histo1D( frag.hbtag(names.side), 'ParTB', 'event_weight' )

        hists.data_cvsb = dfDATA.Histo1D( frag.hcvsb(names.data), 'ParTCvsB', 'event_weight' )
        hists.sigL_cvsb = dfSigL.Histo1D( frag.hcvsb(names.sigL), 'ParTCvsB', 'event_weight' )
        hists.sigC_cvsb = dfSigC.Histo1D( frag.hcvsb(names.sigC), 'ParTCvsB', 'event_weight' )
        hists.sigB_cvsb = dfSigB.Histo1D( frag.hcvsb(names.sigB), 'ParTCvsB', 'event_weight' )
        hists.fake_cvsb = dfFAKE.Histo1D( frag.hcvsb(names.fake), 'ParTCvsB', 'event_weight' )
        hists.side_cvsb = dfSIDE.Histo1D( frag.hcvsb(names.side), 'ParTCvsB', 'event_weight' )

        hists.data_cvsl = dfDATA.Histo1D( frag.hcvsl(names.data), 'ParTCvsL', 'event_weight' )
        hists.sigL_cvsl = dfSigL.Histo1D( frag.hcvsl(names.sigL), 'ParTCvsL', 'event_weight' )
        hists.sigC_cvsl = dfSigC.Histo1D( frag.hcvsl(names.sigC), 'ParTCvsL', 'event_weight' )
        hists.sigB_cvsl = dfSigB.Histo1D( frag.hcvsl(names.sigB), 'ParTCvsL', 'event_weight' )
        hists.fake_cvsl = dfFAKE.Histo1D( frag.hcvsl(names.fake), 'ParTCvsL', 'event_weight' )
        hists.side_cvsl = dfSIDE.Histo1D( frag.hcvsl(names.side), 'ParTCvsL', 'event_weight' )



        return hists



    h_allgjets = plot_all_vars(
            'gjet',
            the_data,
            the_sign,
            the_fake,
            the_side
    )
    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'recreate')
    h_allgjets.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    f_out.Close()
def main_content( usedDF: frag.UsedDataFrames, outputFILE):
    #used_df = define_and_filter(usedDF, dfCUTfuncs, dfDEFfuncs)
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB





    class NameSet:
        def __init__(self, varNAME):
            self.data = f'data_{varNAME}'
            self.gjet = f'gjet_{varNAME}'
            self.sigL = f'sigL_{varNAME}'
            self.sigC = f'sigC_{varNAME}'
            self.sigB = f'sigB_{varNAME}'
            self.fake = f'fake_{varNAME}'
            self.side = f'side_{varNAME}' # data sideband

            #print(f'[NameSet] Generating histograms: {self.data} {self.sign} {self.fake} {self.stak} {self.diff}')



    def plot_all_vars(oTAG, dfDATA, dfSIGN, dfFAKE, dfSIDE):
        dfSigL = dfSIGN.Filter('isLJet')
        dfSigC = dfSIGN.Filter('isCJet')
        dfSigB = dfSIGN.Filter('isBJet')

        names = NameSet(oTAG)
        hists = frag.histCollection()

        ### all entries
        hists.data_BDTAll = dfDATA.Histo1D( frag.hBDTAll(names.data), 'photon_mva', 'event_weight' )
        hists.gjet_BDTAll = dfSIGN.Histo1D( frag.hBDTAll(names.gjet), 'photon_mva', 'event_weight' )
        hists.sigL_BDTAll = dfSigL.Histo1D( frag.hBDTAll(names.sigL), 'photon_mva', 'event_weight' )
        hists.sigC_BDTAll = dfSigC.Histo1D( frag.hBDTAll(names.sigC), 'photon_mva', 'event_weight' )
        hists.sigB_BDTAll = dfSigB.Histo1D( frag.hBDTAll(names.sigB), 'photon_mva', 'event_weight' )
        hists.fake_BDTAll = dfFAKE.Histo1D( frag.hBDTAll(names.fake), 'photon_mva', 'event_weight' )
        hists.side_BDTAll = dfSIDE.Histo1D( frag.hBDTAll(names.side), 'photon_mva', 'event_weight' )

        hists.data_btag = dfDATA.Histo1D( frag.hbtag(names.data), 'ParTB', 'event_weight' )
        hists.sigL_btag = dfSigL.Histo1D( frag.hbtag(names.sigL), 'ParTB', 'event_weight' )
        hists.sigC_btag = dfSigC.Histo1D( frag.hbtag(names.sigC), 'ParTB', 'event_weight' )
        hists.sigB_btag = dfSigB.Histo1D( frag.hbtag(names.sigB), 'ParTB', 'event_weight' )
        hists.fake_btag = dfFAKE.Histo1D( frag.hbtag(names.fake), 'ParTB', 'event_weight' )
        hists.side_btag = dfSIDE.Histo1D( frag.hbtag(names.side), 'ParTB', 'event_weight' )

        hists.data_cvsb = dfDATA.Histo1D( frag.hcvsb(names.data), 'ParTCvsB', 'event_weight' )
        hists.sigL_cvsb = dfSigL.Histo1D( frag.hcvsb(names.sigL), 'ParTCvsB', 'event_weight' )
        hists.sigC_cvsb = dfSigC.Histo1D( frag.hcvsb(names.sigC), 'ParTCvsB', 'event_weight' )
        hists.sigB_cvsb = dfSigB.Histo1D( frag.hcvsb(names.sigB), 'ParTCvsB', 'event_weight' )
        hists.fake_cvsb = dfFAKE.Histo1D( frag.hcvsb(names.fake), 'ParTCvsB', 'event_weight' )
        hists.side_cvsb = dfSIDE.Histo1D( frag.hcvsb(names.side), 'ParTCvsB', 'event_weight' )

        hists.data_cvsl = dfDATA.Histo1D( frag.hcvsl(names.data), 'ParTCvsL', 'event_weight' )
        hists.sigL_cvsl = dfSigL.Histo1D( frag.hcvsl(names.sigL), 'ParTCvsL', 'event_weight' )
        hists.sigC_cvsl = dfSigC.Histo1D( frag.hcvsl(names.sigC), 'ParTCvsL', 'event_weight' )
        hists.sigB_cvsl = dfSigB.Histo1D( frag.hcvsl(names.sigB), 'ParTCvsL', 'event_weight' )
        hists.fake_cvsl = dfFAKE.Histo1D( frag.hcvsl(names.fake), 'ParTCvsL', 'event_weight' )
        hists.side_cvsl = dfSIDE.Histo1D( frag.hcvsl(names.side), 'ParTCvsL', 'event_weight' )



        return hists



    h_allgjets = plot_all_vars(
            'gjet',
            the_data,
            the_sign,
            the_fake,
            the_side
    )
    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'recreate')
    h_allgjets.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    f_out.Close()



def test_main_content(outHISTname):
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )

    general_cut = 'photon_pt>210'
    cut_func = {
            'data': lambda df: df.Filter(f'{general_cut} && 1'),
            'sign': lambda df: df.Filter(f'{general_cut} && 1'),
            'fake': lambda df: df.Filter(f'{general_cut} && 1'),
            'side': lambda df: df.Filter(f'{general_cut} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight','1'),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    df_sig = Define_NormalizeBTagSF(used_df.dfsign, 'renormREQUIRED_wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)
    df_bkg = Define_NormalizeBTagSF(used_df.dffake, 'renormREQUIRED_wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)
    #df_sig = Define_NormalizeBTagSF(used_df.dfsign, 'wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)
    #df_bkg = Define_NormalizeBTagSF(used_df.dffake, 'wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)

    used_df.dfsign = df_sig
    used_df.dffake = df_bkg


    main_content_WPbL(
        usedDF = used_df,
        outputFILE = outHISTname,
    )
def test_main_content2():
    used_data_frames = UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )

    general_cut = 'photon_pt>210'

    binning = 'photon_pt>210 && photon_pt<230 && abs(jet_eta)<1.5 && abs(photon_eta)<1.5'
    cut_func = {
            'data': lambda df: df.Filter(f'{binning} && 1'),
            'sign': lambda df: df.Filter(f'{binning} && 1'),
            'fake': lambda df: df.Filter(f'{binning} && 1'),
            'side': lambda df: df.Filter(f'{binning} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight','1'),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    main_content(
        usedDF = used_df,
        outputFILE = 'makehisto.root',
    )





def DefineJetTruth(df):
    return df \
        .Define('isLJet', 'isHadFlvr_L == 1') \
        .Define('isCJet', 'isHadFlvr_C == 1') \
        .Define('isBJet', 'isHadFlvr_B == 1')




def define_working_points(df):
    return df \
            .Define('WPc_loose' , 'ParTCvsL > 0.039 && ParTCvsB > 0.067' ) \
            .Define('WPc_medium', 'ParTCvsL > 0.117 && ParTCvsB > 0.128' ) \
            .Define('WPc_tight' , 'ParTCvsL > 0.358 && ParTCvsB > 0.095' ) \
            .Define('WPb_loose' , 'ParTB > 0.0897') \
            .Define('WPb_medium', 'ParTB > 0.4510') \
            .Define('WPb_tight' , 'ParTB > 0.8604')



# https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/
btv_jet_binnings = [20, 30, 50, 70, 100, 140, 200, 300, 600, 1000, 1500]
from array import array
BTV_JET = lambda name: (name, '', len(btv_jet_binnings)-1, array('f',btv_jet_binnings))

pho_pt_binnings = [210,230,250,300,400,500,600,1000,1500]
MY_BIN = lambda name: (name, '', len(pho_pt_binnings)-1, array('f',pho_pt_binnings))


def mainfunc(usedDFs):
    grapherrs = frag.histCollection()

    def Get_Eff(oNAME, dfALL, cutSTR):
        dfCUT = dfALL.Filter(cutSTR)

        h_all = dfALL.Histo1D( BTV_JET(f'h_all_{oNAME}'), 'jet_pt', 'event_weight')
        h_cut = dfCUT.Histo1D( BTV_JET(f'h_cut_{oNAME}'), 'jet_pt', 'event_weight')
        
        o = ROOT.TGraphAsymmErrors()
        o.Divide( h_cut.GetValue(), h_all.GetValue(), 'pois')
        o.SetName(oNAME)
        return o
       #return o, h_all, h_cut
    ### origeff: calculate efficiencies of passing WPbL and only apply event weight as reference
    dfSIGNorig = usedDFs.dfsign.Define('event_weight', f'wgt*{DATA_LUMINOSITY}')

    grapherrs.origeffL0 = Get_Eff( 'origeffL0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && isHadFlvr_L'), 'passWPbL' )
    grapherrs.origeffC0 = Get_Eff( 'origeffC0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && isHadFlvr_C'), 'passWPbL' )
    grapherrs.origeffB0 = Get_Eff( 'origeffB0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && isHadFlvr_B'), 'passWPbL' )
    grapherrs.origeffL1 = Get_Eff( 'origeffL1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && isHadFlvr_L'), 'passWPbL' )
    grapherrs.origeffC1 = Get_Eff( 'origeffC1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && isHadFlvr_C'), 'passWPbL' )
    grapherrs.origeffB1 = Get_Eff( 'origeffB1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && isHadFlvr_B'), 'passWPbL' )

    grapherrs.origpurityL0 = Get_Eff( 'origpurityL0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_L' )
    grapherrs.origpurityC0 = Get_Eff( 'origpurityC0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_C' )
    grapherrs.origpurityB0 = Get_Eff( 'origpurityB0', dfSIGNorig.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_B' )
    grapherrs.origpurityL1 = Get_Eff( 'origpurityL1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_L' )
    grapherrs.origpurityC1 = Get_Eff( 'origpurityC1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_C' )
    grapherrs.origpurityB1 = Get_Eff( 'origpurityB1', dfSIGNorig.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_B' )


    def GetUncRatio(oNAME, df, wgtCENTRAL, wgtUNC):
        df_ = df.Define('wgt0', f'event_weight * {wgtCENTRAL}') \
                .Define('wgt1', f'event_weight * {wgtUNC}')
        h_central = df_.Histo1D( MY_BIN('h_ref'), 'photon_pt', 'wgt0' )
        h_unc     = df_.Histo1D( MY_BIN('h_unc'), 'photon_pt', 'wgt1' )
        o = ROOT.TGraphAsymmErrors()
        o.Divide( h_unc.GetValue(), h_central.GetValue(), 'pois' )
        o.SetName(oNAME)
        return o
    ### eff: calculate efficiencies of passing WPbL with BTV WPbL central SF
    dfSIGN = usedDFs.dfsign \
            .Define('event_weight', f'wgt*{DATA_LUMINOSITY}*renormREQUIRED_wgt_WPbL_central') \


    grapherrs.effL0 = Get_Eff( 'effL0', dfSIGN.Filter('abs(jet_eta)<1.5 && isHadFlvr_L'), 'passWPbL' )
    grapherrs.effC0 = Get_Eff( 'effC0', dfSIGN.Filter('abs(jet_eta)<1.5 && isHadFlvr_C'), 'passWPbL' )
    grapherrs.effB0 = Get_Eff( 'effB0', dfSIGN.Filter('abs(jet_eta)<1.5 && isHadFlvr_B'), 'passWPbL' )
    grapherrs.effL1 = Get_Eff( 'effL1', dfSIGN.Filter('abs(jet_eta)>1.5 && isHadFlvr_L'), 'passWPbL' )
    grapherrs.effC1 = Get_Eff( 'effC1', dfSIGN.Filter('abs(jet_eta)>1.5 && isHadFlvr_C'), 'passWPbL' )
    grapherrs.effB1 = Get_Eff( 'effB1', dfSIGN.Filter('abs(jet_eta)>1.5 && isHadFlvr_B'), 'passWPbL' )

    grapherrs.purityL0 = Get_Eff( 'purityL0', dfSIGN.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_L' )
    grapherrs.purityC0 = Get_Eff( 'purityC0', dfSIGN.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_C' )
    grapherrs.purityB0 = Get_Eff( 'purityB0', dfSIGN.Filter('abs(jet_eta)<1.5 && passWPbL'), 'isHadFlvr_B' )
    grapherrs.purityL1 = Get_Eff( 'purityL1', dfSIGN.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_L' )
    grapherrs.purityC1 = Get_Eff( 'purityC1', dfSIGN.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_C' )
    grapherrs.purityB1 = Get_Eff( 'purityB1', dfSIGN.Filter('abs(jet_eta)>1.5 && passWPbL'), 'isHadFlvr_B' )

    dfSIGNL_bin00 = dfSIGNorig.Filter('passWPbL && isHadFlvr_L && abs(photon_eta)<1.5 && abs(jet_eta)<1.5')
    grapherrs.uncL_statUp00 = GetUncRatio( 'uncL_statUp00', dfSIGNL_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_lStatUp' )
    grapherrs.uncL_statDn00 = GetUncRatio( 'uncL_statDn00', dfSIGNL_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_lStatDown' )

    dfSIGNB_bin00 = dfSIGNorig.Filter('passWPbL && isHadFlvr_B && abs(photon_eta)<1.5 && abs(jet_eta)<1.5')
    grapherrs.uncB_statUp00   = GetUncRatio( 'uncB_statUp00'  , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_bStatUp' )
    grapherrs.uncB_statDn00   = GetUncRatio( 'uncB_statDn00'  , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_bStatDown' )
    grapherrs.uncB_Up00       = GetUncRatio( 'uncB_Up00'      , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bUp"       )
    grapherrs.uncB_Dn00       = GetUncRatio( 'uncB_Dn00'      , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bDown"     )
    grapherrs.uncB_JESUp00    = GetUncRatio( 'uncB_JESUp00'   , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bJESUp"    )
    grapherrs.uncB_JESDn00    = GetUncRatio( 'uncB_JESDn00'   , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bJESDown"  )
    grapherrs.uncB_FragUp00   = GetUncRatio( 'uncB_FragUp00'  , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bFragUp"   )
    grapherrs.uncB_FragDn00   = GetUncRatio( 'uncB_FragDn00'  , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bFragDown" )
    grapherrs.uncB_PUUp00     = GetUncRatio( 'uncB_PUUp00'    , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bPUUp"     )
    grapherrs.uncB_PUDn00     = GetUncRatio( 'uncB_PUDn00'    , dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bPUDown"   )
    grapherrs.uncB_bType3Up00 = GetUncRatio( 'uncB_bType3Up00', dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bType3Up"  )
    grapherrs.uncB_bType3Dn00 = GetUncRatio( 'uncB_bType3Dn00', dfSIGNB_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bType3Down")

    dfSIGNC_bin00 = dfSIGNorig.Filter('passWPbL && isHadFlvr_C && abs(photon_eta)<1.5 && abs(jet_eta)<1.5')
    grapherrs.uncC_statUp00   = GetUncRatio( 'uncC_statUp00'  , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_bStatUp' )
    grapherrs.uncC_statDn00   = GetUncRatio( 'uncC_statDn00'  , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', 'renormREQUIRED_wgt_WPbL_bStatDown' )
    grapherrs.uncC_Up00       = GetUncRatio( 'uncC_Up00'      , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bUp"       )
    grapherrs.uncC_Dn00       = GetUncRatio( 'uncC_Dn00'      , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bDown"     )
    grapherrs.uncC_JESUp00    = GetUncRatio( 'uncC_JESUp00'   , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bJESUp"    )
    grapherrs.uncC_JESDn00    = GetUncRatio( 'uncC_JESDn00'   , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bJESDown"  )
    grapherrs.uncC_FragUp00   = GetUncRatio( 'uncC_FragUp00'  , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bFragUp"   )
    grapherrs.uncC_FragDn00   = GetUncRatio( 'uncC_FragDn00'  , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bFragDown" )
    grapherrs.uncC_PUUp00     = GetUncRatio( 'uncC_PUUp00'    , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bPUUp"     )
    grapherrs.uncC_PUDn00     = GetUncRatio( 'uncC_PUDn00'    , dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bPUDown"   )
    grapherrs.uncC_bType3Up00 = GetUncRatio( 'uncC_bType3Up00', dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bType3Up"  )
    grapherrs.uncC_bType3Dn00 = GetUncRatio( 'uncC_bType3Dn00', dfSIGNC_bin00, 'renormREQUIRED_wgt_WPbL_central', "renormREQUIRED_wgt_WPbL_bType3Down")


    ofile = ROOT.TFile('scalefactors_and_uncertainties.root', 'recreate')
    grapherrs.WriteAllHists(ofile, writeNORMALIZEDhist=DEBUG_MODE)
    ofile.Close()


    

    
    





    #dfSIGN.Define('WPb_loose_sf_central', [&](


def testfunc_add_btagSF():
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )
    #add_btagSF(used_data_frames)
    mainfunc(used_data_frames)
    exit(0)


if __name__ == "__main__":
    testfunc_add_btagSF()
    import sys
    outHISTname = sys.argv[1]
    test_main_content(outHISTname)
    #import sys
    #from collections import namedtuple
    #inARGs = namedtuple('inARGs', 'dataERA pETAbin jETAbin pPTlow pPThigh')
    #in_args = inARGs(*sys.argv[1:])
    #dataERA = in_args.dataERA
    #pETAbin = int(in_args.pETAbin)
    #jETAbin = int(in_args.jETAbin)
    #pPTlow = float(in_args.pPTlow)
    #pPThigh = float(in_args.pPThigh)
    #### if pPThigh < 0, disable the upper bond of photon pt

    ##dataERA = "UL2016PostVFP"
    ##pETAbin = 0
    ##jETAbin = 0
    ##pPTlow = 200
    ##pPThigh = 220
    ## { return std::vector<float>({190,200,220,250,300,        600,    1000, 9999}); }


