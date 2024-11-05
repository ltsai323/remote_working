#!/usr/bin/env python3
import ROOT

import ExternalFileMgr


def Binning(df, pETAbin, jETAbin, pPTlow, pPThigh):
    phoEtaCut = 'fabs(recoEta)<1.5' if pETAbin == 0 else 'fabs(recoEta)>1.5'
    jetEtaCut = 'fabs( jetY)<1.5 && jetPt>0' if jETAbin == 0 else 'fabs( jetY)>1.5 && jetPt>0'
    phoPtCut = f'photon_pt>{pPTlow} && photon_pt<{pPThigh}'
    return df.Filter( '&&'.join([phoEtaCut,jetEtaCut, phoPtCut]) )

def GeneralSelection(df):
    ### asdf need to load JEC and JER
    return df.Filter( '&&'.join([
        '!(fabs(recoSCEta)>1.4442&&fabs(recoSCEta)<1.566)', # fidual region cut
        'fabs(recoSCEta)<2.5', # fidual region cut
        '!(fabs(recoSCEta)<1.5 && (sieieFull5x5>0.012 || HoverE>0.08))', # fidual region cut
        '!(fabs(recoSCEta)>1.5 && (sieieFull5x5>0.027 || HoverE>0.05))', # fidual region cut
        'eleVeto!=0',
        'phoFillIdx==0', # leading photon
        
        'jetPt>0',
        'fabs(jetEta)<2.4',
        'jetSubVtxMass!=0',

        ]) )
def SignSelection(df):
    return GeneralSelection( df.Filter('jetID==1 && jetPUIDbit==7 && isMatched==1') )
def FakeSelection(df):
    return GeneralSelection( df.Filter('jetID==1 && jetPUIDbit==7 && isMatched!=1') )
def DataSelection(df):
    return GeneralSelection( df.Filter('( (phoFiredTrgs>>7)&1 )') ) # HLT175


def DefineSignalAndSideband(df, isDATA):
    #ch_iso = 'calib_chIso' if isDATA else 'chIsoRaw'
    return df \
        .Define('phoSignalRegion', '(fabs(recoEta)<1.5 && charge_isolation<2.0) || (fabs(recoEta)>1.5 && charge_isolation<1.5)') \
        .Define('phoDataSideband', '(fabs(recoEta)<1.5 && charge_isolation>7.0 && charge_isolation<13.0) || (fabs(recoEta)>1.5 && charge_isolation>6.0&&charge_isolation<12.0)')
def DefineJetTruth(df):
    return df \
        .Define('isLJet', 'jetHadFlvr == 0') \
        .Define('isCJet', 'jetHadFlvr == 4') \
        .Define('isBJet', 'jetHadFlvr == 5')


def h_BDT(hNAME, hDESC):
    return (hNAME, hDESC, 20, -1.,1.)
def h_CTagVar(hNAME, hDESC):
    return (hNAME, hDESC, 20,  0.,1.)

def DataHists(df):
    df_ = DefineSignalAndSideband(df, True)
    dfSR = df_.Filter('phoSignalRegion==1')
    dfSB = df_.Filter('phoDataSideband==1')

    hists = []
    hists.append( dfSR.Histo1D(h_BDT('BDT_data_signalRegion', 'bdt_score'), 'bdt_score') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag0_data_signalRegion', 'bScore'), 'DeepFlavour.bScore') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag1_data_signalRegion', 'CvsL'  ), 'DeepFlavour.CvsL'  ) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag2_data_signalRegion', 'CvsB'  ), 'DeepFlavour.CvsB'  ) )

    hists.append( dfSB.Histo1D(h_BDT('BDT_data_dataSideband', 'bdt_score'), 'bdt_score') )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag0_data_dataSideband', 'bScore'), 'DeepFlavour.bScore') )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag1_data_dataSideband', 'CvsL'  ), 'DeepFlavour.CvsL'  ) )
    hists.append( dfSB.Histo1D(h_CTagVar('jettag2_data_dataSideband', 'CvsB'  ), 'DeepFlavour.CvsB'  ) )

    return hists
