#!/usr/bin/env python3
import makehisto_usefulfunc as frag
#!/usr/bin/env python3
import logging
import sys
import os

log = logging.getLogger(__name__)
USE_JETPT_NJET_REWEIGHT = True
JETPT_REWEIGHT_NOT_INITIALIZED = True ### variable promise CreateJetPtSF_toTH1() and LoadAdditionalFunc() only executed once. Always set this variable as True initially!


import numpy

def variant_bins( *newBINNINGs ):
    outARR = None
    for iBIN, newBINNING in enumerate(newBINNINGs):
        nbins, xmin, xmax = newBINNING
        xstep = (xmax-xmin) / float(nbins)

        new_arr = numpy.arange(xmin,xmax,step=xstep)
        if outARR is None:
            outARR = new_arr
        else:
            if outARR[-1] > new_arr[0]:
                raise ValueError(f'[BinMixed] Got {iBIN}th binning {newBINNING} from \n{newBINNINGs}')
            outARR = numpy.append(outARR,new_arr)
    outARR = numpy.append(outARR, 1.0) # append last bin

    return outARR

import makehisto_ctagfit_estimateSR as content
import makehisto_GJetPythiaFlatPsuedodata_ctagfit_estimateSR as content_psuedo
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc
import ROOT
#DATA_LUMINOSITY = 26.81
DATA_LUMINOSITY = 27.01


def the_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1' ):
    cuts = f'{additionalCUT} && photon_pt>{pPTlow} && photon_pt<{pPThigh}'
    if pETAbin == 0: cuts += ' && TMath::Abs(photon_eta)<1.5'
    if pETAbin == 1: cuts += ' && TMath::Abs(photon_eta)>1.5'
    if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
    if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
    return cuts
def the_sideband_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1'):
    # use previous 2 bin as sideband increasing statisticcs
    #return the_binning(pETAbin,jETAbin,pPTlow,pPThigh,additionalCUT) if pPTlow < 600 else the_binning(pETAbin,jETAbin,500,600,additionalCUT)
    return the_binning(pETAbin,jETAbin,pPTlow,pPThigh,additionalCUT) if pPTlow < 300 else the_binning(pETAbin,jETAbin,300,400,additionalCUT)

def mainfunc(
        usedDFs,
        binningSTR:str, binningSTRsideband:str,
        pETAbin:int,jETAbin:int,pPTlow:int,pPThigh:int,
        defFUNC:dict,
        outFILEname
        ):
    ### normal situation
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
    }

   #### use QCD as fake data now
   #cut_func = {
   #        'data': lambda df: df.Filter(f'{binningSTR} && wgt!=0 && wgt < 5'),
   #        'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
   #        'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
   #        'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
   #}

    used_df = content.define_and_filter(usedDFs, dfCUTfuncs = cut_func, dfDEFfuncs = defFUNC)

    ### update photon pt and jet pt region for jetpt reweight SF and kinematics plots
    phopt_U = used_df.dfSR.Max('photon_pt').GetValue()
    phopt_D = used_df.dfSR.Min('photon_pt').GetValue()
    frag.kPhoPt  = lambda n: ( f'kine_{n}_phopt' , 'kinematics checking', 128, phopt_D,phopt_U )
    #jetpt_U = used_df.dfSR.Max('jet_pt').GetValue()
    #jetpt_D = used_df.dfSR.Min('jet_pt').GetValue()
    #frag.kJetPt  = lambda n: ( f'kine_{n}_jetpt' , 'kinematics checking', 256, jetpt_D,jetpt_U )

    #jetptbinning = 256
    #njetbinning = 18
    #frag.hJetPt = lambda n: (n,'jet Pt v.s. njet', jetptbinning, jetpt_D,jetpt_U)
    #frag.h2DJetPtANDnJet = lambda n: (n,'jet Pt v.s. njet', jetptbinning, jetpt_D,jetpt_U, njetbinning, 0,njetbinning)


    if USE_JETPT_NJET_REWEIGHT:
        global JETPT_REWEIGHT_NOT_INITIALIZED
        if JETPT_REWEIGHT_NOT_INITIALIZED:
            log.warning('[JetPtReweightCalulated] This message should only found once!!!!!!')
            log.warning('[JetPtReweightCalulated] Craeting jet pt sf ')
            CreateJetPtSF_toTH1(used_df, pETAbin,jETAbin,pPTlow,pPThigh)
            LoadAdditionalFunc()
            JETPT_REWEIGHT_NOT_INITIALIZED = False
        ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign, pETAbin,jETAbin,pPTlow,pPThigh, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF
        used_df.dfsign = ddd




    content.main_content(
        usedDF = used_df,
        outputFILE = outFILEname,
    )
    content_psuedo.update_truth(
            usedDF = used_df,
            outputFILE = outFILEname,
            )

    print(f'[OutputFile] {outFILEname}')


