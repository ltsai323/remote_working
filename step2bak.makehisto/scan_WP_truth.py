#!/usr/bin/env python3
import makehisto_content_estimateSR as content
import makehisto_usefulfunc as frag
import makehisto_GJetPythiaFlatPsuedodata_content_estimateSR as content_psuedo
import ROOT
from uncertanties import ufloat
DATA_LUMINOSITY = 26.81

def update_truth( usedDF: frag.UsedDataFrames, outputFILE, writeOVERFLOWbin=False):
    the_data = usedDF.dfSR
    the_sign = usedDF.dfsign
    the_fake = usedDF.dffake
    the_side = usedDF.dfSB




    class Yields:
        def __init__(self, oTAG, l,c,b):
            self.tag = oTAG
            self.l = l
            self.c = c
            self.b = b

            sumup = l+c+b
            self.fracl = l / sumup
            self.fracc = c / sumup
            self.fracb = b / sumup
    def get_yields(oTAG, dfDATA) -> Yields:
        df_data = content.DefineJetTruth(dfDATA)
        dfTruthL = df_data.Filter('isLJet')
        dfTruthC = df_data.Filter('isCJet')
        dfTruthB = df_data.Filter('isBJet')

        class NameSet:
            def __init__(self, varNAME):
                self.truthL = f'data_{varNAME}_truthL'
                self.truthC = f'data_{varNAME}_truthC'
                self.truthB = f'data_{varNAME}_truthB'
                self.truthSUM = f'data_{varNAME}_truthSUM'
            names = NameSet(oTAG)
            hists = frag.histCollection()

        def sum_hist(newTITLE, h1, h2, h3 ):
            h = h1.Clone(newTITLE)
            h.Add(h2.GetValue())
            h.Add(h3.GetValue())
            return h


        ### all entries
        truthL = dfTruthL.Histo1D( frag.hBDTAll(names.truthL), 'photon_mva', 'event_weight' )
        truthC = dfTruthC.Histo1D( frag.hBDTAll(names.truthC), 'photon_mva', 'event_weight' )
        truthB = dfTruthB.Histo1D( frag.hBDTAll(names.truthB), 'photon_mva', 'event_weight' )

        def yieldFromHist(h):
            val = h.Integral()
            err = sum( h.GetBinError(ii)**2 for ii in range(1, h.GetNbinsX()+1) ) ** 0.5
            return ufloat(val,err)
        yieldL = yieldFromHist(truthL)
        yieldC = yieldFromHist(truthC)
        yieldB = yieldFromHist(truthB)

        return Yields(oTAG, yieldL,yieldC,yieldB)




    allgjet_yields = get_yields( 'allgjets', the_data )
    WPbL_yields = get_yields( 'WPbLoose', the_data.Filter('WPb_loose'),)
    WPbM_yields = get_yields( 'WPbMedium', the_data.Filter('WPb_medium'),)
    WPbT_yields = get_yields( 'WPbTight', the_data.Filter('WPb_tight'),)
    WPcL_yields = get_yields( 'WPcLoose', the_data.Filter('WPc_loose'),)
    WPcM_yields = get_yields( 'WPcMedium', the_data.Filter('WPc_medium'),)
    WPcT_yields = get_yields( 'WPcTight', the_data.Filter('WPc_tight'),)

    ############ ploting ended ##########

    f_out = ROOT.TFile(outputFILE, 'update')
    h_allgjets.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPbLoose.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPbMedium.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPbTight.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPcMedium.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    h_WPcTight.WriteAllHists(f_out, writeOVERFLOWbin=writeOVERFLOWbin)
    f_out.Close()

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

def mainfunc_jet_binning( outFILEname ):
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

