#!/usr/bin/env python3

import ROOT
debug_mode = False
DEBUG_EVENT = 1000
full_mode = False
def BUG(mesg):
    if debug_mode:
        print(f'[BUG] {mesg}')


def draw(inTREE:ROOT.TTree,
        varNAME:str, outTAG:str, xAXIS:str,
        evtCUT:str, evtWEIGHT:str,
        binning:tuple=() ):
    histNAME = '_'.join((outTAG,xAXIS))
    v=f'{varNAME} >> {histNAME}'
    #print(f'drawing hist {histNAME}')
    if len(binning)>0:
        v+=f'({binning[0]:d},{binning[1]:.2f},{binning[2]:.2f})'
    print(f'ttree.Draw("{v}", "({evtCUT})*{evtWEIGHT}"')
    inTREE.Draw(v, f'({evtCUT})*{evtWEIGHT}')

    h = ROOT.gROOT.FindObject(histNAME)
    h.GetXaxis().SetTitle(xAXIS)
    h.SetTitle(varNAME)

    return h

def event_cut( additionalCUT:str='1'):
    def all_cuts(*args):
        return '&&'.join(args).replace('  ',' ')
    basic_cut = '&&'.join(['phoFillIdx==0', 'eleVeto==1', 'jetPt>30.', 'fabs(jetEta)<2.4', 'jetPUIDbit == 7', 'jetID==1']) # jetID == 1 is loose ID
    barrel_pho = '&&'.join(['fabs(recoSCEta)<1.4442'                       , 'HoverE<0.08', 'sieieFull5x5 < 0.012', 'phoIsoRaw<15.', 'chWorstIso<15.'])
    endcap_pho = '&&'.join(['fabs(recoSCEta)>1.566' , 'fabs(recoSCEta)<2.5', 'HoverE<0.05', 'sieieFull5x5 < 0.027', 'phoIsoRaw<15.', 'chWorstIso<15.'])
    all_pho = f'( ({barrel_pho}) || ({endcap_pho}) )'


    #return all_cuts( basic_cut, barrel_pho, additionalCUT )
    #return all_cuts( basic_cut, endcap_pho, additionalCUT )
    return all_cuts( basic_cut, all_pho, additionalCUT )

BINNING_PHOPT = (100, 190.,1000.)
BINNING_PHOETA= (40, -2.5, 2.5)
BINNING_PHOPHI= (40,-4.,4.)
BINNING_CHISO = (40, 0., 15.)
BINNING_N_VTX = (50, 0., 50.)
BINNING_JETPT = (100, 0., 1000.)
BINNING_SCORE = (20, 0.,1,)