#WPbLunc = {
#        1: ('renormREQUIRED_wgt_WPbL_central'   ,'renormREQUIRED_wgt_WPbL_central'   ),
#        2: ('renormREQUIRED_wgt_WPbL_bStatUp'   ,'renormREQUIRED_wgt_WPbL_bStatDown' ),
#        3: ("renormREQUIRED_wgt_WPbL_bUp"       ,"renormREQUIRED_wgt_WPbL_bDown"     ),
#        4: ("renormREQUIRED_wgt_WPbL_bJESUp"    ,"renormREQUIRED_wgt_WPbL_bJESDown"  ),
#        5: ("renormREQUIRED_wgt_WPbL_bFragUp"   ,"renormREQUIRED_wgt_WPbL_bFragDown" ),
#        6: ("renormREQUIRED_wgt_WPbL_bPUUp"     ,"renormREQUIRED_wgt_WPbL_bPUDown"   ),
#        7: ("renormREQUIRED_wgt_WPbL_bType3Up"  ,"renormREQUIRED_wgt_WPbL_bType3Down"),
#        }
#WPcMunc = {
#        1: ('renormREQUIRED_wgt_WPcM_central'   ,'renormREQUIRED_wgt_WPcM_central'   ),
#        2: ('renormREQUIRED_wgt_WPcM_bStatUp'   ,'renormREQUIRED_wgt_WPcM_bStatDown' ),
#        3: ("renormREQUIRED_wgt_WPcM_bUp"       ,"renormREQUIRED_wgt_WPcM_bDown"     ),
#        4: ("renormREQUIRED_wgt_WPcM_bJESUp"    ,"renormREQUIRED_wgt_WPcM_bJESDown"  ),
#        5: ("renormREQUIRED_wgt_WPcM_bFragUp"   ,"renormREQUIRED_wgt_WPcM_bFragDown" ),
#        6: ("renormREQUIRED_wgt_WPcM_bPUUp"     ,"renormREQUIRED_wgt_WPcM_bPUDown"   ),
#        7: ("renormREQUIRED_wgt_WPcM_bType3Up"  ,"renormREQUIRED_wgt_WPcM_bType3Down"),
#        }
WPbLunc = {
        1: ('1', '1'), ## do nothing when using psuedodata
        }
WPcMunc = {
        1: ('1', '1'), ## do nothing when using psuedodata
        }

