#define HI_cxx
#include "HI.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <iostream>

void HI::Loop()
{
   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   Long64_t nbytes = 0, nb = 0;
   bool evt_shown = false;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      if ( nJet == 0 ) continue; evt_shown = true;
      for ( int ijet = 0; ijet < nJet; ++ijet )
      {
          int nsv = Jet_nSVs[ijet];
          std::cout << ijet << "th jet contains nSV = " << int(Jet_nSVs[ijet]) << " and convertion is " << nsv << std::endl;
      }

      if ( evt_shown ) break;
      // if (Cut(ientry) < 0) continue;
   }
}



int main()
{
    HI a;
    a.Loop();
    return 0;
}

