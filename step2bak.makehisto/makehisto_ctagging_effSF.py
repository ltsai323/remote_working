#!/usr/bin/env python3
import logging
import sys

log = logging.getLogger(__name__)

import ROOT
import makehisto_usefulfunc as frag


hBTAG = lambda hNAME: ( hNAME, 'bScore', 20, 0., 1.)
hCvsL = lambda hNAME: ( hNAME, 'CvsL'  , 20, 0., 1.)
hCvsB = lambda hNAME: ( hNAME, 'CvsB'  , 20, 0., 1.)
hCTAGH = lambda hNAME: ( hNAME, 'CvsB and CvsL high res', 20, 0., 1., 20, 0.,1.) # x:CvsB y:CvsL
#hCTAGL = lambda hNAME: ( hNAME, 'CvsB and CvsL low res', 5, 0., 1., 5, 0.,1.) # x:CvsB y:CvsL
hCTAGL = lambda hNAME: ( hNAME, 'CvsB and CvsL low res',10, 0., 1.,10, 0.,1.) # x:CvsB y:CvsL
#h3DPhoPtJetPtANDnJet= lambda n: (n,'3D(phoPT,jetPT,nJET)',
#                                 40, DEFAULT_PHOPT_RANGE[0], DEFAULT_PHOPT_RANGE[1],
#                                 40, DEFAULT_JETPT_RANGE[0],DEFAULT_JETPT_RANGE[1],
#                                 18,0,18)



def GetHistsFromFile(fileIN, oTAG, cut='1', weight='1'):
    dfIN = ROOT.RDataFrame('tree', fileIN)
    return GetHists(dfIN.Filter(cut), oTAG, weight)


def GetHists(dataFRAME, oTAG, weight='event_weight'):
    ## input dataframe is assumed to use event_weight and selection already applied.
    def frag_hists(dataFRAME, tag):
        hists = frag.histCollection()
        hists.btag = dataFRAME.Histo1D( hBTAG(f'btag_{tag}'), 'ParTB', weight )
        hists.cvsl = dataFRAME.Histo1D( hCvsL(f'cvsl_{tag}'), 'ParTCvsL', weight )
        hists.cvsb = dataFRAME.Histo1D( hCvsB(f'cvsb_{tag}'), 'ParTCvsB', weight )
        hists.ctagH = dataFRAME.Histo2D( hCTAGH(f'ctag_{tag}_hRes'), 'ParTCvsB', 'ParTCvsL', weight )
        hists.ctagL = dataFRAME.Histo2D( hCTAGL(f'ctag_{tag}_lRes'), 'ParTCvsB', 'ParTCvsL', weight )

        hists.NormAllHists()
        return hists

    df = dataFRAME
    histsA = frag_hists( df                      , f'{oTAG}_all' )
    histsL = frag_hists( df.Filter('isHadFlvr_L'), f'{oTAG}_L' )
    histsC = frag_hists( df.Filter('isHadFlvr_C'), f'{oTAG}_C' )
    histsB = frag_hists( df.Filter('isHadFlvr_B'), f'{oTAG}_B' )

    return { 'all':histsA, 'L':histsL, 'C':histsC, 'B':histsB }


def fill_zero(hU, hD):
    if type(hU) != type(hD): raise IOError(f'[TypeNotMatch] different type of hU ({type(hU)}) and hD ({type(hD)})')

    if isinstance(hU, ROOT.TH2) and isinstance(hD, ROOT.TH2):
        maxbin = hU.FindBin(1e9,1e9) + 1  ### find last bin idx +1 for tot number of bins
        for binidx in range(maxbin):
            if hU.GetBinContent(binidx) < 1e-8 or hD.GetBinContent(binidx) < 1e-8:
                hU.SetBinContent(binidx, 1e-8)
                hU.SetBinError  (binidx, 1e-12)
                hD.SetBinContent(binidx, 1e-8)
                hD.SetBinError  (binidx, 1e-12)
        return

    if isinstance(hU, ROOT.TH1) and isinstance(hD, ROOT.TH1):
        for binidx in range(hU.GetNbinsX()+2): ## include underflowbin and overflowbin
            if hU.GetBinContent(binidx) < 1e-8 or hD.GetBinContent(binidx) < 1e-8:
                hU.SetBinContent(binidx,1e-8)
                hU.SetBinError  (binidx,1e-12)
                hD.SetBinContent(binidx,1e-8)
                hD.SetBinError  (binidx,1e-12)
        return
    raise IOError(f'[UnsupportedObj] type hU({type(hU)}) and hD({type(hD)}) are not supported in fill_zero()')
    

