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
    intfile->Close();

    // Create RDataFrame for the "Events" tree
    ROOT::RDataFrame df("Events", inFILE);


    // Define the new column "jetP4" based on input jet variables
    auto df_mu = df
      .Define("muon_mom_genidx", MuonMother_GenIdx, { "Muon_genPartIdx", "GenPart_pdgId", "GenPart_genPartIdxMother" })
      .Define("muon_mom_pid", [](const RVec<Int_t>& valARR, const RVec<Short_t>& idxARR) { return GeneralFuncs::access_array_by_idxarray(valARR,idxARR); }, {"GenPart_pdgId", "muon_mom_genidx"})
      .Define("muon_mom_is_z", "muon_mom_pid==23");
    //const double entries_muonsel = df_mu_sel.Count().GetValue();



    auto df_out = df_mu;
    df_out.Snapshot("Events", outFILE, {
        "muon_mom_genidx",
        "muon_mom_pid",
        "muon_mom_is_z", 
        "Muon_pt", 
        "Muon_mediumPromptId",
        "Muon_tightId",
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
