/// \file
/// \ingroup tutorial_dataframe
/// Header file with functions needed to execute the Python version
/// of the NanoAOD Higgs tutorial. The header is declared to the
/// ROOT C++ interpreter prior to the start of the analysis via the
/// `ROOT.gInterpreter.Declare()` function.
///
/// \date July 2019
/// \authors Stefan Wunsch (KIT, CERN), Vincenzo Eduardo Padulano (UniMiB, CERN)


#ifndef __makehisto_additional_functions_h__
#define __makehisto_additional_functions_h__
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include <map>

using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
//const auto z_mass = 91.2;

bool bugmode = true;
void BUG(const char* mesg) { if ( bugmode ) printf( "%s\n", mesg); }
// get 1108001000 for pEta 0 jEta 0 pPT 800~1000
int BinningIdx(int pETAbin, int jETAbin, int pPTlow, int pPThigh) { return 1e9*pETAbin + 1e8*jETAbin + 1e4*pPTlow + pPThigh; }
std::vector<TFile*> opened_files;
std::map<int,TGraphAsymmErrors*> sf_ptGJets;
std::map<int,TGraphAsymmErrors*> sf_ptGJetandQCDs;
std::map<int,TH2F             *> sf_ptANDnjetGJets;
std::map<int,TH3F             *> sf_phoptjetptANDnjetGJets;

//TFile* fIN = TFile::Open("sfhist_jetpt.root");
//auto sfhist_ptGJetandQCD = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJetandQCD");
//auto sfhist_ptGJet       = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJet");


//Double_t pt_sfGJetandQCD(Double_t pt) { return sfhist_ptGJetandQCD->Eval(pt); }
//Double_t pt_sfGJet      (Double_t pt) { return sfhist_ptGJet      ->Eval(pt); }


TH2F* GetSFTH2FGJet( int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{
    int key = BinningIdx(pETAbin,jETAbin,pPTlow,pPThigh);
    auto it = sf_ptANDnjetGJets.find(key);
    if (it != sf_ptANDnjetGJets.end()) {
        return it->second; // Return the value associated with the key
    }

    auto fIN = TFile::Open( Form("sfhist_jetpt__%d_%d_%d_%d.root",pETAbin,jETAbin,pPTlow,pPThigh) );
    BUG( Form("[LoadFile] GetSFHistGJet() loads file %s", fIN->GetName()) );
    sf_ptANDnjetGJets[key] = (TH2F*) fIN->Get("sfjetANDnjet_dataOVERGJet");
    opened_files.push_back(fIN);
    return sf_ptANDnjetGJets[key];
}
TH3F* GetSFTH3FGJet( int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{
    int key = BinningIdx(pETAbin,jETAbin,pPTlow,pPThigh);
    auto it = sf_phoptjetptANDnjetGJets.find(key);
    if (it != sf_phoptjetptANDnjetGJets.end()) {
        return it->second; // Return the value associated with the key
    }

    auto fIN = TFile::Open( Form("sfhist_jetpt__%d_%d_%d_%d.root",pETAbin,jETAbin,pPTlow,pPThigh) );
    BUG( Form("[LoadFile] GetSFHistGJet() loads file %s", fIN->GetName()) );
    sf_phoptjetptANDnjetGJets[key] = (TH3F*) fIN->Get("sfphoptjetptANDnjet_dataOVERGJet");
    opened_files.push_back(fIN);
    return sf_phoptjetptANDnjetGJets[key];
}
TGraphAsymmErrors* GetSFHistGJet( int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{
    int key = BinningIdx(pETAbin,jETAbin,pPTlow,pPThigh);
    auto it = sf_ptGJets.find(key);
    if (it != sf_ptGJets.end()) {
        return it->second; // Return the value associated with the key
    }

    auto fIN = TFile::Open( Form("sfhist_jetpt__%d_%d_%d_%d.root",pETAbin,jETAbin,pPTlow,pPThigh) );
    BUG( Form("[LoadFile] GetSFHistGJet() loads file %s", fIN->GetName()) );
    sf_ptGJets[key] = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJet");
    opened_files.push_back(fIN);
    return sf_ptGJets[key];
}
TGraphAsymmErrors* GetSFHistGJetQCD( int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{
    int key = BinningIdx(pETAbin,jETAbin,pPTlow,pPThigh);
    auto it = sf_ptGJetandQCDs.find(key);
    if (it != sf_ptGJetandQCDs.end()) {
        return it->second; // Return the value associated with the key
    }

    auto fIN = TFile::Open( Form("sfhist_jetpt__%d_%d_%d_%d.root",pETAbin,jETAbin,pPTlow,pPThigh) );

    BUG( Form("[LoadFile] GetSFHistGJetQCD() loads file %s", fIN->GetName()) );
    sf_ptGJetandQCDs[key] = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJetandQCD");
    opened_files.push_back(fIN);
    return sf_ptGJetandQCDs[key];
}
Double_t pt_sfGJetandQCD(Double_t pt, int pETAbin, int jETAbin, int pPTlow, int pPThigh ) { return GetSFHistGJetQCD(pETAbin,jETAbin,pPTlow,pPThigh)->Eval(pt); }
Double_t pt_sfGJet      (Double_t pt, int pETAbin, int jETAbin, int pPTlow, int pPThigh ) { return GetSFHistGJet   (pETAbin,jETAbin,pPTlow,pPThigh)->Eval(pt); }

Double_t ptANDnjet_sfGJet(Double_t pt, Int_t nJET, int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{ auto h2D = (TH2F*) GetSFTH2FGJet(pETAbin,jETAbin,pPTlow,pPThigh); Int_t ibin = h2D->FindBin(pt,nJET); return h2D->GetBinContent(ibin); }
Double_t phoptjetptANDnjet_sfGJet(Double_t phoPT, Double_t jetPT, Int_t nJET, int pETAbin, int jETAbin, int pPTlow, int pPThigh )
{ auto h3D = (TH3F*) GetSFTH3FGJet(pETAbin,jETAbin,pPTlow,pPThigh); Int_t ibin = h3D->FindBin(phoPT,jetPT,nJET); return h3D->GetBinContent(ibin); }


#endif