def TakeRatio(histCOLLECTIONdict0:dict, histCOLLECTIONdict1:dict) -> frag.histCollection:
    def take_ratio(histU, histD, ratioNAME):
        log.debug(f'[input] hU({histU}) and hD({histD})')

        hU = histU.GetValue()
        hD = histD.GetValue()
        if hU.GetNbinsX() != hD.GetNbinsX():
            raise IOError(f'[BinningUnMatched] nbinsX of hU({hU.GetNbinsX}) and hD({hD.GetNbinsX()}) is different')

        fill_zero(hU,hD)
       #supported_type = False
       #if isinstance(hU, ROOT.TH1D) and isinstance(hD, ROOT.TH1D):
       #    supported_type = True
       #    for idx in range(hU.GetNbinsX()):
       #        binidx = idx + 1
       #        if hU.GetBinContent(binidx) < 1e-8 or hD.GetBinContent(binidx) < 1e-8:
       #            hU.SetBinContent(binidx,1e-8)
       #            hU.SetBinError  (binidx,1e-12)
       #            hD.SetBinContent(binidx,1e-8)
       #            hD.SetBinError  (binidx,1e-12)
       #if isinstance(hU, ROOT.TH2D) and isinstance(hD, ROOT.TH2D):
       #    supported_type = True
       #    for idx in range(hU.GetNbinsX()):
       #        for idy in range(hU.GetNbinsY()):
       #            binidx = idx + 1
       #            binidy = idy + 1
       #            if hU.GetBinContent(binidx,binidy) < 1e-8 or hD.GetBinContent(binidx,binidy) < 1e-8:
       #                hU.SetBinContent(binidx,binidy,1e-8)
       #                hU.SetBinError  (binidx,binidy,1e-12)
       #                hD.SetBinContent(binidx,binidy,1e-8)
       #                hD.SetBinError  (binidx,binidy,1e-12)
       #if not supported_type: raise IOError(f'[UnsupportedHistType] hU({type(hU)}) or hD({type(hD)}) are not supported')

        #err_ratio = ROOT.TGraphAsymmErrors()
        #err_ratio.SetName(ratioNAME)
        #err_ratio.Divide(hU,hD,'pois')
        err_ratio = hU.Clone(ratioNAME)
        err_ratio.Divide(hD)
        return err_ratio
    histCOLL0A = histCOLLECTIONdict0['all']
    histCOLL0L = histCOLLECTIONdict0['L']
    histCOLL0C = histCOLLECTIONdict0['C']
    histCOLL0B = histCOLLECTIONdict0['B']
    
    histCOLL1A = histCOLLECTIONdict1['all']
    histCOLL1L = histCOLLECTIONdict1['L']
    histCOLL1C = histCOLLECTIONdict1['C']
    histCOLL1B = histCOLLECTIONdict1['B']

    hists = frag.histCollection()
    for histNAME in vars(histCOLL0L).keys():
        ratioA = take_ratio( getattr(histCOLL0A,histNAME),getattr(histCOLL1A,histNAME),f'ratioALL_{histNAME}' )
        ratioL = take_ratio( getattr(histCOLL0L,histNAME),getattr(histCOLL1L,histNAME),f'ratioL_{histNAME}' )
        ratioC = take_ratio( getattr(histCOLL0C,histNAME),getattr(histCOLL1C,histNAME),f'ratioC_{histNAME}' )
        ratioB = take_ratio( getattr(histCOLL0B,histNAME),getattr(histCOLL1B,histNAME),f'ratioB_{histNAME}' )
        setattr(hists, ratioA.GetName(), ratioA)
        setattr(hists, ratioL.GetName(), ratioL)
        setattr(hists, ratioC.GetName(), ratioC)
        setattr(hists, ratioB.GetName(), ratioB)
    return hists

