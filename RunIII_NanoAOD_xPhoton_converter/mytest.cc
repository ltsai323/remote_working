#include <ROOT/RDataFrame.hxx>
#include <TLorentzVector.h>
#include <ROOT/RVec.hxx>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <iostream>
#include "MyDYjet_ZmmSelections.h"
#include "MyJetSelections.h"
#include "MyGeneralFuncs.h"
#include "MyImportedFileMgr.h"


using namespace ROOT;
using namespace ROOT::VecOps;

//// Function to construct jetP4 vector
//RVec<TLorentzVector> ConstructJetP4(const RVec<float> &Jet_pt, 
//                                    const RVec<float> &Jet_eta, 
//                                    const RVec<float> &Jet_phi, 
//                                    const RVec<float> &Jet_mass,
//                                    const Int_t nJet) {
//    RVec<TLorentzVector> jetP4;
//    for (size_t i = 0; i < nJet; ++i) {
//        TLorentzVector jet;
//        jet.SetPtEtaPhiM(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
//        jetP4.push_back(jet);
//    }
//    return jetP4;
//}

template <typename T>
T access_array_by_idx(const RVec<T>& theARRAY, Short_t idx)
{
  try {
    // not to raise error if -1 put. (means nothing)
    if ( idx<0 ) return -1;
    if (idx >= theARRAY.size()) {
    //if (idx < 0 || idx >= theARRAY.size()) {
      throw std::out_of_range(
          Form("[OutOfRange] Accessing array(size %zu) with index(%d) is out of bounds!", theARRAY.size(), idx)
          );
    }
    return theARRAY[idx];  // Safe access
  } 
  catch (const std::out_of_range &e) {
    std::cerr << "Error: " << e.what() << std::endl;
    exit(EXIT_FAILURE);
  }
}
Short_t MuonMother_iterative_search_mother_genpartidx(Short_t genIDX, const RVec<int>& genPARTpid, const RVec<Short_t>& genMOMidx)
{
  Short_t currentPID = access_array_by_idx(genPARTpid, genIDX);  // Safe access
  if ( abs(currentPID) != 13 ) return genIDX;
  Short_t motherIDX = access_array_by_idx(genMOMidx, genIDX);
  return MuonMother_iterative_search_mother_genpartidx( motherIDX, genPARTpid, genMOMidx );
}
RVec<Short_t> MuonMother_GenIdx(
  const RVec<Short_t>& muonGENidx,
  const RVec<Int_t>  & genPARTpid,
  const RVec<Short_t>& genMOMidx)
{
  if ( muonGENidx.size() == 0 ) return RVec<Short_t>();
  RVec<Short_t> muon_mother_idx;
  for ( auto muon_gen_idx : muonGENidx )
    if (muon_gen_idx>0)
      muon_mother_idx.push_back( MuonMother_iterative_search_mother_genpartidx(muon_gen_idx,genPARTpid,genMOMidx) );
    else
      muon_mother_idx.push_back( -1 );
  return muon_mother_idx;
}


  

