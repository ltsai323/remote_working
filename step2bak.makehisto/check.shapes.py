#!/usr/bin/env python3
import makehisto_ctagfit_estimateSR as content
import makehisto_usefulfunc as frag
import ROOT
import numpy as np
#DATA_LUMINOSITY = 26.81
DATA_LUMINOSITY = 27.01
import logging
import sys

log = logging.getLogger(__name__)
import makehisto_usefulfunc as frag



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
                self.truthl = f'truthL_{varNAME}_noweight' # no event weight
                self.truthc = f'truthC_{varNAME}_noweight'
                self.truthb = f'truthB_{varNAME}_noweight'
                self.truthsum = f'truthSUM_{varNAME}_noweight'


        names = NameSet(oTAG)
        hists = frag.histCollection()

        def KinematicPlots(dataFRAME, tag):
            setattr(hists, f'kine_{tag}_phopt' , dataFRAME.Histo1D( frag.kPhoPt(tag) ,'photon_pt' , 'event_weight') )
            setattr(hists, f'kine_{tag}_phoeta', dataFRAME.Histo1D( frag.kPhoEta(tag),'photon_eta', 'event_weight') )
            setattr(hists, f'kine_{tag}_phophi', dataFRAME.Histo1D( frag.kPhoPhi(tag),'photon_phi', 'event_weight') )
            setattr(hists, f'kine_{tag}_jetpt' , dataFRAME.Histo1D( frag.kJetPt (tag),'jet_pt'    , 'event_weight') )
            setattr(hists, f'kine_{tag}_jeteta', dataFRAME.Histo1D( frag.kJetEta(tag),'jet_eta'   , 'event_weight') )
            setattr(hists, f'kine_{tag}_jetphi', dataFRAME.Histo1D( frag.kJetPhi(tag),'jet_phi'   , 'event_weight') )
            setattr(hists, f'kine_{tag}_nJet'  , dataFRAME.Histo1D( frag.kNJet  (tag),'jet_multiplicity', 'event_weight') )
        KinematicPlots(dfTruthL, 'truthL')
        KinematicPlots(dfTruthC, 'truthC')
        KinematicPlots(dfTruthB, 'truthB')



        ### all entries
        hists.truthL_BDTAll = dfTruthL.Histo1D( frag.hBDTAll(names.truthL), 'photon_mva', 'event_weight' )
        hists.truthC_BDTAll = dfTruthC.Histo1D( frag.hBDTAll(names.truthC), 'photon_mva', 'event_weight' )
        hists.truthB_BDTAll = dfTruthB.Histo1D( frag.hBDTAll(names.truthB), 'photon_mva', 'event_weight' )
        hists.truthl_BDTAll = dfTruthL.Histo1D( frag.hBDTAll(names.truthl), 'photon_mva')
        hists.truthc_BDTAll = dfTruthC.Histo1D( frag.hBDTAll(names.truthc), 'photon_mva')
        hists.truthb_BDTAll = dfTruthB.Histo1D( frag.hBDTAll(names.truthb), 'photon_mva')

        hists.truthL_btag = dfTruthL.Histo1D( frag.hbtag(names.truthL), 'ParTB', 'event_weight' )
        hists.truthC_btag = dfTruthC.Histo1D( frag.hbtag(names.truthC), 'ParTB', 'event_weight' )
        hists.truthB_btag = dfTruthB.Histo1D( frag.hbtag(names.truthB), 'ParTB', 'event_weight' )
        hists.trughSUM_btag = sum_hist(names.truthSUM + '_btag', hists.truthL_btag, hists.truthC_btag, hists.truthB_btag)
        hists.truthl_btag = dfTruthL.Histo1D( frag.hbtag(names.truthl), 'ParTB')
        hists.truthc_btag = dfTruthC.Histo1D( frag.hbtag(names.truthc), 'ParTB')
        hists.truthb_btag = dfTruthB.Histo1D( frag.hbtag(names.truthb), 'ParTB')
        hists.trughsum_btag = sum_hist(names.truthsum + '_btag', hists.truthl_btag, hists.truthc_btag, hists.truthb_btag)

        hists.truthL_cvsb = dfTruthL.Histo1D( frag.hcvsb(names.truthL), 'ParTCvsB', 'event_weight' )
        hists.truthC_cvsb = dfTruthC.Histo1D( frag.hcvsb(names.truthC), 'ParTCvsB', 'event_weight' )
        hists.truthB_cvsb = dfTruthB.Histo1D( frag.hcvsb(names.truthB), 'ParTCvsB', 'event_weight' )
        hists.trughSUM_cvsb = sum_hist(names.truthSUM + '_cvsb', hists.truthL_cvsb, hists.truthC_cvsb, hists.truthB_cvsb)
        hists.truthl_cvsb = dfTruthL.Histo1D( frag.hcvsb(names.truthl), 'ParTCvsB')
        hists.truthc_cvsb = dfTruthC.Histo1D( frag.hcvsb(names.truthc), 'ParTCvsB')
        hists.truthb_cvsb = dfTruthB.Histo1D( frag.hcvsb(names.truthb), 'ParTCvsB')
        hists.trughsum_cvsb = sum_hist(names.truthsum + '_cvsb', hists.truthl_cvsb, hists.truthc_cvsb, hists.truthb_cvsb)

        hists.truthL_cvsl = dfTruthL.Histo1D( frag.hcvsl(names.truthL), 'ParTCvsL', 'event_weight' )
        hists.truthC_cvsl = dfTruthC.Histo1D( frag.hcvsl(names.truthC), 'ParTCvsL', 'event_weight' )
        hists.truthB_cvsl = dfTruthB.Histo1D( frag.hcvsl(names.truthB), 'ParTCvsL', 'event_weight' )
        hists.trughSUM_cvsl = sum_hist(names.truthSUM + '_cvsl', hists.truthL_cvsl, hists.truthC_cvsl, hists.truthB_cvsl)
        hists.truthl_cvsl = dfTruthL.Histo1D( frag.hcvsl(names.truthl), 'ParTCvsL')
        hists.truthc_cvsl = dfTruthC.Histo1D( frag.hcvsl(names.truthc), 'ParTCvsL')
        hists.truthb_cvsl = dfTruthB.Histo1D( frag.hcvsl(names.truthb), 'ParTCvsL')
        hists.trughsum_cvsl = sum_hist(names.truthsum + '_cvsl', hists.truthl_cvsl, hists.truthc_cvsl, hists.truthb_cvsl)


        hists.truthL2D_ctag = dfTruthL.Histo2D( frag.h2DcvsbANDcvsl(names.truthL), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.truthC2D_ctag = dfTruthC.Histo2D( frag.h2DcvsbANDcvsl(names.truthC), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.truthB2D_ctag = dfTruthB.Histo2D( frag.h2DcvsbANDcvsl(names.truthB), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.trughSUM2D_ctag = sum_hist(names.truthSUM + '_cvsbANDcvsl', hists.truthL2D_ctag, hists.truthC2D_ctag, hists.truthB2D_ctag)
        hists.truthl2D_ctag = dfTruthL.Histo2D( frag.h2DcvsbANDcvsl(names.truthl), 'ParTCvsB', 'ParTCvsL')
        hists.truthc2D_ctag = dfTruthC.Histo2D( frag.h2DcvsbANDcvsl(names.truthc), 'ParTCvsB', 'ParTCvsL')
        hists.truthb2D_ctag = dfTruthB.Histo2D( frag.h2DcvsbANDcvsl(names.truthb), 'ParTCvsB', 'ParTCvsL')
        hists.trughsum2D_ctag = sum_hist(names.truthsum + '_cvsbANDcvsl', hists.truthl2D_ctag, hists.truthc2D_ctag, hists.truthb2D_ctag)





        #hists.truthNOWGTL_BDTAll = dfTruthL.Histo1D( frag.hNOWGTBDTAll(names.truthL), 'photon_mva')
        #hists.truthNOWGTC_BDTAll = dfTruthC.Histo1D( frag.hNOWGTBDTAll(names.truthC), 'photon_mva')
        #hists.truthNOWGTB_BDTAll = dfTruthB.Histo1D( frag.hNOWGTBDTAll(names.truthB), 'photon_mva')

        #hists.truthNOWGTL_btag = dfTruthL.Histo1D( frag.hNOWGTbtag(names.truthL), 'ParTB')
        #hists.truthNOWGTC_btag = dfTruthC.Histo1D( frag.hNOWGTbtag(names.truthC), 'ParTB')
        #hists.truthNOWGTB_btag = dfTruthB.Histo1D( frag.hNOWGTbtag(names.truthB), 'ParTB')
        #hists.trughNOWGTSUM_btag = sum_hist(names.truthSUM + '_btag_NO_EVT_WEIGHT', hists.truthNOWGTL_btag, hists.truthNOWGTC_btag, hists.truthNOWGTB_btag)

        #hists.truthNOWGTL_cvsb = dfTruthL.Histo1D( frag.hNOWGTcvsb(names.truthL), 'ParTCvsB')
        #hists.truthNOWGTC_cvsb = dfTruthC.Histo1D( frag.hNOWGTcvsb(names.truthC), 'ParTCvsB')
        #hists.truthNOWGTB_cvsb = dfTruthB.Histo1D( frag.hNOWGTcvsb(names.truthB), 'ParTCvsB')
        #hists.trughNOWGTSUM_cvsb = sum_hist(names.truthSUM + '_cvsb_NO_EVT_WEIGHT', hists.truthNOWGTL_cvsb, hists.truthNOWGTC_cvsb, hists.truthNOWGTB_cvsb)

        #hists.truthNOWGTL_cvsl = dfTruthL.Histo1D( frag.hNOWGTcvsl(names.truthL), 'ParTCvsL')
        #hists.truthNOWGTC_cvsl = dfTruthC.Histo1D( frag.hNOWGTcvsl(names.truthC), 'ParTCvsL')
        #hists.truthNOWGTB_cvsl = dfTruthB.Histo1D( frag.hNOWGTcvsl(names.truthB), 'ParTCvsL')
        #hists.trughNOWGTSUM_cvsl = sum_hist(names.truthSUM + '_cvsl_NO_EVT_WEIGHT', hists.truthNOWGTL_cvsl, hists.truthNOWGTC_cvsl, hists.truthNOWGTB_cvsl)

        return hists




    h_allgjets = plot_all_vars(
            'gjet',
            the_data,
    )

    data_BDT = the_data.Histo1D( frag.hBDTAll('data_gjet'), 'photon_mva', 'event_weight' )
    databtag = the_data.Histo1D( frag.hbtag  ('data_gjet'), 'ParTB'     , 'event_weight' )
    datacvsb = the_data.Histo1D( frag.hcvsb  ('data_gjet'), 'ParTCvsB'  , 'event_weight' )
    datacvsl = the_data.Histo1D( frag.hcvsl  ('data_gjet'), 'ParTCvsL'  , 'event_weight' )
    data2D_ctag = the_data.Histo2D( frag.h2DcvsbANDcvsl('data_gjet'), 'ParTCvsB', 'ParTCvsL'  , 'event_weight' )

    fake_BDT = the_side.Histo1D( frag.hBDTAll('fake_gjet'), 'photon_mva', 'event_weight' )
    fakebtag = the_side.Histo1D( frag.hbtag  ('fake_gjet'), 'ParTB'     , 'event_weight' )
    fakecvsb = the_side.Histo1D( frag.hcvsb  ('fake_gjet'), 'ParTCvsB'  , 'event_weight' )
    fakecvsl = the_side.Histo1D( frag.hcvsl  ('fake_gjet'), 'ParTCvsL'  , 'event_weight' )
    fake2D_ctag = the_side.Histo2D( frag.h2DcvsbANDcvsl('fake_gjet'), 'ParTCvsB', 'ParTCvsL'  , 'event_weight' )



    ### sideband as fake (di-jet)
    hists_fake = frag.histCollection()
    hists_fake.BDT  = the_side.Histo1D( frag.hBDTAll('truthfake'), 'photon_mva', 'event_weight' )
    hists_fake.btag = the_side.Histo1D( frag.hbtag  ('truthfake'), 'ParTB'     , 'event_weight' )
    hists_fake.cvsb = the_side.Histo1D( frag.hcvsb  ('truthfake'), 'ParTCvsB'  , 'event_weight' )
    hists_fake.cvsl = the_side.Histo1D( frag.hcvsl  ('truthfake'), 'ParTCvsL'  , 'event_weight' )
    hists_fake.cvsl = the_side.Histo1D( frag.hcvsl  ('truthfake'), 'ParTCvsL'  , 'event_weight' )
    hists_fake.ctag = the_side.Histo2D( frag.h2DcvsbANDcvsl('truthfake'), 'ParTCvsB', 'ParTCvsL'  , 'event_weight' )
    if hists_fake.BDT.Integral() > 1e-8: # scale fake to 0.1 * all gjet to get a psuedo data
        scale_to_data = 0.1 * data_BDT.Integral() / fake_BDT.Integral()
        hists_fake.BDT .Scale( scale_to_data )
        hists_fake.btag.Scale( scale_to_data )
        hists_fake.cvsb.Scale( scale_to_data )
        hists_fake.cvsl.Scale( scale_to_data )
        hists_fake.ctag.Scale( scale_to_data )

    hists_fake.NOWGT_BDT = the_side.Histo1D( frag.hNOWGTBDTAll('truthfake'), 'photon_mva')
    hists_fake.NOWGTbtag = the_side.Histo1D( frag.hNOWGTbtag  ('truthfake'), 'ParTB'     )
    hists_fake.NOWGTcvsb = the_side.Histo1D( frag.hNOWGTcvsb  ('truthfake'), 'ParTCvsB'  )
    hists_fake.NOWGTcvsl = the_side.Histo1D( frag.hNOWGTcvsl  ('truthfake'), 'ParTCvsL'  )

    hists_pull_test = frag.histCollection()

    #def create_psuedodata(theVAR, newHISTname):
    #    def create_toy(hist, histNOWGT): # Treat every bin as a compound poisson distribution
    #        newhist = hist.Clone(hist.GetName()+"_toy")

    #        for binidx in range(hist.GetNbinsX()):
    #            binIdx = binidx+1
    #            bin_content = hist.GetBinContent(binIdx)
    #            bin_error   = hist.GetBinError  (binIdx)
    #            if bin_content < 1e-8:
    #                newhist.SetBinContent(binIdx, 0)
    #                newhist.SetBinError  (binIdx, 0)
    #                continue

    #            mu = bin_content
    #            #N_event = int( ( bin_content / bin_error )**2 )
    #            N_events = ( bin_content / bin_error )**2

    #            mean_weight = mu / float(N_events)   # mean weight
    #            s2 = mu * mean_weight                # approximate variance ~ mu * mean weight
    #            lam_tilde = mu**2 / s2               # SPD poisson parameter
    #            scale = s2 / mu                      # SPD scale factor

    #            toy_data = np.random.poisson(lam_tilde, 1) * scale # generate toy data

    #            newhist.SetBinContent(binIdx, toy_data[0])
    #            newhist.SetBinError  (binIdx, s2**0.5)
    #        return newhist


    #    truthL      = getattr(h_allgjets, f'truthL_{theVAR}')
    #    truthNOWGTL = getattr(h_allgjets, f'truthNOWGTL_{theVAR}')
    #    toyL        = create_toy(truthL, truthNOWGTL)
    #    truthC      = getattr(h_allgjets, f'truthC_{theVAR}')
    #    truthNOWGTC = getattr(h_allgjets, f'truthNOWGTC_{theVAR}')
    #    toyC        = create_toy(truthC, truthNOWGTC)
    #    truthB      = getattr(h_allgjets, f'truthB_{theVAR}')
    #    truthNOWGTB = getattr(h_allgjets, f'truthNOWGTB_{theVAR}')
    #    toyB        = create_toy(truthB, truthNOWGTB)

    #    fake      = getattr(hists_fake, f'{theVAR}')
    #    fakeNOWGT = getattr(hists_fake, f'NOWGT{theVAR}')

    #    toyF      = create_toy(fake, fakeNOWGT)

    #    toyF.Add(toyL)
    #    toyF.Add(toyC)
    #    toyF.Add(toyB)
    #    toyF.SetName(newHISTname)
    #    return toyF


    #for pullIdx in range(1000):
    #    setattr( hists_pull_test, f'data_gjet_cvsl_{pullIdx}', create_psuedodata('cvsl', f'data_gjet_cvsl_{pullIdx}') )
    #    setattr( hists_pull_test, f'data_gjet_btag_{pullIdx}', create_psuedodata('btag', f'data_gjet_btag_{pullIdx}') )
    #    setattr( hists_pull_test, f'data_gjet_cvsb_{pullIdx}', create_psuedodata('cvsb', f'data_gjet_cvsb_{pullIdx}') )



    hists_mergefake = frag.histCollection()
    def mergefake_hists(addTAG, addNUM):
        def merge_fake(addTAG, hDATA, hSIDE, addNUM):
            hfake = hSIDE.Clone(f'{hSIDE.GetName()}_{addTAG}')
            fakeINTEGRAL = hfake.Integral()
            if fakeINTEGRAL != 0:
                hfake.Scale( addNUM / hfake.Integral() )

            hdata = hDATA.Clone(f'{hDATA.GetName()}_{addTAG}')
            hdata.Add(hfake)
            setattr(hists_mergefake, hfake.GetName(), hfake)
            setattr(hists_mergefake, hdata.GetName(), hdata)
        merge_fake(addTAG, data_BDT, fake_BDT, addNUM)
        merge_fake(addTAG, databtag, fakebtag, addNUM)
        merge_fake(addTAG, datacvsl, fakecvsl, addNUM)
        merge_fake(addTAG, datacvsb, fakecvsb, addNUM)
        merge_fake(addTAG, data2D_ctag, fake2D_ctag, addNUM)
    data_integral = data_BDT.Integral()
    rnd = ROOT.TRandom3()
    idx = 0

    merged_val = data_integral * 0.2
    mergefake_hists(f'0', data_integral * 0.00000001)
    mergefake_hists(f'1', data_integral * 0.1)
    mergefake_hists(f'2', data_integral * 0.2)
    mergefake_hists(f'3', data_integral * 0.5)
    mergefake_hists(f'4', data_integral * 1.0)

    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'update')
    h_allgjets.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    hists_mergefake.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    #hists_pull_test.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    hists_fake.WriteAllHists(f_out, writeNORMALIZEDhist = False)
    f_out.Close()

def check_shape(dataFRAME, fOUTname):
    df = dataFRAME
    hists = frag.histCollection()

    hists.photon_pt                   = df.Histo1D( ('phopt'        , '',150,   0,1500), 'photon_pt'                  , 'event_weight')
    hists.photon_eta                  = df.Histo1D( ('phoeta'       , '', 40,-3.5, 3.5), 'photon_eta'                 , 'event_weight')
    hists.photon_phi                  = df.Histo1D( ('phophi'       , '', 40,-3.5, 3.5), 'photon_phi'                 , 'event_weight')
    hists.photon_mva                  = df.Histo1D( ('phomva'       , '', 40,   0,   1), 'photon_mva'                 , 'event_weight')
    hists.photon_sieie                = df.Histo1D( ('phosieie'     , '', 40,   0,0.03), 'photon_sieie'               , 'event_weight')
    hists.photon_hoe                  = df.Histo1D( ('phohoe'       , '', 40,   0,0.05), 'photon_hoe'                 , 'event_weight')
    hists.photon_pfChargedIsoWorstVtx = df.Histo1D( ('phochIsoWorst', '', 40,   0,  10), 'photon_pfChargedIsoWorstVtx', 'event_weight')
    hists.photon_pfChargedIsoPFPV     = df.Histo1D( ('phochIso'     , '', 40,   0,   2), 'photon_pfChargedIsoPFPV'    , 'event_weight')
    hists.jet_pt                      = df.Histo1D( ('jetpt'        , '',150,   0,1500), 'jet_pt'                     , 'event_weight')
    hists.jet_eta                     = df.Histo1D( ('jeteta'       , '', 40,-3.5, 3.5), 'jet_eta'                    , 'event_weight')
    hists.jet_phi                     = df.Histo1D( ('jetphi'       , '', 40,-3.5, 3.5), 'jet_phi'                    , 'event_weight')
    hists.jet_multiplicity            = df.Histo1D( ('njet'         , '', 15,   0,  15), 'jet_multiplicity'           , 'event_weight')
    hists.jet_nSV                     = df.Histo1D( ('jetnSV'       , '',  8,   0,   8), 'jet_nSV'                    , 'event_weight')
    hists.jet_SVmass                  = df.Histo1D( ('jetSVmass'    , '', 40,   0,   5), 'jet_SVmass'                 , 'event_weight')
    hists.jet_SVpt                    = df.Histo1D( ('jetSVpt'      , '', 80,   0, 800), 'jet_SVpt'                   , 'event_weight')
    hists.jet_SVdr                    = df.Histo1D( ('jetSVdr'      , '', 40,   0, 0.3), 'jet_SVdr'                   , 'event_weight')
    hists.jet_SVntracks               = df.Histo1D( ('jetSVntrack'  , '', 18,   0,  18), 'jet_SVntracks'              , 'event_weight')
    hists.MET                         = df.Histo1D( ('MET'          , '', 40,   0, 500), 'MET'                        , 'event_weight')
    hists.GenPhoton_pt                = df.Histo1D( ('genphopt'     , '',150,   0,1500), 'GenPhoton_pt'               , 'event_weight')
    hists.GenPhoton_eta               = df.Histo1D( ('genphoeta'    , '', 40,-3.5, 3.5), 'GenPhoton_eta'              , 'event_weight')
    hists.GenPhoton_phi               = df.Histo1D( ('genphophi'    , '', 40,-3.5, 3.5), 'GenPhoton_phi'              , 'event_weight')
    hists.photon_mva_orig             = df.Histo1D( ('phomvaorig'   , '', 40,   0,   1), 'photon_mva_orig'            , 'event_weight')
    hists.PNetB                       = df.Histo1D( ('PNetB'        , '', 40,   0,   1), 'PNetB'                      , 'event_weight')
    hists.PNetCvsB                    = df.Histo1D( ('PNetCvsB'     , '', 40,   0,   1), 'PNetCvsB'                   , 'event_weight')
    hists.PNetCvsL                    = df.Histo1D( ('PNetCvsL'     , '', 40,   0,   1), 'PNetCvsL'                   , 'event_weight')
    hists.ParTB                       = df.Histo1D( ('ParTB'        , '', 40,   0,   1), 'ParTB'                      , 'event_weight')
    hists.ParTCvsB                    = df.Histo1D( ('ParTCvsB'     , '', 40,   0,   1), 'ParTCvsB'                   , 'event_weight')
    hists.ParTCvsL                    = df.Histo1D( ('ParTCvsL'     , '', 40,   0,   1), 'ParTCvsL'                   , 'event_weight')
    hists.DeepFlavourB                = df.Histo1D( ('DeepFlvrB'    , '', 40,   0,   1), 'DeepFlavourB'               , 'event_weight')
    hists.DeepFlavourCvsB             = df.Histo1D( ('DeepFlvrCvsB' , '', 40,   0,   1), 'DeepFlavourCvsB'            , 'event_weight')
    hists.DeepFlavourCvsL             = df.Histo1D( ('DeepFlvrCvsL' , '', 40,   0,   1), 'DeepFlavourCvsL'            , 'event_weight')


    log.info(f'[WriteHistToFile] output file {fOUTname}')
    fOUT = ROOT.TFile(fOUTname, 'recreate')
    hists.WriteAllHists(fOUT, writeNORMALIZEDhist=False, writeOVERFLOWbin=True)
    fOUT.Close()
    log.info(f'[WriteHistToFile] all related histograms written')

def main_function(
    iFILEmadgraph, iFILEpythia, iFILEfake,
    oFILEname, additionalCUT=1
    ):


    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            dataFILE = iFILEpythia,
            signFILE = iFILEmadgraph,
            fakeFILE = iFILEfake,
            )


    ### define eventweight from MC
    defineFUNCmc = lambda df: df.Define('event_weight', f'wgt * {DATA_LUMINOSITY}') # gen weight, xs norm, PU weight, photon SF, trigger SF
    cut_func = {
            'data': lambda df: df.Filter(additionalCUT),
            'sign': lambda df: df.Filter(additionalCUT),
            'fake': lambda df: df.Filter(additionalCUT),
            'side': lambda df: df,
    }
    def_func = {
            'data': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df,
    }
    used_df = content.define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    # from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc
    # CreateJetPtSF_toTH1(used_df, 9,9,99,99)

    # ### update event weight using JetPt-PhoPt-nJet SF
    # LoadAdditionalFunc()
    # ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign,9,9,99,99, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF
    # used_df.dfsign = ddd

    check_shape(used_df.dfSR  , 'check.shape.PythiaFlat.root')
    check_shape(used_df.dfsign, 'check.shape.Madgraph.root')





if __name__ == "__main__":
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
            format='[GJetPythiaFlatPsuedodata_ctagfit_estimateSR] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')


    outfile = 'check.shapes.root'
    additionalCUT = sys.argv[1]

    ifile_madgraph = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root'
    ifile_pythia   = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root'
    ifile_fake     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root'

    main_function(ifile_madgraph,ifile_pythia,ifile_fake, outfile,additionalCUT)
    


    #content.main_content(
    #    usedDF = used_df,
    #    outputFILE = outfile
    #)
    #update_truth(
    #        usedDF = used_df,
    #        outputFILE = outfile
    #        )

    #print(f'[OutputFile] {outfile}')