def Access_MyShapeSF(dataFRAME, myTAGGINGfile):
    '''
    Add new event weight "event_weight_ctag" for CvsL,CvsB (2D) and "event_weight_btag" for bTag (1D).
    Such as it should calibrate the shape difference.

    Requirement: overall event weight should be stored in column "event_weight".
    '''

   #effFILE = 'ctagging_effSF.root'
    effFILE = myTAGGINGfile
    nameL_ctag = 'ratioL_ctagL'
    nameC_ctag = 'ratioC_ctagL'
    nameB_ctag = 'ratioB_ctagL'

    nameL_btag = 'ratioL_btag'
    nameC_btag = 'ratioC_btag'
    nameB_btag = 'ratioB_btag'
    loadOTHERfile = f'''
    TFile* fIN = TFile::Open("{effFILE}");
    TH2D* hEffL_ctag = (TH2D*) fIN->Get("{nameL_ctag}");
    TH2D* hEffC_ctag = (TH2D*) fIN->Get("{nameC_ctag}");
    TH2D* hEffB_ctag = (TH2D*) fIN->Get("{nameB_ctag}");
    Double_t sf_ctag(TH2* hEFF, Double_t cvsb, Double_t cvsl)
    {{ int ibin = hEFF->FindBin(cvsb,cvsl); return hEFF->GetBinContent(ibin); }}

    Double_t SF_CTag(int hadFLVR, Double_t cvsb, Double_t cvsl)
    {{
        if ( hadFLVR == 0 ) return sf_ctag( hEffL_ctag, cvsb, cvsl );
        if ( hadFLVR == 4 ) return sf_ctag( hEffC_ctag, cvsb, cvsl );
        if ( hadFLVR == 5 ) return sf_ctag( hEffB_ctag, cvsb, cvsl );
        return -999;
    }}


    TH1D* hEffL_btag = (TH1D*) fIN->Get("{nameL_btag}");
    TH1D* hEffC_btag = (TH1D*) fIN->Get("{nameC_btag}");
    TH1D* hEffB_btag = (TH1D*) fIN->Get("{nameB_btag}");
    Double_t sf_btag(TH1* hEFF, Double_t btag)
    {{ int ibin = hEFF->FindBin(btag); return hEFF->GetBinContent(ibin); }}
    Double_t SF_BTag(int hadFLVR, Double_t btag)
    {{ 
        if ( hadFLVR == 0 ) return sf_btag( hEffL_btag, btag );
        if ( hadFLVR == 4 ) return sf_btag( hEffC_btag, btag );
        if ( hadFLVR == 5 ) return sf_btag( hEffB_btag, btag );
        return -999;
    }}
    '''
    ROOT.gInterpreter.Declare(loadOTHERfile)

    d = dataFRAME \
            .Define( 'sf_btag',  'SF_BTag(jetHadFlvr,ParTB)' ) \
            .Define( 'sf_ctag',  'SF_CTag(jetHadFlvr,ParTCvsB,ParTCvsL)' )

    sum_of_sf_btag_norm = d.Define('sf_btagANDevtwgt','sf_btag * event_weight').Sum('sf_btagANDevtwgt').GetValue()
    sum_of_sf_ctag_norm = d.Define('sf_ctagANDevtwgt','sf_ctag * event_weight').Sum('sf_ctagANDevtwgt').GetValue()
    sum_of_evtwgt_norm = d.Sum('event_weight').GetValue()

    sf_btag_norm = sum_of_evtwgt_norm / sum_of_sf_btag_norm
    sf_ctag_norm = sum_of_evtwgt_norm / sum_of_sf_ctag_norm 

    return d \
            .Define('event_weight_btagsf', f'sf_btag * {sf_btag_norm}') \
            .Define('event_weight_ctagsf', f'sf_ctag * {sf_ctag_norm}') \
            .Define('event_weight_btag', 'event_weight_btagsf * event_weight') \
            .Define('event_weight_ctag', 'event_weight_ctagsf * event_weight')

