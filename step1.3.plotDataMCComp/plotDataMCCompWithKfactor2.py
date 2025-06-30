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

class histCollection:
    def __init__(self):
        pass
    def WriteAllHists(self, fOUT):
        fOUT.cd()
        for hname, hinst in vars(self).items():
            hinst.Write()
def TakeRatio(outHISTname, hUPPER:ROOT.TH1F, hLOWER:ROOT.TH1F):
    hU = hUPPER
    hL = hLOWER
    for ibin in range(1,hL.GetNbinsX()+2):
        if hL.GetBinContent(ibin) == 0: hL.SetBinContent(ibin, 1e-8)
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio
def take_ratio_in_obj(obj, insU:str, insDs:list, outTAG):
    # getvalue convert TH1DModel to TH1D
    hU = getattr(obj,insU).GetValue()
    hDs = []
    for insD in insDs:
        hDs.append( getattr(obj,insD).GetValue() )

    hD = None
    for _hD in hDs:
        if hD == None: hD = _hD.Clone()
        else: hD.Add(_hD)
    if hD is None:
        print(f'W@[No any denominator hists] hists "{insDs}" does not get any histograms')
        return



    sumNAME = f'{outTAG}_MCsum'
    hD.SetName(sumNAME)
    setattr(obj,sumNAME,hD)

    ratioNAME = f'{outTAG}_ratio'
    ratio = TakeRatio(ratioNAME, hU, hD)
    setattr(obj,ratioNAME, ratio)
    print(f'[GenerateRatio] {ratioNAME} generate from {hU.GetName()} / {hD.GetName()}')

def mainfunc(dataFILE, signFILE, fakeFILE, outFILE):
    hists = histCollection()

    dfdata = ROOT.RDataFrame('tree', dataFILE)
    dffake = ROOT.RDataFrame('tree', fakeFILE)
    dfsign = ROOT.RDataFrame('tree', signFILE)


    df_data = dfdata.Define('event_weight', '1')
    df_fake = dffake.Define('event_weight', 'wgt * 26.67') # contains photon sf, jet smear, gen weight, xs weight, luminosity(?), pileup, trigger SF
    df_sign = dfsign.Define('event_weight', 'wgt * 26.67') # contains photon sf, jet smear, gen weight, xs weight, luminosity(?), pileup, trigger SF


    def store(h):
        setattr(hists, h.GetName(), h)
    def draw(binning, var, oTAG):
        store( df_data.Histo1D( binning(f'{oTAG}_data'), var) )
        store( df_fake.Histo1D( binning(f'{oTAG}_fake'), var, 'event_weight') )
        store( df_sign.Histo1D( binning(f'{oTAG}_sign'), var, 'event_weight') )
        take_ratio_in_obj(hists, f'{oTAG}_data', [f'{oTAG}_sign',f'{oTAG}_fake'], oTAG)

    #BIN_PHOPT = lambda n: ROOT.ROOT.RDF.TH1DModel( f'phopt_{n}', 'pt', len(pts)-1, array('f',pts) )
    BIN_PHOPT  = lambda n: ROOT.ROOT.RDF.TH1DModel(n, 'pt', 40, 200.,1000.)
    draw(BIN_PHOPT, 'photon_pt', 'phopt')
    draw(BIN_PHOPT, 'jet_pt', 'jetpt')


    BIN_ETA = lambda n: ROOT.ROOT.RDF.TH1DModel(n, 'eta', 40, -3.5, 3.5)
    draw(BIN_ETA, 'photon_eta', 'phoeta')
    draw(BIN_ETA, 'jet_eta', 'jeteta')
    BIN_PHI = lambda n: ROOT.ROOT.RDF.TH1DModel(n, 'phi', 40, -3.5, 3.5)
    draw(BIN_PHI, 'photon_phi', 'phophi')
    draw(BIN_PHI, 'jet_phi', 'jetphi')
    #BIN_CHISO = lambda n: ROOT.ROOT.RDF.TH1DModel(n, 'charge isolation', 40, 0., 15.)
    #draw(BIN_CHISO, 'photon_chiso', 'chiso')
    BIN_SIEIE = lambda n: (n, 'sieie', 40, 0., 0.1)
    draw(BIN_SIEIE, 'photon_pfChargedIsoPFPV', 'chiso')

    BIN_HOE = lambda n: (n, 'H over E', 40, 0., 0.055)
    draw(BIN_SIEIE, 'photon_hoe', 'hoe')

    BIN_SVMASS = lambda n: (n, 'SV mass', 40, 0., 10.)
    draw(BIN_SVMASS, 'jet_SVmass', 'SVmass')

    BIN_SVPT   = lambda n: (n, 'SV mass', 40, 0., 300.)
    draw(BIN_SVPT, 'jet_SVmass', 'SVpt')

    BIN_SVnTRACK = lambda n: (n, 'SV nTracks', 18, 0., 18.)
    draw(BIN_SVnTRACK, 'jet_SVntracks', 'SVnTracks')

    BIN_nSV = lambda n: (n, 'SV multiplicity', 10, 0., 10.)
    draw(BIN_nSV, 'jet_nSV', 'nSV')


    BIN_nJET = lambda n: (n, 'Jet multiplicity', 10, 0., 10.)
    draw(BIN_nSV, 'jet_multiplicity', 'nJET')


    f_out = ROOT.TFile(outFILE, 'recreate')
    hists.WriteAllHists(f_out)
    f_out.Close()
    





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
    #MainFunc()
    datafile = '/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_GJetDataSignalRegion.root'
    fakefile = '/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_QCDMadgraph.root'
    signfile = '/home/ltsai/ReceivedFile/GJet/latestsample/2022EE_MiniAODv12/stage2/stage2_GJetMCGJetMadgraph.root'

    outfile = 'o.root'
    mainfunc(datafile,signfile,fakefile, outfile)

