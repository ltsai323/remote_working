#!/usr/bin/env python3
import ROOT
### used for miniAOD v12
DEBUG_MODE = True

import ExternalFileMgr
def info(mesg):
    print(f'i@ {mesg}')

#from makehisto_usefulfunc import UsedDataFrames, histCollection
#from makehisto_usefulfunc import hBDTAll, hBDTAct, hSVmAll, hSVmAct
import makehisto_usefulfunc as frag

DATA_LUMINOSITY = 26.81

def define_and_filter(usedDF: frag.UsedDataFrames, dfCUTfuncs:dict, dfDEFfuncs:dict, rescaleSIGN=False):
    the_data0 = dfCUTfuncs['data'](usedDF.dfSR)
    the_sign0 = dfCUTfuncs['sign'](usedDF.dfsign)
    the_fake0 = dfCUTfuncs['fake'](usedDF.dffake)
    the_side0 = dfCUTfuncs['side'](usedDF.dfSB)

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

    the_data = the_data1
    the_sign = the_sign2
    the_fake = the_fake2
    the_side = the_side1
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


def main_content( usedDF: frag.UsedDataFrames, outputFILE):
    #used_df = define_and_filter(usedDF, dfCUTfuncs, dfDEFfuncs)
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB





    class NameSet:
        def __init__(self, varNAME):
            self.data = f'data_{varNAME}'
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
    h_allgjets.WriteAllHists(f_out, writeNORMALIZEDhist = True)
    f_out.Close()



def test_main_content():
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
    main_content(
        usedDF = used_df,
        outputFILE = 'makehisto.root',
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




if __name__ == "__main__":
    test_main_content()
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

    #main_func(dataERA, pETAbin, jETAbin, pPTlow, pPThigh)