def mainfunc_eff(
        usedDFs,
        binningSTR:str, wpCUT:str,
        pETAbin:int,jETAbin:int,pPTlow:int,pPThigh:int,
        defFUNC:dict,
        outFILEname
        ):
    ### normal situation
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'1'),
    }

    # ### use QCD as fake data now
    # cut_func = {
    #         'data': lambda df: df.Filter(f'{binningSTR} && wgt!=0 && wgt < 5'),
    #         'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
    #         'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
    #         'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
    # }

    used_df = content.define_and_filter(usedDFs, dfCUTfuncs = cut_func, dfDEFfuncs = defFUNC)



    if USE_JETPT_NJET_REWEIGHT:
        global JETPT_REWEIGHT_NOT_INITIALIZED
        if JETPT_REWEIGHT_NOT_INITIALIZED:
            log.warning('[JetPtReweightCalulated] This message should only found once!!!!!!')
            log.warning('[JetPtReweightCalulated] Craeting jet pt sf ')
            CreateJetPtSF_toTH1(used_df, pETAbin,jETAbin,pPTlow,pPThigh)
            LoadAdditionalFunc()
            JETPT_REWEIGHT_NOT_INITIALIZED = False
        ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign, pETAbin,jETAbin,pPTlow,pPThigh, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF
        used_df.dfsign = ddd

    dfsign = used_df.dfsign


    
    uncs = None
    if wpCUT == 'passWPbL': uncs = WPbLunc
    if wpCUT == 'passWPcM': uncs = WPcMunc
    if uncs is None: raise IOError(f'[InvalidWPcut] WP cut "{wpCUT}" is not supported.')


    def make_eff_plots(dataFRAME):
        ### bin0  : efficiencies without WP cut. it shuould be always 1. (Check SF central reweight does not destroy normalization)
        ### bin1  : efficiencies from central
        ### bin2~N: efficiencies from uncertainties
        nbins = int(len(uncs))
        log.debug(f'[nbins] get nbins {nbins} of histogram')
        hUP = ROOT.TH1F('effUP', 'efficiencies from SF. Bin0:nocut,eff should always1. Bin1:center, Bin2~N:unc', nbins, 1, nbins)
        hDN = ROOT.TH1F('effDN', 'efficiencies from SF. Bin0:nocut,eff should always1. Bin1:center, Bin2~N:unc', nbins, 1, nbins)

        integral_orig = dataFRAME.Sum('event_weight').GetValue()
        for binidx, (uncUPname,uncDNname) in uncs.items():
            df = dataFRAME \
                    .Define(f'evtwgtUP', f'event_weight * {uncUPname}') \
                    .Define(f'evtwgtDN', f'event_weight * {uncDNname}')


            norm_evtup = integral_orig / df.Sum(f'evtwgtUP').GetValue()
            norm_evtdn = integral_orig / df.Sum(f'evtwgtDN').GetValue()

            df_defined = df \
                    .Define(f'norm_evtwgtUP', f'{norm_evtup}') \
                    .Define(f'event_weightUP', 'evtwgtUP * norm_evtwgtUP') \
                    .Define(f'norm_evtwgtDN', f'{norm_evtdn}') \
                    .Define(f'event_weightDN', 'evtwgtDN * norm_evtwgtDN')

            df_filtered = df_defined.Filter(wpCUT)
            integral_up = df_filtered.Sum('event_weightUP').GetValue()
            integral_dn = df_filtered.Sum('event_weightDN').GetValue()
                    


            hUP.SetBinContent(binidx, integral_up/integral_orig)
            hDN.SetBinContent(binidx, integral_dn/integral_orig)

            if binidx == 1: ## for bin1: central. check efficiencies without cut as bin0
                integral_up_nocut = df_defined.Sum('event_weightUP').GetValue()
                integral_dn_nocut = df_defined.Sum('event_weightDN').GetValue()
                hUP.SetBinContent(0, integral_up_nocut/integral_orig)
                hDN.SetBinContent(0, integral_dn_nocut/integral_orig)
        return hUP,hDN

    hUP_L, hDN_L = make_eff_plots( used_df.dfsign.Filter('isHadFlvr_L') )
    hUP_L.SetName('effUP_L')
    hDN_L.SetName('effDN_L')
    hUP_C, hDN_C = make_eff_plots( used_df.dfsign.Filter('isHadFlvr_C') )
    hUP_C.SetName('effUP_C')
    hDN_C.SetName('effDN_C')
    hUP_B, hDN_B = make_eff_plots( used_df.dfsign.Filter('isHadFlvr_B') )
    hUP_B.SetName('effUP_B')
    hDN_B.SetName('effDN_B')
    

    ofile = ROOT.TFile(outFILEname, 'recreate')
    ofile.cd()
    hUP_L.Write()
    hDN_L.Write()
    hUP_C.Write()
    hDN_C.Write()
    hUP_B.Write()
    hDN_B.Write()

    ofile.Close()