def DrawData(inTREE, outTAG, additionalCUT:str = '1'):
    nTEMP = 'data_%s'
    evtWEIGHT = '1'
    evtCUT = event_cut( '&&'.join([additionalCUT, 'recoPtCalib>190 && (((phoFiredTrgs>>7)&1)==1)']) )

    hists = {}
    hists['phoPt' ] = draw(inTREE,'recoPtCalib',outTAG,'phoPt' , evtCUT, evtWEIGHT, BINNING_PHOPT )
    hists['phoEta'] = draw(inTREE,'recoEta'    ,outTAG,'phoEta', evtCUT, evtWEIGHT, BINNING_PHOETA)
    hists['phoETA'] = draw(inTREE,'recoSCEta'  ,outTAG,'phoETA', evtCUT, evtWEIGHT, BINNING_PHOETA)
    hists['phoPhi'] = draw(inTREE,'recoPhi'    ,outTAG,'phoPhi', evtCUT, evtWEIGHT, BINNING_PHOPHI)
    hists['chiso' ] = draw(inTREE,'chIsoRaw'   ,outTAG,'chiso' , evtCUT, evtWEIGHT, BINNING_CHISO )
    hists['nVtx'  ] = draw(inTREE,'nVtx'       ,outTAG,'nVtx'  , evtCUT, evtWEIGHT, BINNING_N_VTX )
    hists['jetPt' ] = draw(inTREE,'jetPt'      ,outTAG,'jetPt' , evtCUT, evtWEIGHT, BINNING_JETPT )

    hists['DeepFlavour_bScore'] = draw(inTREE, 'DeepFlavour.bScore',outTAG,'DeepFlavour_bScore' , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepFlavour_CvsL'  ] = draw(inTREE, 'DeepFlavour.CvsL'  ,outTAG,'DeepFlavour_CvsL'   , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepFlavour_CvsB'  ] = draw(inTREE, 'DeepFlavour.CvsB'  ,outTAG,'DeepFlavour_CvsB'   , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepCSV_bScore'    ] = draw(inTREE, 'DeepCSV.bScore'    ,outTAG,'DeepCSV_bScore'     , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepCSV_CvsL'      ] = draw(inTREE, 'DeepCSV.CvsL'      ,outTAG,'DeepCSV_CvsL'       , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepCSV_CvsB'      ] = draw(inTREE, 'DeepCSV.CvsB'      ,outTAG,'DeepCSV_CvsB'       , evtCUT, evtWEIGHT, BINNING_SCORE)
    return hists
def DrawMC_DeepFlavour(inTREE, outTAG,additionalCUT:str = '1',  evtWEIGHT:str='1'):
    evtCUT = event_cut( '&&'.join([additionalCUT, 'recoPt>190.']) )

    hists = {}
    hists['DeepFlavour_bScore'] = draw(inTREE, 'DeepFlavour.bScore',outTAG,'DeepFlavour_bScore' , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepFlavour_CvsL'  ] = draw(inTREE, 'DeepFlavour.CvsL'  ,outTAG,'DeepFlavour_CvsL'   , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepFlavour_CvsB'  ] = draw(inTREE, 'DeepFlavour.CvsB'  ,outTAG,'DeepFlavour_CvsB'   , evtCUT, evtWEIGHT, BINNING_SCORE)
    return hists
def DrawMC_DeepCSV(inTREE, outTAG,additionalCUT:str = '1',  evtWEIGHT:str='1'):
    evtCUT = event_cut( '&&'.join([additionalCUT, 'recoPt>190.']) )

    hists = {}
    hists['DeepCSV_bScore'    ] = draw(inTREE, 'DeepCSV.bScore'    ,outTAG,'DeepCSV_bScore'     , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepCSV_CvsL'      ] = draw(inTREE, 'DeepCSV.CvsL'      ,outTAG,'DeepCSV_CvsL'       , evtCUT, evtWEIGHT, BINNING_SCORE)
    hists['DeepCSV_CvsB'      ] = draw(inTREE, 'DeepCSV.CvsB'      ,outTAG,'DeepCSV_CvsB'       , evtCUT, evtWEIGHT, BINNING_SCORE)
    return hists
def DrawMC(inTREE, outTAG,additionalCUT:str = '1',  evtWEIGHT:str='1'):
    evtCUT = event_cut( '&&'.join([additionalCUT, 'recoPt>190.']) )

    hists = {}
    hists['phoPt' ] = draw(inTREE,'recoPt'     ,outTAG,'phoPt' , evtCUT, evtWEIGHT, BINNING_PHOPT )
    hists['phoEta'] = draw(inTREE,'recoEta'    ,outTAG,'phoEta', evtCUT, evtWEIGHT, BINNING_PHOETA)
    hists['phoETA'] = draw(inTREE,'recoSCEta'  ,outTAG,'phoETA', evtCUT, evtWEIGHT, BINNING_PHOETA)
    hists['phoPhi'] = draw(inTREE,'recoPhi'    ,outTAG,'phoPhi', evtCUT, evtWEIGHT, BINNING_PHOPHI)
    hists['chiso' ] = draw(inTREE,'chIsoRaw'   ,outTAG,'chiso' , evtCUT, evtWEIGHT, BINNING_CHISO )
    hists['nVtx'  ] = draw(inTREE,'nVtx'       ,outTAG,'nVtx'  , evtCUT, evtWEIGHT, BINNING_N_VTX )
    hists['jetPt' ] = draw(inTREE,'jetPt'      ,outTAG,'jetPt' , evtCUT, evtWEIGHT, BINNING_JETPT )
    return hists

class TFileAndTree:
    def __init__(self,inFILEname:str):
        self.tfile = ROOT.TFile.Open(inFILEname)
        ttree = self.tfile.Get('t')
        from testmodule_smalltree import GetSmallTree
        self.ttree = GetSmallTree(ttree, DEBUG_EVENT) if debug_mode else ttree

def MainFunc():
    #datafile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/data.root'         )
    #fakefile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/qcd.madgraph.root' )
    ##signfile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/sig.pythia.root'   )
    #signfile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/sig.madgraph.root' )

    datafile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_GJetDataSignalRegion.root')
    fakefile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_QCDMadgraph.root')
    signfile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_GJetMCGJetMadgraph.root')
    #signfile = TFileAndTree('/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_GJetPythiaFlat.root')


    strict_C_selection = 'jetSubVtx3DVal/jetSubVtx3DErr>8. && jetSubVtxNtrks>2'
    drawing_hists = []
    drawing_hists.append( DrawData(datafile.ttree, 'expdata') )
    drawing_hists.append( DrawData(datafile.ttree, 'expdataStrictC', strict_C_selection) )
    # all weights
    drawing_hists.append( DrawMC  ( signfile.ttree, 'signALL',
            'isMatched==1', 'mcweight *puwei * scalefactor_photon * jetP4Smear') )

    drawing_hists.append( DrawMC_DeepCSV    ( signfile.ttree, 'signDeepCSVOrig',
            'isMatched==1', 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
    drawing_hists.append( DrawMC_DeepCSV    ( signfile.ttree, 'signDeepCSVCalib',
            'isMatched==1', 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepCSV.ctagWeight.central'    ) )
    drawing_hists.append( DrawMC_DeepCSV    ( signfile.ttree, 'signDeepCSVOrigStrictC',
            '&&'.join(['isMatched==1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
    drawing_hists.append( DrawMC_DeepCSV    ( signfile.ttree, 'signDeepCSVCalibStrictC',
            '&&'.join(['isMatched==1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepCSV.ctagWeight.central'    ) )

    if full_mode:
        drawing_hists.append( DrawMC_DeepFlavour( signfile.ttree, 'signDeepFlavourOrig',
                'isMatched==1', 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
        drawing_hists.append( DrawMC_DeepFlavour( signfile.ttree, 'signDeepFlavourCalib',
                'isMatched==1', 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepFlavour.ctagWeight.central') )
        drawing_hists.append( DrawMC_DeepFlavour( signfile.ttree, 'signDeepFlavourOrigStrictC',
                '&&'.join(['isMatched==1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
        drawing_hists.append( DrawMC_DeepFlavour( signfile.ttree, 'signDeepFlavourCalibStrictC',
                '&&'.join(['isMatched==1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepFlavour.ctagWeight.central') )

    if full_mode:
        # only luminosity weight
        drawing_hists.append( DrawMC  ( signfile.ttree, 'sign0',
                'isMatched==1', 'mcweight') )
        # lunminosity wieght + puwei
        drawing_hists.append( DrawMC  ( signfile.ttree, 'sign1',
                'isMatched==1', 'mcweight *puwei') )
         # lumi + pho sf
        drawing_hists.append( DrawMC  ( signfile.ttree, 'sign2',
                'isMatched==1', 'mcweight * scalefactor_photon') )
         # lumi + jetP4Smear
        drawing_hists.append( DrawMC  ( signfile.ttree, 'sign3',
                'isMatched==1', 'mcweight * jetP4Smear') )

    # all weights
    drawing_hists.append( DrawMC  ( fakefile.ttree, 'fakeALL',
            'isMatched!=1', 'mcweight *puwei * scalefactor_photon* jetP4Smear') )

    drawing_hists.append( DrawMC_DeepCSV    ( fakefile.ttree, 'fakeDeepCSVOrig',
            'isMatched!=1', 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
    drawing_hists.append( DrawMC_DeepCSV    ( fakefile.ttree, 'fakeDeepCSVCalib',
            'isMatched!=1', 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepCSV.ctagWeight.central'    ) )
    drawing_hists.append( DrawMC_DeepCSV    ( fakefile.ttree, 'fakeDeepCSVOrigStrictC',
            '&&'.join(['isMatched!=1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
    drawing_hists.append( DrawMC_DeepCSV    ( fakefile.ttree, 'fakeDeepCSVCalibStrictC',
            '&&'.join(['isMatched!=1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepCSV.ctagWeight.central'    ) )

    if full_mode:
        drawing_hists.append( DrawMC_DeepFlavour( fakefile.ttree, 'fakeDeepFlavourOrig',
                'isMatched!=1', 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
        drawing_hists.append( DrawMC_DeepFlavour( fakefile.ttree, 'fakeDeepFlavourCalib',
                'isMatched!=1', 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepFlavour.ctagWeight.central') )
        drawing_hists.append( DrawMC_DeepFlavour( fakefile.ttree, 'fakeDeepFlavourOrigStrictC',
                '&&'.join(['isMatched!=1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear ') )
        drawing_hists.append( DrawMC_DeepFlavour( fakefile.ttree, 'fakeDeepFlavourCalibStrictC',
                '&&'.join(['isMatched!=1',strict_C_selection]), 'mcweight *puwei * scalefactor_photon* jetP4Smear * DeepFlavour.ctagWeight.central') )

    if full_mode:
        # only luminosity weight
        drawing_hists.append( DrawMC  ( fakefile.ttree, 'fake0',
                'isMatched!=1', 'mcweight') )
         # lunminosity wieght + puwei
        drawing_hists.append( DrawMC  ( fakefile.ttree, 'fake1',
                'isMatched!=1', 'mcweight *puwei') )
         # lumi + pho sf
        drawing_hists.append( DrawMC  ( fakefile.ttree, 'fake2',
                'isMatched!=1', 'mcweight *scalefactor_photon') )
         # lumi + jetP4Smear
        drawing_hists.append( DrawMC  ( fakefile.ttree, 'fake3',
                'isMatched!=1', 'mcweight * jetP4Smear') )
         # lumi + pass max pu
        drawing_hists.append( DrawMC  ( fakefile.ttree, 'fake4',
                'isMatched!=1&&passMaxPUcut', 'mcweight * weight_passMaxPUcut') )



    outfile = ROOT.TFile('dataMCcomp.root', 'recreate')
    def writeTo(outFILE, histDICT):
        try:
            first_key = list(histDICT.keys())[0]
            BUG(f'Writing directory "{ first_key }" to ROOT file.')
        except IndexError as e:
            raise IndexError(f'writeTo() said nothing inside this histogram dictionary. Terminate process... (histDICT = {histDICT})')
        dirName = histDICT[first_key].GetName().split('_')[0]
        BUG(f'Creating directory "{ dirName }"')
        tdir = outFILE.mkdir(dirName)
        tdir.cd()
        for objname, hist in histDICT.items():
            hist.SetName(objname)
            hist.Write()

    for drawn_hists in drawing_hists:
        writeTo(outfile, drawn_hists)

    outfile.Close()









if __name__ == "__main__":
    MainFunc()

