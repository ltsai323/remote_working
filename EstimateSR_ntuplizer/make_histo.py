import ROOT

BDTHistSetup = lambda name: (name, "BDT Score", 10, -1.,1.)
CTagScoreHistSetup = lambda name, varname: (name, varname, 10, 0., 1.)

def Drawing_histogram_data(binnedDATAframe, oFILE):
    out = []

    d_SR = binnedDATAframe
    out.append( d_SR.Histo1D(BDTHistSetup('BDT_data_signalRegion'), 'photon_mva') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag0_data_signalRegion','bScore'), 'bScore') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag1_data_signalRegion','CvsL'  ), 'CvsL'  ) )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag2_data_signalRegion','CvsB'  ), 'CvsB'  ) )

    oFILE.cd()
    for hist in out:
        hist.Write()
def Drawing_histogram_data_sideband(binnedDATAframe, oFILE):
    out = []

    d_SB = binnedDATAframe
    out.append( d_SB.Histo1D(BDTHistSetup('BDT_data_dataSideband'), 'photon_mva') )
    out.append( d_SB.Histo1D(CTagScoreHistSetup('jettag0_data_dataSideband','bScore'), 'bScore') )
    out.append( d_SB.Histo1D(CTagScoreHistSetup('jettag1_data_dataSideband','CvsL'  ), 'CvsL'  ) )
    out.append( d_SB.Histo1D(CTagScoreHistSetup('jettag2_data_dataSideband','CvsB'  ), 'CvsB'  ) )

    oFILE.cd()
    for hist in out:
        hist.Write()
def Drawing_histogram_gjet(binnedDATAframe, oFILE):
    def BDT_shapeUncDown(hNominal, hUncUp):
        hUncDown = hNominal.Clone( f'{hNominal.GetName()}_shapeUncDown' )
        for binIdx in range(hNominal.GetNbinsX()+2): # including underflow and overflow bins
            contentUp = hUncUp.GetBinContent(binIdx)
            contentNum= hNominal.GetBinContent(binIdx)
            contentDown = contentNum - (contentUp-contentNum) # mean - diff
            if contentDown < 0 : contentDown = 0
            hUncDown.SetBinContent(binIdx, contentDown)
        return hUncDown

    out = []

    d_SR = binnedDATAframe.Filter('GenPhoton_pt>0')
    d_SR_L = d_SR.Filter('isHadFlvr_L')
    d_SR_C = d_SR.Filter('isHadFlvr_C')
    d_SR_B = d_SR.Filter('isHadFlvr_B')


    out.append( d_SR.Histo1D(BDTHistSetup('BDT_gjet_signalRegion'), 'photon_mva', 'wgt') )
    out.append( d_SR.Histo1D(BDTHistSetup('BDT_gjet_signalRegion_shapeUncUp'), 'photon_mva_orig', 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag0_gjet_allJets_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag1_gjet_allJets_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag2_gjet_allJets_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )
    out.append( BDT_shapeUncDown(out[-2],out[-1]) )

    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag0_gjet_GJetsL_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag1_gjet_GJetsL_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag2_gjet_GJetsL_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )

    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag0_gjet_GJetsC_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag1_gjet_GJetsC_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag2_gjet_GJetsC_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )

    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag0_gjet_GJetsB_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag1_gjet_GJetsB_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag2_gjet_GJetsB_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )


    oFILE.cd()
    for hist in out:
        hist.Write()