def mainfunc_gjet_binning( outFILEname, inFILEdict:dict, defineWEIGHT:dict, additionalCUT='1' ):


    # old
    #ptbinsL = [ 210,230,250,300,400,500,600,1000      ]
    #ptbinsR = [     230,250,300,400,500,600,1000,1500 ]
    ## test
    #ptbinsL = [ 210,230,250,300,400,500,800,          ]
    #ptbinsR = [     230,250,300,400,500,800,1500      ]
    # original photon + jet binning
    ptbinsL = [ 210,230,250,300,400,500,600,800,1000      ]
    ptbinsR = [     230,250,300,400,500,600,800,1000,1500 ]

    for pEta in range(2):
        for jEta in range(2):
            for ptL, ptR in zip(ptbinsL,ptbinsR):
                used_data_frames = frag.UsedDataFrames( **inFILEdict )

                newfilename = outFILEname.replace('.root',f'__{pEta}_{jEta}_{ptL}_{ptR}.root')
                binning = the_binning(pEta,jEta,ptL,ptR, additionalCUT)
                binning_sideband = the_sideband_binning(pEta,jEta,ptL,ptR, additionalCUT)
                mainfunc(
                        used_data_frames,
                        binning, binning_sideband,
                        pEta,jEta,ptL,ptR,
                        defineWEIGHT,
                        newfilename
                        )
                return



def mainfunc_gjet_singlebin( outFILEname, inFILEdict:dict, defineWEIGHT:dict, pEta,jEta,ptL,ptR, additionalCUT='1' ):
    used_data_frames = frag.UsedDataFrames( **inFILEdict )

    newfilename = outFILEname
    binning = the_binning(pEta,jEta,ptL,ptR, additionalCUT)
    binning_sideband = the_sideband_binning(pEta,jEta,ptL,ptR, additionalCUT)
    log.debug(f'cut: {binning}')
    mainfunc(
            used_data_frames,
            binning, binning_sideband,
            pEta,jEta,ptL,ptR,
            defineWEIGHT,
            newfilename
            )
def mainfunc_eff_singlebin( outFILEname, inFILEdict:dict, defineWEIGHT:dict, pEta,jEta,ptL,ptR, wpCUT, additionalCUT ):
    used_data_frames = frag.UsedDataFrames( **inFILEdict )

    newfilename = outFILEname
    binning = the_binning(pEta,jEta,ptL,ptR, additionalCUT)
    log.debug(f'cut: {binning}')
    mainfunc_eff(
            used_data_frames,
            binning, wpCUT,
            pEta,jEta,ptL,ptR,
            defineWEIGHT,
            newfilename
            )

