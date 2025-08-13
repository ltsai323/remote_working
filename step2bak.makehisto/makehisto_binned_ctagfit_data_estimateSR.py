#!/usr/bin/env python3
import makehisto_ctagfit_estimateSR as content
import makehisto_usefulfunc as frag
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc
import ROOT
DATA_LUMINOSITY = 26.81



def mainfunc(
        usedDFs,
        binningSTR:str, binningSTRsideband:str,
        reweightJETpt:bool,
        outFILEname
        ):
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight',f"1"),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = content.define_and_filter(usedDFs, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    #CreateJetPtSF_toTH1(used_df, createINTERMEDIATEhist=False) ## comment out because we calculate the PtSF before binning

    if reweightJETpt:
        ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF, used histogram should be created beforehand
        used_df.dfsign = ddd



    content.main_content(
        usedDF = used_df,
        outputFILE = outFILEname,
    )

    print(f'[OutputFile] {outFILEname}')

def mainfunc_gjet_binning( outFILEname, additionalCUT='1' ):
    CreatePtSF(additionalCUT)
    def the_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1' ):
        cuts = f'{additionalCUT} && photon_pt>{pPTlow} && photon_pt<{pPThigh}'
        if pETAbin == 0: cuts += ' && TMath::Abs(photon_eta)<1.5'
        if pETAbin == 1: cuts += ' && TMath::Abs(photon_eta)>1.5'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts
    def the_sideband_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1'):
        # use previous 2 bin as sideband increasing statisticcs
        if pPTlow > 600:
            print(f'[RedefineSideband] Bin({pETAbin},{jETAbin},{pPTlow},{pPThigh}) use additional sideband Bin({pETAbin},{jETAbin},600,1000)')
        return the_binning(pETAbin,jETAbin,pPTlow,pPThigh,additionalCUT) if pPTlow < 600 else the_binning(pETAbin,jETAbin,600,1000,additionalCUT)


    ptbinsL = [ 210,230,250,300,400,500,600,1000      ]
    ptbinsR = [     230,250,300,400,500,600,1000,1500 ]

    for pEta in range(2):
        for jEta in range(2):
            for ptL, ptR in zip(ptbinsL,ptbinsR):
                used_data_frames = frag.UsedDataFrames(
                        sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
                        dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
                        signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
                       #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
                        fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
                )

                newfilename = outFILEname.replace('.root',f'__{pEta}_{jEta}_{ptL}_{ptR}.root')
                binning = the_binning(pEta,jEta,ptL,ptR, additionalCUT)
                binning_sideband = the_sideband_binning(pEta,jEta,ptL,ptR, additionalCUT)
                mainfunc(
                        used_data_frames,
                        binning, binning_sideband,
                        False, # not to reweight jet pt
                        newfilename
                        )

def testfunc_specific_sideband_cut():
    def the_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1' ):
        cuts = f'{additionalCUT} && photon_pt>{pPTlow} && photon_pt<{pPThigh}'
        if pETAbin == 0: cuts += ' && TMath::Abs(photon_eta)<1.5'
        if pETAbin == 1: cuts += ' && TMath::Abs(photon_eta)>1.5'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts
    def the_sideband_binning( pETAbin, jETAbin, pPTlow, pPThigh, additionalCUT='1'):
        # use previous 2 bin as sideband increasing statisticcs
        print(f'[sideband check] pPTlow("{ pPTlow }") > 600 ? "{ pPTlow>600 }"')
        return the_binning(pETAbin,jETAbin,pPTlow,pPThigh,additionalCUT) if pPTlow < 600 else the_binning(pETAbin,jETAbin,600,1000,additionalCUT)


    ptbinsL = [ 500,600,1000      ]
    ptbinsR = [     600,1000,1500 ]

    outFILEname = 'testfunc.root'
    additionalCUT = '1'
    for pEta in range(2):
        for jEta in range(2):
            for ptL, ptR in zip(ptbinsL,ptbinsR):
                used_data_frames = frag.UsedDataFrames(
                        sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
                        dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
                        signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
                       #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
                        fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
                )

                newfilename = outFILEname.replace('.root',f'__{pEta}_{jEta}_{ptL}_{ptR}.root')
                binning = the_binning(pEta,jEta,ptL,ptR, additionalCUT)
                binning_sideband = the_sideband_binning(pEta,jEta,ptL,ptR, additionalCUT)
                mainfunc(
                        used_data_frames,
                        binning, binning_sideband,
                        False, # not to reweight jet pt
                        newfilename
                        )
    exit()

