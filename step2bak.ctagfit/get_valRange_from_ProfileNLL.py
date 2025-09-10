#!/usr/bin/env python3
import logging

import ROOT
testfile = '/afs/cern.ch/work/l/ltsai/Work/CMSSW/CMSSW_13_0_21/src/macros/step2bak.ctagfit/psuedo_allgjets_10bins_3fit_psuedodata_GJetPythia1/binned_0_0_210_230/higgsCombine_scan_numL.MultiDimFit.mH120.root'




log = logging.getLogger(__name__)


class nll_and_fitval:
    def __init__(self, nllVALUE, fitVALUE):
        self.nllVALUE = nllVALUE
        self.fitVALUE = fitVALUE

    def __gt__(self, other):
        if isinstance(other, nll_and_fitval):
            return self.nllVALUE > other.nllVALUE
        return NotImplemented
    def __str__(self):
        return f'nll_and_fitval(NLL={self.nllVALUE}, val={self.fitVALUE})'


class LimitRange:
    def __init__(self, centralVAL, rangeL, rangeR):
        self.c = centralVAL
        self.l = rangeL
        self.r = rangeR
    def to_dict(self, tag):
        return { f'{tag}_central': self.c, f'{tag}_rangeL': self.l, f'{tag}_rangeR': self.r }
    def __str__(self):
        return f'LimitRange( val:{self.c:.2f}, range:({self.l:.2f},{self.r:.2f} )'
def get_limit_range(fIN, xVAR, scanSIGMA:int) -> LimitRange:
    in_file = ROOT.TFile.Open(fIN)
    in_tree = in_file.Get("limit")

    has_neg_NLL = False

    fit_center = nll_and_fitval(9999,0)
    maxNLL0 = nll_and_fitval(0,0)
    maxNLL1 = nll_and_fitval(0,0)
    for evt in in_tree:
        deltaNLL = getattr(evt, 'deltaNLL')
        fitvalue = getattr(evt, xVAR)
        this_evt = nll_and_fitval(deltaNLL,fitvalue)
        #if deltaNLL > 20: continue # only find range in +- 10sigma region
        if deltaNLL > scanSIGMA: continue # only find range in +- 10sigma region
        log.debug(this_evt)
        if deltaNLL < 0: has_neg_NLL = True

        if this_evt > maxNLL0: # find largest 2 NLL value as fit range L and R
            maxNLL1 = maxNLL0
            maxNLL0 = this_evt
        elif this_evt > maxNLL1:
            maxNLL1 = this_evt

        if this_evt <  fit_center: # fint smallest NLL value as fit center
            fit_center = this_evt


    if (fit_center.fitVALUE - maxNLL0.fitVALUE) * (fit_center.fitVALUE - maxNLL1.fitVALUE) < 0:
        ### in case of center between rangeL and rangeR
        rangeL = min(maxNLL0.fitVALUE,maxNLL1.fitVALUE)
        rangeR = max(maxNLL0.fitVALUE,maxNLL1.fitVALUE)
        log.debug(f'[GotNormalRange] get_limit_range() Got fit range [{rangeL},{rangeR}]')
        return LimitRange( fit_center.fitVALUE, rangeL, rangeR )

    ### in case of center is out of rangeL,rangeR. find larger deltaVAL as range (-2*deltaVAL, deltaVAL).
    log.debug(f'[GotNormalRange] get_limit_range() Got fit range [{maxNLL0.fitVALUE},{maxNLL1.fitVALUE}] and center {fit_center}')
    v = maxNLL0 if abs(maxNLL0.fitVALUE - fit_center.fitVALUE) > abs(maxNLL1.fitVALUE - fit_center.fitVALUE) else maxNLL1
    v0 = 3. * fit_center.fitVALUE - 2. * v.fitVALUE
    if v0 < 0: v0 = 0 # if range goes to minus value, force it as 0
    v1 = v.fitVALUE
    return LimitRange( fit_center.fitVALUE, v0, v1 ) if v1 > v0 else LimitRange( fit_center.fitVALUE, v1, v0 )





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
            format='[basicCONFIG] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')
    import sys
    opts = {}

    if len(sys.argv) >= 2+1:
        varNAME = sys.argv[1]
        scanFILE = sys.argv[2]
        scanSIGMA = int(sys.argv[3]) if len(sys.argv) > 2+1 else 10
    else:
        raise IOError('''args: 1.varNAME 2.scan.root 3.scan sigma (default 10)''')
        


    the_range = get_limit_range(scanFILE, varNAME, scanSIGMA)
    log.info(f'[GotFitRange] Fit range to "{varNAME}" is {the_range}')

    f_out_name = f'valRange_{varNAME}.sh'
    log.info(f'[OutputFile] bash scipt {f_out_name} generated')
    with open(f_out_name, 'w') as f_out:
        for bash_var, value in the_range.to_dict(varNAME).items():
            f_out.write(f'{bash_var}={value:.2f}\n')

