#!/usr/bin/env python3
import ROOT
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc, Define_NormalizeBTagSF
import makehisto_usefulfunc as extfunc
### used for miniAOD v12
import logging
import sys
DEBUG_MODE = False

log = logging.getLogger(__name__)


import ExternalFileMgr

#from makehisto_usefulfunc import UsedDataFrames, histCollection
#from makehisto_usefulfunc import hBDTAll, hBDTAct, hSVmAll, hSVmAct
import makehisto_usefulfunc as frag

#DATA_LUMINOSITY = 26.81 # 2022EE
DATA_LUMINOSITY = 27.01 # 2022EE


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
        def __init__(self, oTAG):
            self.data = f'data_{oTAG}'
            self.gjet = f'gjet_{oTAG}'
            self.sigL = f'sigL_{oTAG}'
            self.sigC = f'sigC_{oTAG}'
            self.sigB = f'sigB_{oTAG}'
            self.fake = f'fake_{oTAG}'
            self.side = f'side_{oTAG}' # data sideband

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
        def __init__(self, oTAG):
            self.data = f'data_{oTAG}'
            self.gjet = f'gjet_{oTAG}'
            self.sigL = f'sigL_{oTAG}'
            self.sigC = f'sigC_{oTAG}'
            self.sigB = f'sigB_{oTAG}'
            self.fake = f'fake_{oTAG}'
            self.side = f'side_{oTAG}' # data sideband
            self.gJET = f'gjet_{oTAG}_noweight'
            self.sigl = f'sigL_{oTAG}_noweight'
            self.sigc = f'sigC_{oTAG}_noweight'
            self.sigb = f'sigB_{oTAG}_noweight'
            self.ogjet = f'gjet_{oTAG}_origweight'
            self.osigl = f'sigL_{oTAG}_origweight'
            self.osigc = f'sigC_{oTAG}_origweight'
            self.osigb = f'sigB_{oTAG}_origweight'

            #print(f'[NameSet] Generating histograms: {self.data} {self.sign} {self.fake} {self.stak} {self.diff}')



    def plot_all_vars(oTAG, dfDATA, dfSIGN, dfFAKE, dfSIDE):
        dfSigL = dfSIGN.Filter('isLJet')
        dfSigC = dfSIGN.Filter('isCJet')
        dfSigB = dfSIGN.Filter('isBJet')

        names = NameSet(oTAG)
        hists = frag.histCollection()
        def KinematicPlotsORIG(dataFRAME, tag):
            draw_orig_hist = True if 'event_weight_orig' in dfSIGN.GetColumnNames() else False
            if draw_orig_hist:
                setattr(hists, f'kine_{tag}_phopt' , dataFRAME.Histo1D( frag.kPhoPt (tag),'photon_pt' , 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_phoeta', dataFRAME.Histo1D( frag.kPhoEta(tag),'photon_eta', 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_phophi', dataFRAME.Histo1D( frag.kPhoPhi(tag),'photon_phi', 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_jetpt' , dataFRAME.Histo1D( frag.kJetPt (tag),'jet_pt'    , 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_jeteta', dataFRAME.Histo1D( frag.kJetEta(tag),'jet_eta'   , 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_jetphi', dataFRAME.Histo1D( frag.kJetPhi(tag),'jet_phi'   , 'event_weight_orig') )
                setattr(hists, f'kine_{tag}_nJet'  , dataFRAME.Histo1D( frag.kNJet  (tag),'jet_multiplicity', 'event_weight_orig') )
        def KinematicPlots(dataFRAME, tag):
            setattr(hists, f'kine_{tag}_phopt' , dataFRAME.Histo1D( frag.kPhoPt (tag),'photon_pt' , 'event_weight') )
            setattr(hists, f'kine_{tag}_phoeta', dataFRAME.Histo1D( frag.kPhoEta(tag),'photon_eta', 'event_weight') )
            setattr(hists, f'kine_{tag}_phophi', dataFRAME.Histo1D( frag.kPhoPhi(tag),'photon_phi', 'event_weight') )
            setattr(hists, f'kine_{tag}_jetpt' , dataFRAME.Histo1D( frag.kJetPt (tag),'jet_pt'    , 'event_weight') )
            setattr(hists, f'kine_{tag}_jeteta', dataFRAME.Histo1D( frag.kJetEta(tag),'jet_eta'   , 'event_weight') )
            setattr(hists, f'kine_{tag}_jetphi', dataFRAME.Histo1D( frag.kJetPhi(tag),'jet_phi'   , 'event_weight') )
            setattr(hists, f'kine_{tag}_nJet'  , dataFRAME.Histo1D( frag.kNJet  (tag),'jet_multiplicity', 'event_weight') )
        KinematicPlots(dfDATA, 'data')
        KinematicPlots(dfSIGN, 'gjet')
        KinematicPlots(dfSIGN, 'sigL')
        KinematicPlots(dfSIGN, 'sigC')
        KinematicPlots(dfSIGN, 'sigB')
        KinematicPlots(dfFAKE, 'fake')
        KinematicPlots(dfSIDE, 'side')
        draw_orig_hist = True if 'event_weight_orig' in dfSIGN.GetColumnNames() else False
        if draw_orig_hist:
            KinematicPlotsORIG(dfSIGN, 'gjet_origweight')
            KinematicPlotsORIG(dfSigL, 'sigL_origweight')
            KinematicPlotsORIG(dfSigC, 'sigC_origweight')
            KinematicPlotsORIG(dfSigB, 'sigB_origweight')

        ### all entries
        hists.data_BDTAll = dfDATA.Histo1D( frag.hBDTAll(names.data), 'photon_mva', 'event_weight' )
        hists.gjet_BDTAll = dfSIGN.Histo1D( frag.hBDTAll(names.gjet), 'photon_mva', 'event_weight' )
        hists.sigL_BDTAll = dfSigL.Histo1D( frag.hBDTAll(names.sigL), 'photon_mva', 'event_weight' )
        hists.sigC_BDTAll = dfSigC.Histo1D( frag.hBDTAll(names.sigC), 'photon_mva', 'event_weight' )
        hists.sigB_BDTAll = dfSigB.Histo1D( frag.hBDTAll(names.sigB), 'photon_mva', 'event_weight' )
        hists.fake_BDTAll = dfFAKE.Histo1D( frag.hBDTAll(names.fake), 'photon_mva', 'event_weight' )
        hists.side_BDTAll = dfSIDE.Histo1D( frag.hBDTAll(names.side), 'photon_mva', 'event_weight' )
        hists.gJET_BDTAll = dfSIGN.Histo1D( frag.hBDTAll(names.gJET), 'photon_mva')
        hists.sigl_BDTAll = dfSigL.Histo1D( frag.hBDTAll(names.sigl), 'photon_mva')
        hists.sigc_BDTAll = dfSigC.Histo1D( frag.hBDTAll(names.sigc), 'photon_mva')
        hists.sigb_BDTAll = dfSigB.Histo1D( frag.hBDTAll(names.sigb), 'photon_mva')

        hists.data_btag = dfDATA.Histo1D( frag.hbtag(names.data), 'ParTB', 'event_weight' )
        hists.sigL_btag = dfSigL.Histo1D( frag.hbtag(names.sigL), 'ParTB', 'event_weight' )
        hists.sigC_btag = dfSigC.Histo1D( frag.hbtag(names.sigC), 'ParTB', 'event_weight' )
        hists.sigB_btag = dfSigB.Histo1D( frag.hbtag(names.sigB), 'ParTB', 'event_weight' )
        hists.fake_btag = dfFAKE.Histo1D( frag.hbtag(names.fake), 'ParTB', 'event_weight' )
        hists.side_btag = dfSIDE.Histo1D( frag.hbtag(names.side), 'ParTB', 'event_weight' )
        hists.gJET_btag = dfSIGN.Histo1D( frag.hbtag(names.gJET), 'ParTB')
        hists.sigl_btag = dfSigL.Histo1D( frag.hbtag(names.sigl), 'ParTB')
        hists.sigc_btag = dfSigC.Histo1D( frag.hbtag(names.sigc), 'ParTB')
        hists.sigb_btag = dfSigB.Histo1D( frag.hbtag(names.sigb), 'ParTB')

        hists.data_cvsb = dfDATA.Histo1D( frag.hcvsb(names.data), 'ParTCvsB', 'event_weight' )
        hists.sigL_cvsb = dfSigL.Histo1D( frag.hcvsb(names.sigL), 'ParTCvsB', 'event_weight' )
        hists.sigC_cvsb = dfSigC.Histo1D( frag.hcvsb(names.sigC), 'ParTCvsB', 'event_weight' )
        hists.sigB_cvsb = dfSigB.Histo1D( frag.hcvsb(names.sigB), 'ParTCvsB', 'event_weight' )
        hists.fake_cvsb = dfFAKE.Histo1D( frag.hcvsb(names.fake), 'ParTCvsB', 'event_weight' )
        hists.side_cvsb = dfSIDE.Histo1D( frag.hcvsb(names.side), 'ParTCvsB', 'event_weight' )
        hists.gJET_cvsb = dfSIGN.Histo1D( frag.hcvsb(names.gJET), 'ParTCvsB')
        hists.sigl_cvsb = dfSigL.Histo1D( frag.hcvsb(names.sigl), 'ParTCvsB')
        hists.sigc_cvsb = dfSigC.Histo1D( frag.hcvsb(names.sigc), 'ParTCvsB')
        hists.sigb_cvsb = dfSigB.Histo1D( frag.hcvsb(names.sigb), 'ParTCvsB')

        hists.data_cvsl = dfDATA.Histo1D( frag.hcvsl(names.data), 'ParTCvsL', 'event_weight' )
        hists.sigL_cvsl = dfSigL.Histo1D( frag.hcvsl(names.sigL), 'ParTCvsL', 'event_weight' )
        hists.sigC_cvsl = dfSigC.Histo1D( frag.hcvsl(names.sigC), 'ParTCvsL', 'event_weight' )
        hists.sigB_cvsl = dfSigB.Histo1D( frag.hcvsl(names.sigB), 'ParTCvsL', 'event_weight' )
        hists.fake_cvsl = dfFAKE.Histo1D( frag.hcvsl(names.fake), 'ParTCvsL', 'event_weight' )
        hists.side_cvsl = dfSIDE.Histo1D( frag.hcvsl(names.side), 'ParTCvsL', 'event_weight' )
        hists.gJET_cvsl = dfSIGN.Histo1D( frag.hcvsl(names.gJET), 'ParTCvsL')
        hists.sigl_cvsl = dfSigL.Histo1D( frag.hcvsl(names.sigl), 'ParTCvsL')
        hists.sigc_cvsl = dfSigC.Histo1D( frag.hcvsl(names.sigc), 'ParTCvsL')
        hists.sigb_cvsl = dfSigB.Histo1D( frag.hcvsl(names.sigb), 'ParTCvsL')


        hists.data2D_ctag = dfDATA.Histo2D( frag.h2DcvsbANDcvsl(names.data), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.sigL2D_ctag = dfSigL.Histo2D( frag.h2DcvsbANDcvsl(names.sigL), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.sigC2D_ctag = dfSigC.Histo2D( frag.h2DcvsbANDcvsl(names.sigC), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.sigB2D_ctag = dfSigB.Histo2D( frag.h2DcvsbANDcvsl(names.sigB), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.fake2D_ctag = dfFAKE.Histo2D( frag.h2DcvsbANDcvsl(names.fake), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.side2D_ctag = dfSIDE.Histo2D( frag.h2DcvsbANDcvsl(names.side), 'ParTCvsB', 'ParTCvsL', 'event_weight' )
        hists.gJET2D_ctag = dfSIGN.Histo2D( frag.h2DcvsbANDcvsl(names.gJET), 'ParTCvsB', 'ParTCvsL')
        hists.sigl2D_ctag = dfSigL.Histo2D( frag.h2DcvsbANDcvsl(names.sigl), 'ParTCvsB', 'ParTCvsL')
        hists.sigc2D_ctag = dfSigC.Histo2D( frag.h2DcvsbANDcvsl(names.sigc), 'ParTCvsB', 'ParTCvsL')
        hists.sigb2D_ctag = dfSigB.Histo2D( frag.h2DcvsbANDcvsl(names.sigb), 'ParTCvsB', 'ParTCvsL')

        if draw_orig_hist:
            hists.ogjet_BDTAll = dfSIGN.Histo1D( frag.hBDTAll(names.ogjet), 'photon_mva', 'event_weight_orig')
            hists.osigl_BDTAll = dfSigL.Histo1D( frag.hBDTAll(names.osigl), 'photon_mva', 'event_weight_orig')
            hists.osigc_BDTAll = dfSigC.Histo1D( frag.hBDTAll(names.osigc), 'photon_mva', 'event_weight_orig')
            hists.osigb_BDTAll = dfSigB.Histo1D( frag.hBDTAll(names.osigb), 'photon_mva', 'event_weight_orig')

            hists.ogjet_btag = dfSIGN.Histo1D( frag.hbtag(names.ogjet), 'ParTB', 'event_weight_orig')
            hists.osigl_btag = dfSigL.Histo1D( frag.hbtag(names.osigl), 'ParTB', 'event_weight_orig')
            hists.osigc_btag = dfSigC.Histo1D( frag.hbtag(names.osigc), 'ParTB', 'event_weight_orig')
            hists.osigb_btag = dfSigB.Histo1D( frag.hbtag(names.osigb), 'ParTB', 'event_weight_orig')

            hists.ogjet_cvsb = dfSIGN.Histo1D( frag.hcvsb(names.ogjet), 'ParTCvsB', 'event_weight_orig')
            hists.osigl_cvsb = dfSigL.Histo1D( frag.hcvsb(names.osigl), 'ParTCvsB', 'event_weight_orig')
            hists.osigc_cvsb = dfSigC.Histo1D( frag.hcvsb(names.osigc), 'ParTCvsB', 'event_weight_orig')
            hists.osigb_cvsb = dfSigB.Histo1D( frag.hcvsb(names.osigb), 'ParTCvsB', 'event_weight_orig')

            hists.ogjet_cvsl = dfSIGN.Histo1D( frag.hcvsl(names.ogjet), 'ParTCvsL', 'event_weight_orig')
            hists.osigl_cvsl = dfSigL.Histo1D( frag.hcvsl(names.osigl), 'ParTCvsL', 'event_weight_orig')
            hists.osigc_cvsl = dfSigC.Histo1D( frag.hcvsl(names.osigc), 'ParTCvsL', 'event_weight_orig')
            hists.osigb_cvsl = dfSigB.Histo1D( frag.hcvsl(names.osigb), 'ParTCvsL', 'event_weight_orig')


            hists.ogjet2D_ctag = dfSIGN.Histo2D( frag.h2DcvsbANDcvsl(names.ogjet), 'ParTCvsB', 'ParTCvsL', 'event_weight_orig')
            hists.osigl2D_ctag = dfSigL.Histo2D( frag.h2DcvsbANDcvsl(names.osigl), 'ParTCvsB', 'ParTCvsL', 'event_weight_orig')
            hists.osigc2D_ctag = dfSigC.Histo2D( frag.h2DcvsbANDcvsl(names.osigc), 'ParTCvsB', 'ParTCvsL', 'event_weight_orig')
            hists.osigb2D_ctag = dfSigB.Histo2D( frag.h2DcvsbANDcvsl(names.osigb), 'ParTCvsB', 'ParTCvsL', 'event_weight_orig')

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


def add_btagSF(usedDFs):
    dfSIGN = usedDFs.dfsign.Define('event_weight', f'wgt*{DATA_LUMINOSITY}')

    df_new = Define_NormalizeBTagSF(dfSIGN, 'renormREQUIRED_wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)
    #df_new = Define_NormalizeBTagSF(dfSIGN, 'wgt_WPbL_central', extfunc.evtwgt_WPbLCentral)
    ## new: filter then calculate weight
    binning = 'jet_pt > 500 && jet_pt < 1000 && abs(jet_eta) > 1.5 && abs(photon_eta)>1.5'
    binnedf_sign = df_new.Filter(binning)

    df = binnedf_sign

    #hnew = df.Histo1D( ("hnew", "", 120, 0.85,1.5), extfunc.evtwgt_WPbLCentral)
    #hnew = df.Histo1D(extfunc.evtwgt_WPbLCentral)
    hnew = df.Histo1D( ('hi','renormREQUIRED_wgt_WPbL_central', 80, 0.85,1.5),'renormREQUIRED_wgt_WPbL_central')


    ## ref: calcualate weight then filter

    canv = ROOT.TCanvas('c1','',800,800)
    hnew.SetLineColor(ROOT.kRed)
    hnew.SetLineWidth(2)
    hnew.Draw("HIST")

    canv.SetLogy()
    canv.SaveAs("hi.png")






    #dfSIGN.Define('WPb_loose_sf_central', [&](


def testfunc_add_btagSF():
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )
    add_btagSF(used_data_frames)
    exit(0)


if __name__ == "__main__":
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
            format='[makehisto_ctagfit_estimateSR] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

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


