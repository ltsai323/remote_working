#!/usr/bin/env python3
import ROOT

class LoadedValue:
    def __init__(self, lVAL, cVAL, bVAL):
        self.lval = lVAL
        self.cval = cVAL
        self.bval = bVAL
        tot = lVAL + cVAL + bVAL
        self.lfrac = lVAL / tot
        self.cfrac = cVAL / tot
        self.bfrac = bVAL / tot


def load_truth(iFILEname, Ljet, Cjet, Bjet) -> LoadedValue:
    tfile = ROOT.TFile.Open(iFILEname)

    hL = tfile.Get(Ljet)
    hC = tfile.Get(Cjet)
    hB = tfile.Get(Bjet)

    return LoadedValue(
            hL.Integral(),
            hC.Integral(),
            hB.Integral() )

def load_fit_from_postfit(iFILEname):
    print(iFILEname)

    tfile = ROOT.TFile.Open(iFILEname)

    hL = tfile.Get('Ljet')
    hC = tfile.Get('Cjet')
    hB = tfile.Get('Bjet')

    return LoadedValue(
            hL.Integral(),
            hC.Integral(),
            hB.Integral() )


def show_value(info, tag):
    print(f'LoadValue({tag}, l({info.lval:10.2f}),  c({info.cval:10.2f}),  b({info.bval:10.2f}) )')
def show_frac(info, tag):
    print(f'LoadFrac ({tag}, l({info.lfrac:.4f}),  c({info.cfrac:.4f}),  b({info.bfrac:.4f}) )')

if __name__ == "__main__":
    import sys
    import yaml

    with open(sys.argv[1], 'r') as iFILE:
        config = yaml.safe_load(iFILE)

    truth_file = config['inputFILE']

    truth_value = load_truth(
            config['inputFILE'],
            **config['truth_info'])

    fit_value = load_fit_from_postfit(
            config['fit_info']['file'])

    print(f'[LoadFile] Truth value loaded from {truth_file}')
    show_value(truth_value, 'truth')
    show_frac (truth_value, 'truth')
    print(f'[LoadFile] Fit value loaded from {config["fit_info"]["file"]}')
    show_value(fit_value  , 'fit  ')
    show_frac (fit_value  , 'fit  ')
