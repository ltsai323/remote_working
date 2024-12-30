#include <cstdio>
#include <iostream>
#include "/cvmfs/cms.cern.ch/slc7_amd64_gcc11/external/py3-correctionlib/2.1.0-d2a3f7d7a03ec004ef7327ef5e29e333/lib/python3.9/site-packages/correctionlib/include/correction.h"

using namespace correction;

int main(int argc, char** argv) {
  if ( argc == 1 ) {
    printf("sizeof(Binning): %lu\n", sizeof(Binning));
    printf("sizeof(MultiBinning): %lu\n", sizeof(MultiBinning));
    printf("sizeof(Category): %lu\n", sizeof(Category));
    printf("sizeof(Formula): %lu\n", sizeof(Formula));
    printf("sizeof(Content): %lu\n", sizeof(Content));
  }
  else if ( argc == 2 ) {
    auto cset = CorrectionSet::from_file(std::string(argv[1]));
    for (auto& corr : *cset) {
      printf("Correction: %s\n", corr.first.c_str());
    }
    double out = cset->at("scalefactors_Tight_Electron")->evaluate({1.3, 25.});
    printf("scalefactors_Tight_Electron(1.3, 25) = %f\n", out);
    auto deepcsv = cset->at("DeepCSV_2016LegacySF");
    printf("deepcsv correction use count: %lu\n", deepcsv.use_count());
    cset.reset(nullptr);
    printf("deepcsv correction use count: %lu\n", deepcsv.use_count());
    out = deepcsv->evaluate({"central", 0, 1.2, 35., 0.01});
    printf("DeepCSV_2016LegacySF('central', 0, 1.2, 35., 0.5) = %f\n", out);
    double stuff {0.};
    size_t n { 1000000 };
    for(size_t i=0; i<n; ++i) {
      stuff += deepcsv->evaluate({"central", 0, 1.2, 35., i / (double) n});
    }
  }
  else {
    printf("Usage:%s filename.json\n", argv[0]);
  }
}
