#!/usr/bin/env python3
import makehisto_content_estimateSR as content
import makehisto_usefulfunc as frag
import ROOT
DATA_LUMINOSITY = 26.81

def update_truth( usedDF: frag.UsedDataFrames, outputFILE, writeOVERFLOWbin=False):
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB





    ############# ploting ################
    #hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 42, -1, 8 )
    #hBDTAll = lambda tag: ( f'{tag}_BDTAll', 'BDT Score', 40, -1.,1.)

    #hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 32, 0, 8 )
    #hBDTAct = lambda tag: ( f'{tag}_BDTAct', 'BDT Score with SV constructed', 40, -1.,1.)
    class NameSet:
        def __init__(self, varNAME):
            self.truthL = f'data_{varNAME}_truthL'
            self.truthC = f'data_{varNAME}_truthC'
            self.truthB = f'data_{varNAME}_truthB'
            self.truthSUM = f'data_{varNAME}_truthSUM'



    def plot_all_vars(oTAG, dfDATA):
        df_data = content.DefineJetTruth(dfDATA)
        dfTruthL = df_data.Filter('isLJet')
        dfTruthC = df_data.Filter('isCJet')
        dfTruthB = df_data.Filter('isBJet')

        names = NameSet(oTAG)
        hists = frag.histCollection()

        def sum_hist(newTITLE, h1, h2, h3 ):
            h = h1.Clone(newTITLE)
            h.Add(h2.GetValue())
            h.Add(h3.GetValue())
            return h


        ### all entries
        hists.truthL_BDTAll = dfTruthL.Histo1D( frag.hBDTAll(names.truthL), 'photon_mva', 'event_weight' )
        hists.truthC_BDTAll = dfTruthC.Histo1D( frag.hBDTAll(names.truthC), 'photon_mva', 'event_weight' )
        hists.truthB_BDTAll = dfTruthB.Histo1D( frag.hBDTAll(names.truthB), 'photon_mva', 'event_weight' )
        hists.trughSUM_BDTAll = sum_hist(names.truthSUM + '_BDTAll', hists.truthL_BDTAll, hists.truthC_BDTAll, hists.truthB_BDTAll)

        hists.truthL_SVmAll = dfTruthL.Histo1D( frag.hSVmAll(names.truthL), 'jet_SVmass', 'event_weight' )
        hists.truthC_SVmAll = dfTruthC.Histo1D( frag.hSVmAll(names.truthC), 'jet_SVmass', 'event_weight' )
        hists.truthB_SVmAll = dfTruthB.Histo1D( frag.hSVmAll(names.truthB), 'jet_SVmass', 'event_weight' )
        hists.trughSUM_SVmAll = sum_hist(names.truthSUM + '_SVmAll', hists.truthL_SVmAll, hists.truthC_SVmAll, hists.truthB_SVmAll)

        if frag.cutWPcANDfitbTag:
            hists.truthL_btag = dfTruthL.Histo1D( frag.hbtag(names.truthL), 'ParTB', 'event_weight' )
            hists.truthC_btag = dfTruthC.Histo1D( frag.hbtag(names.truthC), 'ParTB', 'event_weight' )
            hists.truthB_btag = dfTruthB.Histo1D( frag.hbtag(names.truthB), 'ParTB', 'event_weight' )
            hists.trughSUM_btag = sum_hist(names.truthSUM + '_btag', hists.truthL_btag, hists.truthC_btag, hists.truthB_btag)


        if frag.cutWPANDfitSVMass:
            ### only record the jet_SVmass activated distributions
            dftruthl = dfTruthL.Filter('jet_SVmass>0')
            dftruthc = dfTruthC.Filter('jet_SVmass>0')
            dftruthb = dfTruthB.Filter('jet_SVmass>0')

            hists.truthL_BDTAct = dfTruthL.Histo1D( frag.hBDTAct(names.truthL), 'photon_mva', 'event_weight' )
            hists.truthC_BDTAct = dfTruthC.Histo1D( frag.hBDTAct(names.truthC), 'photon_mva', 'event_weight' )
            hists.truthB_BDTAct = dfTruthB.Histo1D( frag.hBDTAct(names.truthB), 'photon_mva', 'event_weight' )

            hists.truthL_SVmAct = dfTruthL.Histo1D( frag.hSVmAct(names.truthL), 'jet_SVmass', 'event_weight' )
            hists.truthC_SVmAct = dfTruthC.Histo1D( frag.hSVmAct(names.truthC), 'jet_SVmass', 'event_weight' )
            hists.truthB_SVmAct = dfTruthB.Histo1D( frag.hSVmAct(names.truthB), 'jet_SVmass', 'event_weight' )
            hists.truthSUM_SVmAct = sum_hist(names.truthSUM + '_SVmAct', hists.truthL_SVmAct, hists.truthC_SVmAct, hists.truthB_SVmAct)




        return hists



    h_allgjets = plot_all_vars(
            'allgjets',
            the_data,
    )
    if frag.cutWPANDfitSVMass:
        h_WPbLoose = plot_all_vars(
                'WPbLoose',
                the_data.Filter('WPb_loose'),
        )
        h_WPbMedium = plot_all_vars(
                'WPbMedium',
                the_data.Filter('WPb_medium'),
        )
        h_WPbTight = plot_all_vars(
                'WPbTight',
                the_data.Filter('WPb_tight'),
        )
    h_WPcLoose  = plot_all_vars(
            'WPcLoose',
            the_data.Filter('WPc_loose'),
    )
    h_WPcMedium = plot_all_vars(
            'WPcMedium',
            the_data.Filter('WPc_medium'),
    )
    h_WPcTight = plot_all_vars(
            'WPcTight',
            the_data.Filter('WPc_tight'),
    )
    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'update')
    h_allgjets.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    if frag.cutWPANDfitSVMass:
        h_WPbLoose.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
        h_WPbMedium.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
        h_WPbTight.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPcLoose.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPcMedium.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPcTight.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    f_out.Close()




if __name__ == "__main__":
    import sys

    outfile = sys.argv[1] if len(sys.argv) > 1 else 'makehisto_psuedodata_rescaled.root'
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            #dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )

    #### redefine the histogram
    #frag.hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
    #frag.hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )




    #binning = 'photon_pt>210 && photon_pt<230 && abs(jet_eta)<1.5 && abs(photon_eta)<1.5'
    binning = 'photon_pt>210'
    cut_func = {
            'data': lambda df: df.Filter(f'{binning} && 1'),
            'sign': lambda df: df.Filter(f'{binning} && 1'),
            'fake': lambda df: df.Filter(f'{binning} && 1'),
            'side': lambda df: df.Filter(f'{binning} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = content.define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    content.main_content(
        usedDF = used_df,
        outputFILE = outfile
    )
    update_truth(
            usedDF = used_df,
            outputFILE = outfile
            )

    print(f'[OutputFile] {outfile}')
