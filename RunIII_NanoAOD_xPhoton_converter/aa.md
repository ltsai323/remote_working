### input files
auto cset_photon_scale_smearing_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/SS.json");
auto cset_jet_jerc_file = CorrectionSet::from_file("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/EGmSFs/jet_jerc.json");
   fpu = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/Pileup_files/PileupSF_DYJets_EraEFG.root");
   TFile *fss_barrel = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/TagAndProbe/output_ShowerShapeCorrection_barrel_1000Bins.root");
   TFile *fss_endcap = new TFile("/eos/user/s/sakarmak/SWAN_projects/GammaJets13p6TeV/TagAndProbe/output_ShowerShapeCorrection_endcap_1000Bins.root");
### Selections
      if(HLT_Photon200==0) continue;
      if(isSignal == true && nGenIsolatedPhoton < 1) continue;
      if(abs(Photon_eta[ij])>2.5 || Photon_pixelSeed[ij]==1)continue;
      if(abs(Photon_eta[ij])>1.44 && abs(Photon_eta[ij])<1.566) continue;
      if(abs(Photon_eta[ij])<1.44 && (Photon_pfChargedIsoPFPV[ij]>1.7 || Photon_sieie[ij]>0.015 || Photon_hoe[ij]>0.05 || Photon_pfChargedIsoWorstVtx[ij]>10)) continue;
      if(abs(Photon_eta[ij])>1.566 && (Photon_pfChargedIsoPFPV[ij]>1.5 || Photon_sieie[ij]>0.04 || Photon_hoe[ij]>0.05 || Photon_pfChargedIsoWorstVtx[ij]>10)) continue;
      if(Photon_pt[ij]>700 && Photon_pt[ij]<900 && Photon_seediEtaOriX[ij]+0==-21 && Photon_seediPhiOriY[ij]==260 && isEraG==true) continue; //Only for Era G

* Smeared (MC) or Scaled (data) Photon pt > 210. GeV (line749)
* For signal MC, the selected photon should matched to gen photon. ( use Photon_genPartIdx or match GenIsolatedPhoton? )
### New variables
* Photon Pt smearing on MC and Photon pt scale on Data. (line736)


### Stranges
* Lots of barrel photon SS does not load SScorr
  - photon_esEffSigmaRR = Photon_esEffSigmaRR[ij];
  - photon_energyRaw = Photon_energyRaw[ij];
  - photon_esEnergyOverRawE = Photon_esEnergyOverRawE[ij];
  - photon_etaWidth = Photon_etaWidth[ij];
  - photon_hoe = grDataInv_b[0]->Eval(grMC_b[0]->Eval(Photon_hoe[ij]));
  - photon_phiWidth = Photon_phiWidth[ij];
  - photon_r9 = Photon_r9[ij];
  - photon_s4 = Photon_s4[ij];
  - photon_sieie = grDataInv_b[1]->Eval(grMC_b[1]->Eval(Photon_sieie[ij]));
  - photon_sieip = Photon_sieip[ij];
  Only Signal Photon used SScorr. QCD uses original value

* Signal MC : Select photon passes selection, matching to gen isolated photon and choose leading one.
* QCD: not gen isolated photon, choose leading reco photon WITHOUT SScorr. If gen isolated photon listed in event, choose reco photon passes selection. Try to match gen isolated photon. 
  - But this algorithm losses the fake leading reco photon selected and this event generated some gen isolated photon.

* Calculate JEC and JER and jet selection
* Calculate PUweight
  