def GJetHists(df):
    def GetShapeDown(newNAME, hNOMINAL, hUNCup):
        newHist = hNOMINAL.Clone()
        newHist.SetName(newNAME)
        for ibin in range(hNOMINAL.GetNbinsX()+2):
            nom = hNOMINAL.GetBinContent(ibin)
            unc = hUNCup.GetBinContent(ibin)
            uncLow = nom - (unc-nom)
            if uncLow < 0: uncLow = 1e-10
            newHist.SetBinContent(ibin, uncLow)
        return newHist


    df_ = DefineSignalAndSideband(df, False)
    df__ = DefineJetTruth(df_)
    dfSR = df__.Filter('phoSignalRegion==1')
    dfSB = df__.Filter('phoDataSideband==1')

    hists = []
    hists.append( dfSR.Histo1D(h_BDT('BDT_gjet_signalRegion', 'bdt_score'), 'bdt_score') )
    hists.append( dfSR.Histo1D(h_BDT('BDT_gjet_signalRegion_shapeUncUp', 'bdt_score ShapeUp'), 'mva') )
    hists.append( GetShapeDown('BDT_gjet_signalRegion_shapeUncDown', hists[-2], hists[-1]) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag0_gjet_signalRegion', 'bScore'), 'DeepFlavour.bScore') )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag1_gjet_signalRegion', 'CvsL'  ), 'DeepFlavour.CvsL'  ) )
    hists.append( dfSR.Histo1D(h_CTagVar('jettag2_gjet_signalRegion', 'CvsB'  ), 'DeepFlavour.CvsB'  ) )


    return hists


if __name__ == "__main__":
    dataERA = "UL2016PostVFP"
    pETAbin = 0
    jETAbin = 0
    pPTlow = 200
    pPThigh = 220
    # { return std::vector<float>({190,200,220,250,300,        600,    1000, 9999}); }

    inFILEs = ExternalFileMgr.GetXPhotonFile(dataERA)
    dataFILE = inFILEs['data']
    signFILE = inFILEs['sign']
    fakeFILE = inFILEs['fake']

    rdf_data = ROOT.RDataFrame('t', dataFILE)
    rdf_sign = ROOT.RDataFrame('t', signFILE)
    rdf_fake = ROOT.RDataFrame('t', fakeFILE)

    rdf_data_ = rdf_data.Define('charge_isolation', 'calib_chIso').Define('photon_pt', 'recoPtCalib').Define('bdt_score', 'mva')
    rdf_sign_ = rdf_sign.Define('charge_isolation', 'chIsoRaw').Define('photon_pt', 'recoPt').Define('bdt_score', 'calib_mva')
    rdf_fake_ = rdf_fake.Define('charge_isolation', 'chIsoRaw').Define('photon_pt', 'recoPt').Define('bdt_score', 'mva')

    sel_data = DataSelection(rdf_data_)
    sel_sign = SignSelection(rdf_sign_)
    sel_fake = FakeSelection(rdf_fake_)

    binned_data = Binning(sel_data,  pETAbin,jETAbin,pPTlow,pPThigh)
    binned_sign = Binning(sel_sign,  pETAbin,jETAbin,pPTlow,pPThigh)
    binned_fake = Binning(sel_fake,  pETAbin,jETAbin,pPTlow,pPThigh)

    data_hists = DataHists(binned_data)
    sign_hists = GJetHists(binned_sign)
    #df_data = DefineSignalAndSideband(binned_data, True)
    #df_sign = DefineSignalAndSideband(binned_sign, False)
    #df_fake = DefineSignalAndSideband(binned_fake, False)

    #h = binned_data.Histo1D("recoPt")

    newfile = ROOT.TFile('outfile.root', 'recreate')
    for h in data_hists: h.Write()
    for h in sign_hists: h.Write()
    newfile.Close()