def CreatePtSF(additionalCUT='1'):
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
           #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )
    binningSTR = f'photon_pt>210 && {additionalCUT}'
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTR} && 1'),
    }
    def_func = {
            'data': lambda df: df.Define('event_weight','1'),
            'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
            'side': lambda df: df.Define('event_weight','1'),
    }

    used_df = content.define_and_filter(used_data_frames, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    CreateJetPtSF_toTH1(used_df, createINTERMEDIATEhist=False)
    LoadAdditionalFunc()

def mainfunc_jet_binning( outFILEname, additionalCUT='1' ):
    CreatePtSF(additionalCUT)
    def the_binning( jETAbin, jPTlow, jPThigh, additionalCUT='1' ):
        cuts = f'{additionalCUT} && jet_pt>{jPTlow} && jet_pt<{jPThigh}'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts

    jetptL = [ 0, 100, 210, 230, 250, 300, 400, 500, 600, 1000       ]
    jetptR = [    100, 210, 230, 250, 300, 400, 500, 600, 1000, 1500 ]

    for jEta in range(2):
        for ptL, ptR in zip(jetptL,jetptR):
            used_data_frames = frag.UsedDataFrames(
                    sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
                    dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
                    signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
                   #dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
                    fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
            )

            newfilename = outFILEname.replace('.root',f'__{jEta}_{ptL}_{ptR}.root')
            binning = the_binning(jEta,ptL,ptR, additionalCUT)

            mainfunc(
                    used_data_frames,
                    binning,
                    True, # reweight jet pt
                    newfilename
                    )



if __name__ == "__main__":
    #testfunc_specific_sideband_cut()
    import sys
    if len(sys.argv) == 1:
        # no any argument, show help
        print(f'[help] arg1: output fiolename=makehisto_psuedodata_rescaled.root    arg2: additional cut=WPb_loose')
        exit()

    outfile = sys.argv[1] if len(sys.argv) > 1 else 'makehisto_psuedodata_rescaled.root'
    additional_cut = sys.argv[2] if len(sys.argv) > 2 else '1'

    AVAILABLE_CUT_OPTIONS = [ '1', 'WPb_loose', 'WPb_medium', 'WPb_tight', 'WPc_loose', 'WPc_medium', 'WPc_tight' ]
    if additional_cut not in AVAILABLE_CUT_OPTIONS:
        raise IOError(f'[CutNotAvailable] arg2 "{ additional_cut }" is an invalid cut, the available cuts are "{ AVAILABLE_CUT_OPTIONS }"')
    print(f'[MakehistoBinned] additional cut "{additional_cut}" for output file "{outfile}"')
    ROOT.EnableImplicitMT()

    #### redefine the histogram
    #frag.hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
    #frag.hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )


    mainfunc_gjet_binning(outfile, additional_cut)
    #mainfunc_jet_binning(outfile)
    #mainfunc_gjet_binning(outfile, '1')
    #mainfunc_gjet_binning(outfile, 'WPb_loose')
    #mainfunc_gjet_binning(outfile, 'WPb_medium')
    #mainfunc_gjet_binning(outfile, 'WPb_tight')
    #mainfunc_gjet_binning(outfile, 'WPc_loose')
    #mainfunc_gjet_binning(outfile, 'WPc_medium')
    #mainfunc_gjet_binning(outfile, 'WPc_tight')