def Drawing_histogram_qcd(binnedDATAframe, oFILE):
    out = []

    d_SR = binnedDATAframe.Filter('GenPhoton_pt<0')
    d_SR_L = d_SR.Filter('isHadFlvr_L')
    d_SR_C = d_SR.Filter('isHadFlvr_C')
    d_SR_B = d_SR.Filter('isHadFlvr_B')


    out.append( d_SR.Histo1D(BDTHistSetup('BDT_QCD_signalRegion'), 'photon_mva', 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag0_QCD_allJets_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag1_QCD_allJets_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR.Histo1D(CTagScoreHistSetup('jettag2_QCD_allJets_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )


    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag0_QCD_DiJetL_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag1_QCD_DiJetL_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_L.Histo1D(CTagScoreHistSetup('jettag2_QCD_DiJetL_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )

    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag0_QCD_DiJetC_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag1_QCD_DiJetC_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_C.Histo1D(CTagScoreHistSetup('jettag2_QCD_DiJetC_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )

    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag0_QCD_DiJetB_signalRegion','bScore'), 'bScore', 'wgt') )
    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag1_QCD_DiJetB_signalRegion','CvsL'  ), 'CvsL'  , 'wgt') )
    out.append( d_SR_B.Histo1D(CTagScoreHistSetup('jettag2_QCD_DiJetB_signalRegion','CvsB'  ), 'CvsB'  , 'wgt') )


    oFILE.cd()
    for hist in out:
        hist.Write()

def ctagvar(algo, var):
    ### TBranch name
    ctag_pnet        = {'bScore':"PNetB"       , 'CvsB':"PNetCvsB"       , 'CvsL':"PNetCvsL"       , 'QvsG':"PNetQvsG"       }
    ctag_ptransform  = {'bScore':"ParTB"       , 'CvsB':"ParTCvsB"       , 'CvsL':"ParTCvsL"       , 'QvsG':"ParTQvsG"       }
    ctag_deepflavour = {'bScore':"DeepFlavourB", 'CvsB':"DeepFlavourCvsB", 'CvsL':"DeepFlavourCvsL", 'QvsG':"DeepFlavourQvsG"}

    if algo == 'DeepFlavour':
        return ctag_deepflavour[var]
    if algo == 'ParT':
        return ctag_ptransform[var]
    if algo == 'PNet':
        return ctag_pnet[var]
    raise KeyError(f'\n\n[Invalid Algorithm] ctagvar() got algorithm "{algo}" matched nothing. Please check')


def create_binned_histograms(phoETAbin:int,jetETAbin:int,phoPTlow:float,phoPThigh:float,
        inFILE:tuple, oDIR:ROOT.TDirectoryFile):
    input_file = inFILE[1]
    run_type = inFILE[0]
    df = ROOT.RDataFrame("tree", input_file)  # Replace 'tree_name' with the name of the tree in your ROOT file

    phoEtaBin = phoETAbin
    jetEtaBin = jetETAbin

    df_binning = df \
        .Define('bScore' , ctagvar('DeepFlavour', 'bScore') ) \
        .Define('CvsL'   , ctagvar('DeepFlavour', 'CvsL'  ) ) \
        .Define('CvsB'   , ctagvar('DeepFlavour', 'CvsB'  ) ) \
        .Filter( "&&".join([
                    f'photon_pt > {phoPTlow} && photon_pt<{phoPThigh}',
                     'abs(photon_eta)<1.4442' if phoEtaBin == 0 else 'abs(photon_eta)>1.566&&abs(photon_eta)<2.5',
                     'abs(jet_eta)<1.4442'    if jetEtaBin == 0 else 'abs(jet_eta)>1.566&&abs(jet_eta)<2.5',
                     'jet_nSV>0',
                 ]) )


    if run_type == 'data': Drawing_histogram_data(df_binning, oDIR)
    if run_type == 'sidB': Drawing_histogram_data_sideband(df_binning, oDIR)
    if run_type == 'gjet': Drawing_histogram_gjet(df_binning, oDIR)
    if run_type == 'qcd' : Drawing_histogram_qcd (df_binning, oDIR)

if __name__ == "__main__":
    pETAbin, jETAbin, pPTbin = (0,0,4)
    pt_binnings = [ 210,230,250,300,400,500,600,800,1000,1500 ]
    if pPTbin+1 >= len(pt_binnings):
        info(f'[OutOfRange] input pt bin "{ pPTbin }" is out of range. Ignore the command')
        exit(0)

    in_file_data = ('data', 'data_signalregion.root')
    in_file_sidB = ('sidB', 'data_sideband.root')
    in_file_gjet = ('gjet', 'gjetMadgraph.root')
    in_file_qcd  = ('qcd' , 'QCDMadgraph.root')
    oFile = ROOT.TFile(f'mkhist_{pETAbin}_{jETAbin}_{pPTbin}.root', 'recreate')
    oDir = oFile.mkdir(f'bin_{pETAbin}_{jETAbin}_{pPTbin}')
    create_binned_histograms(pETAbin,jETAbin, pt_binnings[pPTbin],pt_binnings[pPTbin+1], in_file_data, oDir)
    create_binned_histograms(pETAbin,jETAbin, pt_binnings[pPTbin],pt_binnings[pPTbin+1], in_file_sidB, oDir)
    create_binned_histograms(pETAbin,jETAbin, pt_binnings[pPTbin],pt_binnings[pPTbin+1], in_file_gjet, oDir)
    create_binned_histograms(pETAbin,jETAbin, pt_binnings[pPTbin],pt_binnings[pPTbin+1], in_file_qcd , oDir)
    oFile.Close()
    print(f'i@ [OutputRootFile] {oFile.GetName()}')