int mainfunc_MC(const char* inFILE, const char* outFILE, const double integratedLUMINOSITY, const double processCROSSSECTION) {
    auto intfile = TFile::Open(inFILE);
    auto h_load = (TH1*) intfile->Get("totWgt");
    const double integrated_gen_weight = h_load->GetBinContent(1);
    const double total_gen_entries = h_load->GetBinContent(2);
    intfile->Close();

    // Create RDataFrame for the "Events" tree
    ROOT::RDataFrame df("Events", inFILE);


    // Define the new column "jetP4" based on input jet variables
    auto df_mu = df
      .Define("muoncomb_2indices", "Combinations(Muon_pt,2)")
      .Define("mupair_mu0idxs", "muoncomb_2indices[0]")
      .Define("mupair_mu1idxs", "muoncomb_2indices[1]")

      .Define("mupair_mu0eta","Take(Muon_eta,mupair_mu0idxs)")
      .Define("mupair_mu1eta","Take(Muon_eta,mupair_mu1idxs)")
      .Define("mupair_abs_eta", "abs(mupair_mu0eta-mupair_mu1eta)")
      .Define("mupair_cut_abs_eta", "mupair_abs_eta < 2.4") // cut

      .Define("mupair_mu0charge", "Take(Muon_charge,mupair_mu0idxs)")
      .Define("mupair_mu1charge", "Take(Muon_charge,mupair_mu1idxs)")
      .Define("mupair_charge_product", "mupair_mu0charge*mupair_mu1charge")
      .Define("mupair_cut_charge_product", "mupair_charge_product == -1") // cut

      .Define("mupair_mu0pt", "Take(Muon_pt,mupair_mu0idxs)")
      .Define("mupair_mu1pt", "Take(Muon_pt,mupair_mu1idxs)")
      .Define("mupair_cut_pt", "mupair_mu0pt>25 && mupair_mu1pt>20") // cut
      
      .Define("mupair_mu0tightID", "Take(Muon_tightId,mupair_mu0idxs)")
      .Define("mupair_mu1tightID", "Take(Muon_tightId,mupair_mu1idxs)")
      .Define("mupair_cut_tightID", "mupair_mu0tightID==1&&mupair_mu1tightID==1") // cut


      .Define("mupair_mu0pfIsoID", "Take(Muon_pfIsoId,mupair_mu0idxs)")
      .Define("mupair_mu1pfIsoID", "Take(Muon_pfIsoId,mupair_mu1idxs)")
      .Define("mupair_cut_pfIsoID", "mupair_mu0pfIsoID>=4 && mupair_mu1pfIsoID>=4") // 4 tight, 5 very tight, 6 very very tight
      .Define("mupair_overallcut", "mupair_cut_abs_eta*mupair_cut_charge_product*mupair_cut_pt*mupair_cut_tightID*mupair_cut_pfIsoID")
      .Define("mupair_selected_idx",
          [](const RVec<Int_t>& cuts) {
            auto indices_from_descent_sorted_array = StableArgsort(cuts, [](Int_t a,Int_t b){return a>b;});
            Short_t found_idx = indices_from_descent_sorted_array[0];
            Int_t cut = cuts[found_idx];
            if ( cut == 0 ) found_idx = -1; // set it to none
            return found_idx;
            }, {"mupair_overallcut"})
      .Filter("mupair_selected_idx>=0") // cut entry found no muon pair
      .Define("muon_cand0idx", "mupair_mu0idxs[mupair_selected_idx]")
      .Define("muon_cand1idx", "mupair_mu1idxs[mupair_selected_idx]")



      .Define("muon_mom_genidx", MuonMother_GenIdx, { "Muon_genPartIdx", "GenPart_pdgId", "GenPart_genPartIdxMother" })
      .Define("muon_mom_pid", "Take(GenPart_pdgId,muon_mom_genidx, -1)")
      .Define("mucand0mompid", "muon_mom_pid[muon_cand0idx]")
      .Define("mucand1mompid", "muon_mom_pid[muon_cand1idx]")
      .Define("isMatchedZ", "mucand0mompid==23 && mucand1mompid==23")

      .Define("mucand0P4", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muon_cand0idx],Muon_eta[muon_cand0idx],Muon_phi[muon_cand0idx],Muon_mass[muon_cand0idx])")
      .Define("mucand1P4", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muon_cand1idx],Muon_eta[muon_cand1idx],Muon_phi[muon_cand1idx],Muon_mass[muon_cand1idx])")
      .Define("recZP4", "mucand0P4+mucand1P4")
      .Define("recZmass", "recZP4.M()")
      .Define("recZpt"  , "recZP4.Pt()")
      .Define("recZeta" , "recZP4.Eta()")
      .Define("recZphi" , "recZP4.Phi()")
      .Filter("recZmass>(90-30) && recZmass<(90+30)") // cut Z mass window
      ;
    //const double entries_muonsel = df_mu_sel.Count().GetValue();



    auto df_out = df_mu;
    df_out.Snapshot("Events", outFILE, {
        "mupair_mu0eta", "mupair_mu1eta",
        "mupair_abs_eta",
        "mupair_charge_product",
        "muon_mom_genidx",
        "muon_mom_pid",
        "isMatchedZ", 
        "Muon_pt", 
        "Muon_mediumPromptId",
        "Muon_tightId",
      "mupair_overallcut",
      "mupair_selected_idx",
        "nMuon",
      "recZmass",
      "recZpt"  ,
      "recZeta" ,
      "recZphi" ,
        });

    return 0;




    /*
    auto out_file = new TFile(outFILE, "UPDATE");
    out_file->cd();

    auto hEFF_muonSel = new TH1F("effMuonSel", "MuonSelectionEfficiency bin1:total bin2:pass filter", 2, 0., 2.);
    hEFF_muonSel->SetBinContent(1, entries_tot);
    hEFF_muonSel->SetBinContent(2, entries_muonsel);
    hEFF_muonSel->Write();

    out_file->Close();

    delete jecjer_corr, pileup_mgr;
    */
    
    return 0;
}
int main(int argc, char** argv) {
    if (argc < 1+1) {
        std::cerr << "Usage: " << argv[0] << " <input_root_file>" << std::endl;
        return 1;
    }
    // available data_era: "2022EERunE", "2022EERunF", "2022EERunG", "2022EE_MC"
    std::string dataERA = "2022EE_MC";
    double lumi = 22.26; // fb-1
    double xs = 1.0; // fb
    if ( dataERA == "2022EE_MC" )
      return mainfunc_MC(argv[1], "testoutput.root", lumi, xs);

    throw std::invalid_argument(
        Form("[InvalidDataEra] data era(%s) is rejected. The available options are '2022EERunE', '2022EERunF', '2022EERunG', '2022EE_MC'", dataERA.c_str())
          );
}