def mainfunc_dataframe( taganddataframeTARGET, taganddataframeSIGNAL, outFILEname ):
    ## input dataframe is assumed to have column "event_weight" and selection already applied.
    tagTARGET, dfTARGET = taganddataframeTARGET
    tagSIGNAL, dfSIGNAL = taganddataframeSIGNAL
    h_target = GetHists(dfTARGET, tagTARGET, 'event_weight')
    h_signal = GetHists(dfSIGNAL, tagSIGNAL, 'event_weight')
    h_signal_orig = GetHists(dfSIGNAL, tagSIGNAL+'_origweight', 'event_weight_orig')

    ratio = TakeRatio(h_target,h_signal)
    
    fout = ROOT.TFile(outFILEname, 'recreate')
    fout.cd()
    for tag, histCOLLs in h_target.items():
        histCOLLs.WriteAllHists(fout)
    for tag, histCOLLs in h_signal.items():
        histCOLLs.WriteAllHists(fout)
    for tag, histCOLLs in h_signal_orig.items():
        histCOLLs.WriteAllHists(fout)
    ratio.WriteAllHists(fout)
    fout.Close()


    #### add validation plots
    dfSIGNALcalb = Access_MyShapeSF(dfSIGNAL, outFILEname)
    tagSIGNALcalb_btag = f'{tagSIGNAL}_calb_btagSF'
    h_signal_calb_btag = GetHists(dfSIGNALcalb, tagSIGNALcalb_btag, 'event_weight_btag')
    tagSIGNALcalb_ctag = f'{tagSIGNAL}_calb_ctagSF'
    h_signal_calb_ctag = GetHists(dfSIGNALcalb, tagSIGNALcalb_ctag, 'event_weight_ctag')

    fout = ROOT.TFile(outFILEname, 'update')
    for tag, histCOLLs in h_signal_calb_btag.items():
        #delattr(histCOLLs, 'btag' )
        delattr(histCOLLs, 'cvsb' )
        delattr(histCOLLs, 'cvsl' )
        delattr(histCOLLs, 'ctagH')
        delattr(histCOLLs, 'ctagL')
        histCOLLs.WriteAllHists(fout)
    for tag, histCOLLs in h_signal_calb_ctag.items():
        delattr(histCOLLs, 'btag' )
        #delattr(histCOLLs, 'cvsb' )
        #delattr(histCOLLs, 'cvsl' )
        #delattr(histCOLLs, 'ctagH')
        #delattr(histCOLLs, 'ctagL')
        histCOLLs.WriteAllHists(fout)
    fout.Close()


def mainfunc(tagandfileTARGET, tagandfileSIGNAL, outFILEname, cut):
    tagTARGET, fileTARGET = tagandfileTARGET
    tagSIGNAL, fileSIGNAL = tagandfileSIGNAL
    h_target = GetHistsFromFile(fileTARGET, tagTARGET, cut, 'wgt')
    h_signal = GetHistsFromFile(fileSIGNAL, tagSIGNAL, cut, 'wgt')

    ratio = TakeRatio(h_target,h_signal)
    
    fout = ROOT.TFile(outFILEname, 'recreate')
    fout.cd()

    for tag, histCOLLs in h_target.items():
        histCOLLs.WriteAllHists(fout)
    for tag, histCOLLs in h_signal.items():
        histCOLLs.WriteAllHists(fout)

   #h_target['all'].WriteAllHists(fout)
   #h_target['L'].WriteAllHists(fout)
   #h_target['C'].WriteAllHists(fout)
   #h_target['B'].WriteAllHists(fout)
   #h_signal['all'].WriteAllHists(fout)
   #h_signal['L'].WriteAllHists(fout)
   #h_signal['C'].WriteAllHists(fout)
   #h_signal['B'].WriteAllHists(fout)
    ratio.WriteAllHists(fout)
    fout.Close()


