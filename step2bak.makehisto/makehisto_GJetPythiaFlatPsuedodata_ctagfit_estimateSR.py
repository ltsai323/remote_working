#!/usr/bin/env python3
import makehisto_ctagfit_estimateSR as content
import makehisto_usefulfunc as frag
import ROOT
DATA_LUMINOSITY = 26.81

def update_truth( usedDF: frag.UsedDataFrames, outputFILE):
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB





    ############# ploting ################
    def sum_hist(newTITLE, h1, *addHISTs):
        h = h1.Clone(newTITLE)
        for add_hist in addHISTs:
            h.Add(add_hist.GetValue())
        return h

    def plot_all_vars(oTAG, dfDATA):
        df_data = content.DefineJetTruth(dfDATA)
        dfTruthL = df_data.Filter('isLJet')
        dfTruthC = df_data.Filter('isCJet')
        dfTruthB = df_data.Filter('isBJet')

        class NameSet:
            def __init__(self, varNAME):
                self.truthL = f'truthL_{varNAME}'
                self.truthC = f'truthC_{varNAME}'
                self.truthB = f'truthB_{varNAME}'
                self.truthSUM = f'truthSUM_{varNAME}'


        names = NameSet(oTAG)
        hists = frag.histCollection()



        ### all entries
        hists.truthL_BDTAll = dfTruthL.Histo1D( frag.hBDTAll(names.truthL), 'photon_mva', 'event_weight' )
        hists.truthC_BDTAll = dfTruthC.Histo1D( frag.hBDTAll(names.truthC), 'photon_mva', 'event_weight' )
        hists.truthB_BDTAll = dfTruthB.Histo1D( frag.hBDTAll(names.truthB), 'photon_mva', 'event_weight' )

        hists.truthL_btag = dfTruthL.Histo1D( frag.hbtag(names.truthL), 'ParTB', 'event_weight' )
        hists.truthC_btag = dfTruthC.Histo1D( frag.hbtag(names.truthC), 'ParTB', 'event_weight' )
        hists.truthB_btag = dfTruthB.Histo1D( frag.hbtag(names.truthB), 'ParTB', 'event_weight' )
        hists.trughSUM_btag = sum_hist(names.truthSUM + '_btag', hists.truthL_btag, hists.truthC_btag, hists.truthB_btag)

        hists.truthL_cvsb = dfTruthL.Histo1D( frag.hcvsb(names.truthL), 'ParTCvsB', 'event_weight' )
        hists.truthC_cvsb = dfTruthC.Histo1D( frag.hcvsb(names.truthC), 'ParTCvsB', 'event_weight' )
        hists.truthB_cvsb = dfTruthB.Histo1D( frag.hcvsb(names.truthB), 'ParTCvsB', 'event_weight' )
        hists.trughSUM_cvsb = sum_hist(names.truthSUM + '_cvsb', hists.truthL_cvsb, hists.truthC_cvsb, hists.truthB_cvsb)

        hists.truthL_cvsl = dfTruthL.Histo1D( frag.hcvsl(names.truthL), 'ParTCvsL', 'event_weight' )
        hists.truthC_cvsl = dfTruthC.Histo1D( frag.hcvsl(names.truthC), 'ParTCvsL', 'event_weight' )
        hists.truthB_cvsl = dfTruthB.Histo1D( frag.hcvsl(names.truthB), 'ParTCvsL', 'event_weight' )
        hists.trughSUM_cvsl = sum_hist(names.truthSUM + '_cvsl', hists.truthL_cvsl, hists.truthC_cvsl, hists.truthB_cvsl)

        return hists
    



    h_allgjets = plot_all_vars(
            'gjet',
            the_data,
    )

    data_BDT = the_data.Histo1D( frag.hBDTAll('data_gjet'), 'photon_mva', 'event_weight' )
    databtag = the_data.Histo1D( frag.hbtag  ('data_gjet'), 'ParTB'     , 'event_weight' )
    datacvsb = the_data.Histo1D( frag.hcvsb  ('data_gjet'), 'ParTCvsB'  , 'event_weight' )
    datacvsl = the_data.Histo1D( frag.hcvsl  ('data_gjet'), 'ParTCvsL'  , 'event_weight' )

    fake_BDT = the_side.Histo1D( frag.hBDTAll('fake_gjet'), 'photon_mva', 'event_weight' )
    fakebtag = the_side.Histo1D( frag.hbtag  ('fake_gjet'), 'ParTB'     , 'event_weight' )
    fakecvsb = the_side.Histo1D( frag.hcvsb  ('fake_gjet'), 'ParTCvsB'  , 'event_weight' )
    fakecvsl = the_side.Histo1D( frag.hcvsl  ('fake_gjet'), 'ParTCvsL'  , 'event_weight' )

    hists_mergefake = frag.histCollection()
    def mergefake_hists(addTAG, addNUM):
        def merge_fake(addTAG, hDATA, hSIDE, addNUM):
            hfake = hSIDE.Clone(f'{hSIDE.GetName()}_{addTAG}')
            hfake.Scale( addNUM / hfake.Integral() )
            
            hdata = hDATA.Clone(f'{hDATA.GetName()}_{addTAG}')
            hdata.Add(hfake)
            setattr(hists_mergefake, hfake.GetName(), hfake)
            setattr(hists_mergefake, hdata.GetName(), hdata)
        merge_fake(addTAG, data_BDT, fake_BDT, addNUM)
        merge_fake(addTAG, databtag, fakebtag, addNUM)
        merge_fake(addTAG, datacvsl, fakecvsl, addNUM)
        merge_fake(addTAG, datacvsb, fakecvsb, addNUM)
    data_integral = data_BDT.Integral()
    rnd = ROOT.TRandom3()
    idx = 0

    merged_val = data_integral * 0.2
    mergefake_hists(f'0', data_integral * 0.01)
    mergefake_hists(f'1', data_integral * 0.1)
    mergefake_hists(f'2', data_integral * 0.2)
    mergefake_hists(f'3', data_integral * 0.5)
    mergefake_hists(f'4', data_integral * 1.0)

    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'update')
    h_allgjets.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    hists_mergefake.WriteAllHists(f_out, writeNORMALIZEDhist = False)
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
