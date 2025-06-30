#!/usr/bin/env python3

import ROOT

inFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/GJetPythiaFlat.root'
inFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/QCD4JetsMadgraph_100to200.root'
#inFILE = '/afs/cern.ch/user/l/ltsai/eos_storage/condor_summary/2022EE_GJet/G4JetsMadgraph_40to70.root'

if __name__ == "__main__":
    df = ROOT.RDataFrame('Events', inFILE) \
            .Define('ispartonB', 'abs(Jet_partonFlavour) == 5') \
            .Define('ispartonC', 'abs(Jet_partonFlavour) == 4') \
            .Define('ishadronB', 'ROOT::VecOps::RVec<bool> o; for (auto&& hadF : Jet_hadronFlavour) o.push_back( int(hadF)==5 ? true : false ); return o;' ) \
            .Define('ishadronC', 'ROOT::VecOps::RVec<bool> o; for (auto&& hadF : Jet_hadronFlavour) o.push_back( int(hadF)==4 ? true : false ); return o;' ) \
            .Define('ishadronL', 'ROOT::VecOps::RVec<bool> o; for (auto&& hadF : Jet_hadronFlavour) o.push_back( int(hadF)==0 ? true : false ); return o;' )

    df_partonB = df \
            .Filter('Sum(ispartonB)>0') \
            .Define('jetpt_partonB', 'ispartonB * Jet_pt') \
            .Define('partonB_idx', 'ArgMax(jetpt_partonB)') \
            .Define('hardonF', 'int(Jet_hadronFlavour[partonB_idx])')
    df_partonC = df \
            .Filter('Sum(ispartonC)>0') \
            .Define('jetpt_partonC', 'ispartonC * Jet_pt') \
            .Define('partonC_idx', 'ArgMax(jetpt_partonC)') \
            .Define('hardonF', 'int(Jet_hadronFlavour[partonC_idx])')
    df_hadronB = df \
            .Filter('Sum(ishadronB)>0') \
            .Define('jetpt_hadronB', 'ishadronB * Jet_pt') \
            .Define('hadronB_idx', 'ArgMax(jetpt_hadronB)') \
            .Define('partonF', 'int(Jet_partonFlavour[hadronB_idx])')
    df_hadronC = df \
            .Filter('Sum(ishadronC)>0') \
            .Define('jetpt_hadronC', 'ishadronC * Jet_pt') \
            .Define('hadronC_idx', 'ArgMax(jetpt_hadronC)') \
            .Define('partonF', 'int(Jet_partonFlavour[hadronC_idx])')

    df_hadronL = df \
            .Filter('Sum(ishadronL)>0') \
            .Define('jetpt_hadronL', 'ishadronL * Jet_pt') \
            .Define('hadronL_idx', 'ArgMax(jetpt_hadronL)') \
            .Define('partonF', 'int(Jet_partonFlavour[hadronL_idx])') \
            .Filter('abs(partonF) == 4 || abs(partonF) == 5')

    print('\n\n[Check hadraonFlavour in partonB')
    df_partonB.Display('hardonF').Print()

    print('\n\n[Check hadraonFlavour in partonC')
    df_partonC.Display('hardonF').Print()

    print('\n\n[Check partonFlavour in hadronB')
    df_hadronB.Display('partonF').Print()

    print('\n\n[Check partonFlavour in hadronC')
    df_hadronC.Display('partonF').Print()

    print('\n\n[Check partonFlavour in hadronL but parton is C or B')
    df_hadronL.Display('partonF').Print()

    exit()
    df = ROOT.RDataFrame('Events', inFILE) \
            .Define('ispartonB', 'abs(Jet_partonFlavour) == 5') \
            .Filter('Sum(ispartonB)>0') \
            .Define('jetpt_partonB', 'ispartonB * Jet_pt') \
            .Define('partonB_idx', 'ArgMax(jetpt_partonB)') \
            .Define('hardonF_partonB', 'Jet_hardonFlavour[partonB_idx]')
           #.Define('ispartonC', 'Jet_hadronFlavour == 4') \
           #.Define('jetpt_partonC', 'ispartonC * Jet_pt') \
           #.Define('partonC_idx', 'ArgMax(jetpt_partonC)')
    canv = ROOT.TCanvas("c1",'', 800,800)
    h = df.Histo1D('hardonF_partonB')
    h.Draw()
    canv.SaveAs("hi.png")



