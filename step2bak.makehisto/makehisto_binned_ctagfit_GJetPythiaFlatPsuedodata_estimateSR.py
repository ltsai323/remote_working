#!/usr/bin/env python3
import makehisto_usefulfunc as frag
frag.hbtag = lambda tag: ( f'{tag}_btag', 'b tag score', 40, 0.,1.)
frag.hcvsb = lambda tag: ( f'{tag}_cvsb', 'c vs b', 40, 0,1.)
frag.hcvsl = lambda tag: ( f'{tag}_cvsl', 'c vs l', 40, 0.,1.)
frag.h2DcvsbANDcvsl = lambda tag: (f'{tag}_cvsbANDcvsl', 'X(cvsb) Y(cvsl)', 20,0,1, 20,0,1)
import makehisto_ctagfit_estimateSR as content
import makehisto_GJetPythiaFlatPsuedodata_ctagfit_estimateSR as content_psuedo
from makehisto_usefulfunc import CreateJetPtSF_toTH1, UpdateEvtWeight_ReweightJetPtFromGJetandQCD, UpdateEvtWeight_ReweightJetPtFromGJet, LoadAdditionalFunc
import ROOT
DATA_LUMINOSITY = 26.81
#DATA_LUMINOSITY = 27.01



def mainfunc(
        usedDFs,
        binningSTR:str, binningSTRsideband:str,
        defFUNC:dict,
        outFILEname
        ):
    cut_func = {
            'data': lambda df: df.Filter(f'{binningSTR} && 1'),
            'sign': lambda df: df.Filter(f'{binningSTR} && 1'),
            'fake': lambda df: df.Filter(f'{binningSTR} && 1'),
            'side': lambda df: df.Filter(f'{binningSTRsideband} && 1'),
    }
    #def_func = {
    #        'data': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"),
    #        'sign': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
    #        'fake': lambda df: df.Define('event_weight',f"wgt * {DATA_LUMINOSITY}"), # gen weight, xs norm, PU weight, photon SF, trigger SF
    #        'side': lambda df: df.Define('event_weight','1'),
    #}

    used_df = content.define_and_filter(usedDFs, dfCUTfuncs = cut_func, dfDEFfuncs = defFUNC)
    #CreateJetPtSF_toTH1(used_df, createINTERMEDIATEhist=False)

    ddd = UpdateEvtWeight_ReweightJetPtFromGJet(used_df.dfsign, makehistoADDITIONALfunctions_LOADED = True) ## update event_weight with jetPtSF
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
    CreatePtSF(inFILEdict,additionalCUT) # tmptmp
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
                        defineWEIGHT,
                        newfilename
                        )

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


if __name__ == "__main__":
    import sys

    outfile = sys.argv[1] if len(sys.argv) > 1 else 'makehisto_psuedodata_rescaled.root'
    ROOT.EnableImplicitMT()

    #### redefine the histogram
    #frag.hSVmAll = lambda tag: ( f'{tag}_SVmAll', 'SV mass including -1', 80, -1, 15 )
    #frag.hSVmAct = lambda tag: ( f'{tag}_SVmAct', 'SV mass with SV constructed', 75, 0, 15 )

    inFILEdict = {
        'sidebandFILE': '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataDataSideband.root',
       #'dataFILE'    :' /afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetDataSignalRegion.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJetMadgraph.root',
       #'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_QCDMadgraph.root',
        'dataFILE'    : '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/stage2/stage2_GJetMCGJeyPythiaFlat.root',

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
    mainfunc_gjet_binning(outfile, inFILEdict, define_weight, '1')
    #mainfunc_gjet_binning(outfile, inFILEdict, 'WPb_loose')
    #mainfunc_gjet_binning(outfile, 'WPb_medium')
    #mainfunc_gjet_binning(outfile, 'WPb_tight')
    #mainfunc_gjet_binning(outfile, 'WPc_loose')
    #mainfunc_gjet_binning(outfile, 'WPc_medium')
    #mainfunc_gjet_binning(outfile, 'WPc_tight')
