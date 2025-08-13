#!/usr/bin/env python3
import makehisto_content_estimateSR as content
import makehisto_usefulfunc as frag
import makehisto_GJetPythiaFlatPsuedodata_content_estimateSR as content_psuedo
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc
import ROOT
DATA_LUMINOSITY = 26.81



def mainfunc(
        usedDFs,
        binningSTR:str,
        outFILEname
        ):
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

    used_df = content.define_and_filter(usedDFs, dfCUTfuncs = cut_func, dfDEFfuncs = def_func)
    #CreateJetPtSF_toTH1(used_df, createINTERMEDIATEhist=False)

    ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF
    used_df.dfsign = ddd



    content.main_content(
        usedDF = used_df,
        outputFILE = outFILEname,
        writeOVERFLOWbin = True
    )
    content_psuedo.update_truth(
            usedDF = used_df,
            outputFILE = outFILEname,
            writeOVERFLOWbin = True
            )

    print(f'[OutputFile] {outFILEname}')

def mainfunc_gjet_binning( outFILEname ):
    CreatePtSF()
    def the_binning( pETAbin, jETAbin, pPTlow, pPThigh ):
        cuts = f'photon_pt>{pPTlow} && photon_pt<{pPThigh}'
        if pETAbin == 0: cuts += ' && TMath::Abs(photon_eta)<1.5'
        if pETAbin == 1: cuts += ' && TMath::Abs(photon_eta)>1.5'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts

    ptbinsL = [ 210,230,250,300,400,500,600,1000      ]
    ptbinsR = [     230,250,300,400,500,600,1000,1500 ]

    for pEta in range(2):
        for jEta in range(2):
            for ptL, ptR in zip(ptbinsL,ptbinsR):
                used_data_frames = frag.UsedDataFrames(
                        sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
                        #dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
                        signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
                        dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
                        fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
                )

                newfilename = outFILEname.replace('.',f'{pEta}_{jEta}_{ptL}_{ptR}.')
                binning = the_binning(pEta,jEta,ptL,ptR)
                mainfunc(
                        used_data_frames,
                        binning,
                        newfilename
                        )

def CreatePtSF():
    used_data_frames = frag.UsedDataFrames(
            sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
            #dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
            signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
            dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
            fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
    )
    binningSTR = 'photon_pt>210'
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

def mainfunc_jet_binning( outFILEname ):
    CreatePtSF()
    def the_binning( jETAbin, jPTlow, jPThigh ):
        cuts = f'jet_pt>{jPTlow} && jet_pt<{jPThigh}'
        if jETAbin == 0: cuts += ' && TMath::Abs(jet_eta)<1.5'
        if jETAbin == 1: cuts += ' && TMath::Abs(jet_eta)>1.5'
        return cuts

    jetptL = [ 0, 100, 210, 230, 250, 300, 400, 500, 600, 1000       ]
    jetptR = [    100, 210, 230, 250, 300, 400, 500, 600, 1000, 1500 ]

    for jEta in range(2):
        for ptL, ptR in zip(jetptL,jetptR):
            used_data_frames = frag.UsedDataFrames(
                    sidebandFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
                    #dataFILE     =' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
                    signFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
                    dataFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',
                    fakeFILE     = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
            )

            newfilename = outFILEname.replace('.',f'_{jEta}_{ptL}_{ptR}.')
            binning = the_binning(jEta,ptL,ptR)

            mainfunc(
                    used_data_frames,
                    binning,
                    newfilename
                    )


if __name__ == "__main__":
    import sys

    outfile = sys.argv[1] if len(sys.argv) > 1 else 'makehisto_psuedodata_rescaled.root'
    ROOT.EnableImplicitMT()

    #### redefine the histogram
    #frag.hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
    #frag.hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )


    mainfunc_jet_binning(outfile)