def mainfunc_has_pt_reweight( tagandfileTARGET, tagandfileSIGNAL, oTAG, cut, oNAMEctagEFF):
    tagTARGET, fileTARGET = tagandfileTARGET
    tagSIGNAL, fileSIGNAL = tagandfileSIGNAL
    dfTARGET = ROOT.RDataFrame('tree', fileTARGET)
    dfSIGNAL = ROOT.RDataFrame('tree', fileSIGNAL)

    dfT = dfTARGET.Filter(cut).Define('event_weight', 'wgt')
    dfS = dfSIGNAL.Filter(cut).Define('event_weight', 'wgt')

    ### update photon pt and jet pt region for jetpt reweight SF and kinematics plots
    phopt_U = dfT.Max('photon_pt').GetValue()
    phopt_D = dfT.Min('photon_pt').GetValue()
    frag.kPhoPt  = lambda n: ( f'kine_{n}_phopt' , 'kinematics checking', int( (phopt_U-phopt_D)/20 ), phopt_D,phopt_U ) ## every 20 GeV calculate a SF

    from makehisto_usefulfunc import CreateJetPtSF_general, UpdateEvtWeight_MyWeight
    sfFILEname = f'sfhist_forEffFiles_{oTAG}.root'
    CreateJetPtSF_general(dfT, dfS, sfFILEname)

    dfs = UpdateEvtWeight_MyWeight(dfS, oTAG, sfFILEname)

    mainfunc_dataframe( (tagTARGET, dfT), (tagSIGNAL, dfs), oNAMEctagEFF )


if __name__ == '__main__':
    import os
    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format=f'%(levelname)-7s{__file__.split("/")[-1]} >>> %(message)s',
                        datefmt='%H:%M:%S')

    tagTARGET = 'TARGET_PythiaFlat'
    fileTARGET = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root'
    tagSIGNAL = 'SIGNAL_Madgraph'
    fileSIGNAL = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root'

    from multiprocessing import Process
    try:
        cut = 'abs(photon_eta)<1.5 && abs(jet_eta)<1.5'
        binning = '0_0'
    #mainfunc_has_pt_reweight( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root')
        t00 = Process( target=mainfunc_has_pt_reweight,
                            args=( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root' )
                            )
        t00.start()

        cut = 'abs(photon_eta)<1.5 && abs(jet_eta)>1.5 && photon_pt>250 && photon_pt<300'
        binning = '0_1'
        t01 = Process( target=mainfunc_has_pt_reweight,
                            args=( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root' )
                            )
        t01.start()

        cut = 'abs(photon_eta)>1.5 && abs(jet_eta)<1.5'
        binning = '1_0'
        t10 = Process( target=mainfunc_has_pt_reweight,
                            args=( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root' )
                            )
        t10.start()

        cut = 'abs(photon_eta)>1.5 && abs(jet_eta)>1.5'
        binning = '1_1'
        t11 = Process( target=mainfunc_has_pt_reweight,
                            args=( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root' )
                            )
        t11.start()

        cut = '1'
        binning = '9_9'
        t99 = Process( target=mainfunc_has_pt_reweight,
                            args=( (tagTARGET,fileTARGET), (tagSIGNAL,fileSIGNAL), binning, cut, f'ctagging_effSF{binning}.root' )
                            )
        t99.start()

        t00.join()
        t01.join()
        t10.join()
        t11.join()
        t99.join()
    except KeyboardInterrupt:
        t00.terminate()
        t01.terminate()
        t10.terminate()
        t11.terminate()
        t99.terminate()

        t00.join()
        t01.join()
        t10.join()
        t11.join()
        t99.join()
        os.kill(os.getpid(), signal.SIGINT) ## raising keyboard interrupt
