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

using namespace ROOT;
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
const auto z_mass = 91.2;

TFile* fIN = TFile::Open("sfhist_jetpt.root");
auto sfhist_ptGJetandQCD = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJetandQCD");
auto sfhist_ptGJet       = (TGraphAsymmErrors*) fIN->Get("sfjet_dataOVERGJet");


Double_t pt_sfGJetandQCD(Double_t pt) { return sfhist_ptGJetandQCD->Eval(pt); }
Double_t pt_sfGJet      (Double_t pt) { return sfhist_ptGJet      ->Eval(pt); }

#include "extlib/correction.h"

auto btvjson = CorrectionSet::from_file("/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/BTV/2022_Summer22EE/btagging.json.gz");
Double_t sf_WPbL_central(Double_t jetPT, Double_t jetETA) { return btvjson->at("



#endif