if __name__ == "__main__":
   #bin_btag = variant_bins( [ 7,0,0.3], [ 3,0.3,0.9], [ 5,0.9,1.0] )
   #bin_cvsb = variant_bins( [ 5,0,0.1], [ 3,0.1,0.7], [ 6,0.7,0.85], [1,0.85,1.0] )
   #bin_cvsl = variant_bins( [ 7,0,0.3], [ 3,0.3,0.9], [ 5,0.9,1.0] )
   #frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', len(bin_btag)-1, bin_btag)
   #frag.hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b'     , len(bin_cvsb)-1, bin_cvsb)
   #frag.hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l'     , len(bin_cvsl)-1, bin_cvsl)

   #bin2D_cvsb = variant_bins( [ 2,0,0.1], [ 1,0.1,0.7], [ 3,0.7,1.0] )
   #bin2D_cvsl = variant_bins( [ 3,0,0.3], [ 1,0.3,0.9], [ 2,0.9,1.0] )
   #frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', len(bin2D_cvsb)-1, bin2D_cvsb, len(bin2D_cvsl)-1, bin2D_cvsl)

   #frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 40,0,1)
    bin_btag = variant_bins( [ 7,0,0.3], [ 3,0.3,0.9], [ 5,0.9,1.0] )
    from array import array
    bin_btag = array('f', [ 0., 0.02, 0.04, 0.06, 0.1, 0.15, 0.2, 0.25, 1.0])
    frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', len(bin_btag)-1, bin_btag)
   #frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 60,0,1)
    frag.hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b'     , 40,0,1)
    frag.hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l'     , 40,0,1)

   #frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', 5,0,1, 5,0,1)
   #frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)',7,0,1,7,0,1)
   #bin_cvsb = variant_bins( [ 2,0.,0.1], [2,0.1,0.6], [2,0.6,0.85], [1,0.85,1.0] )
   #bin_cvsb = variant_bins( [ 1,0.,0.05], [3,0.05,0.6], [2,0.6,0.85], [1,0.85,1.0] )
   #bin_cvsl = variant_bins( [ 4,0.,0.4], [1,0.4,0.7], [1,0.7,0.95], [1,0.95,1.0] )
   #bin_cvsl = variant_bins( [ 3,0.,0.3], [3,0.4,0.95], [1,0.95,1.0] )
   #frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', len(bin_cvsb)-1, bin_cvsb, len(bin_cvsl)-1, bin_cvsl)

    bin_cvsb = array('d', [0.,0.2,0.4,0.6,0.8,1.0])
    bin_cvsl = array('d', [0.,0.1,0.2,0.3,0.4,0.6,0.8,1.0])
    frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', len(bin_cvsb)-1, bin_cvsb, len(bin_cvsl)-1, bin_cvsl)


    loglevel = os.environ.get('LOG_LEVEL', 'INFO') # DEBUG, INFO, WARNING
    DEBUG_MODE = True if loglevel == 'DEBUG' else False
    logLEVEL = getattr(logging, loglevel)
    logging.basicConfig(stream=sys.stdout,level=logLEVEL,
                        format=f'%(levelname)-7s{__file__.split("/")[-1]} >>> %(message)s',
                        datefmt='%H:%M:%S')


    outfile = sys.argv[1] if len(sys.argv) > 1 else 'makehisto_psuedodata_rescaled.root'
    argBINNINGstr = sys.argv[2].split('_') ## ex: 0_0_210_230

    pETAbin = int(argBINNINGstr[0])
    jETAbin = int(argBINNINGstr[1])
    pPTlow  = int(argBINNINGstr[2])
    pPThigh = int(argBINNINGstr[3])

    #ROOT.EnableImplicitMT()

    #### redefine the histogram
    #frag.hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
    #frag.hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )

    inFILEdictORIG = {
        'sidebandFILE': '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
        'dataFILE'    :' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
        'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
       #'dataFILE'    : '~/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.allphotonregion.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
       #'signFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
        'signFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
        'fakeFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
            }
    inFILEdict = {
        'sidebandFILE': '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
       #'dataFILE'    :' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
        'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
       #'dataFILE'    : '~/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.allphotonregion.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
       #'signFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
        'signFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
        'fakeFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
            }
    define_weight = {
            'data': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # should modify to 1 if use data.
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }


    def cut(*cuts): return '(' + '&&'.join(cuts) + ')'
    #additional_cut = 'selected_jet_idx==0 && passWPcT'
    additional_cut = 'passWPbM'
    outfilename = outfile
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut(additional_cut))
    exit(0)

    outfilename = outfile.replace('.root', '.WPbL.root')
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut('passWPbL',additional_cut))
    outfilename = outfile.replace('.root', '.WPbL.eff.root')
    mainfunc_eff_singlebin (outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, 'passWPbL', additional_cut)

    outfilename = outfile.replace('.root', '.WPcM.root')
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut('passWPcM',additional_cut))
    outfilename = outfile.replace('.root', '.WPcM.eff.root')
    mainfunc_eff_singlebin (outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, 'passWPcM', additional_cut)

