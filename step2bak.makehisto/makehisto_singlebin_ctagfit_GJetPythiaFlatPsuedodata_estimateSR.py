#!/usr/bin/env python3
import makehisto_usefulfunc as frag
#!/usr/bin/env python3
import logging

log = logging.getLogger(__name__)


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



def mainfunc(
        usedDFs,
        binningSTR:str, binningSTRsideband:str,
        pETAbin:int,jETAbin:int,pPTlow:int,pPThigh:int,
        defFUNC:dict,
        outFILEname
        ):
    ### normal situation
   #cut_func = {
   #        'data': lambda df: df.Filter(f'{binningSTR} && 1'),
   #        'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
   #        'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
   #        'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
   #}

    ### use QCD as fake data now
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && wgt!=0 && wgt < 5'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
    }

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


    use_jetpt_njet_reweight = True
    if use_jetpt_njet_reweight:
        CreateJetPtSF_toTH1(used_df, pETAbin,jETAbin,pPTlow,pPThigh)
        LoadAdditionalFunc()
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

def mainfunc_gjet_binning( outFILEname, inFILEdict:dict, defineWEIGHT:dict, additionalCUT='1' ):
    #CreatePtSF(inFILEdict,additionalCUT)
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

def CreatePtSF(inFILEdict:dict,additionalCUT='1'):
    used_data_frames = frag.UsedDataFrames( **inFILEdict )
    binningSTR = f'photon_pt>210 && {additionalCUT}'
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTR} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = content.define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    CreateJetPtSF_toTH1(used_df, createINTERMEDIATEhist=False)
    LoadAdditionalFunc()

def mainfunc_jet_binning( outFILEname, inFILEdict:dict, additionalCUT='1' ):
    CreatePtSF(inFILEdict,additionalCUT)
    def the_binning( jETAbin, jPTlow, jPThigh, additionalCUT='1' ):
        cuts = f'{additionalCUT} && jet_pt>{jPTlow} && jet_pt<{jPThigh}'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts

    jetptL = [ 0, 100, 210, 230, 250, 300, 400, 500, 600, 1000       ]
    jetptR = [    100, 210, 230, 250, 300, 400, 500, 600, 1000, 1500 ]

    for jEta in range(2):
        for ptL, ptR in zip(jetptL,jetptR):
            used_data_frames = frag.UsedDataFrames( **inFILEdict )

            newfilename = outFILEname.replace('.root',f'__{jEta}_{ptL}_{ptR}.root')
            binning = the_binning(jEta,ptL,ptR, additionalCUT)

            mainfunc(
                    used_data_frames,
                    binning,
                    newfilename
                    )

def mainfunc_gjet_singlebin( outFILEname, inFILEdict:dict, defineWEIGHT:dict, pEta,jEta,ptL,ptR, additionalCUT='1' ):
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

    frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 40,0,1)
    frag.hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b'     , 40,0,1)
    frag.hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l'     , 40,0,1)
   #frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', 5,0,1, 5,0,1)
    frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)',10,0,1,10,0,1)


    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
    import sys

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

    #mainfunc_jet_binning(outfile)
    #mainfunc_gjet_binning(outfile, inFILEdict, define_weight, '1')
    #mainfunc_gjet_binning(outfile, inFILEdict, 'WPb_loose')

    def cut(*cuts): return '(' + '&&'.join(cuts) + ')'
    additional_cut = 'selected_jet_idx==0'
    outfilename = outfile
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut(additional_cut))

    outfilename = outfile.replace('.root', '.WPbL.root')
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut('passWPbL',additional_cut))

    outfilename = outfile.replace('.root', '.WPcM.root')
    mainfunc_gjet_singlebin(outfilename, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, cut('passWPcM',additional_cut))

    #mainfunc_gjet_singlebin(outfile, inFILEdict, define_weight, pETAbin,jETAbin,pPTlow,pPThigh, 'jet_pt>250')
