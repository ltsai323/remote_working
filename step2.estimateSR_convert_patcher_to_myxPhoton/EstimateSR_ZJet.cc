#include <ROOT/RDataFrame.hxx>
#include <TLorentzVector.h>
#include <ROOT/RVec.hxx>
#include <TFile.h>
#include <TTree.h>
#include <iostream>

using namespace ROOT;
using namespace ROOT::VecOps;

// Function to construct jetP4 vector
RVec<TLorentzVector> ConstructJetP4(const RVec<float> &Jet_pt, 
                                    const RVec<float> &Jet_eta, 
                                    const RVec<float> &Jet_phi, 
                                    const RVec<float> &Jet_mass,
                                    const Int_t nJet) {
    RVec<TLorentzVector> jetP4;
    for (size_t i = 0; i < nJet; ++i) {
        TLorentzVector jet;
        jet.SetPtEtaPhiM(Jet_pt[i], Jet_eta[i], Jet_phi[i], Jet_mass[i]);
        jetP4.push_back(jet);
    }
    return jetP4;
}

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


  

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_root_file>" << std::endl;
        return 1;
    }

    std::string filename = argv[1];

    // Create RDataFrame for the "Events" tree
    ROOT::RDataFrame df("Events", filename);

    // Define the new column "jetP4" based on input jet variables
    auto df2 = df
      .Define("jet_p4", ConstructJetP4, {"Jet_pt", "Jet_eta", "Jet_phi", "Jet_mass", "nJet"})
      .Define("muon_mom_genidx", MuonMother_GenIdx, { "Muon_genPartIdx", "GenPart_pdgId", "GenPart_genPartIdxMother" });

    df2.Display({"muon_mom_genidx"})->Print();
    return 0;
    // Print the first few entries for verification
    df2.Display({"jetP4"})->Print();

    // Save the modified DataFrame with the new column into a new ROOT file
    df2.Snapshot("Events", "output.root", {"myJetMass"});

    std::cout << "Processed ROOT file saved as output.root" << std::endl;

    return 0;
}
