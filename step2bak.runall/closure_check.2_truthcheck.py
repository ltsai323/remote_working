#!/usr/bin/env python3
import csv
from uncertainties import ufloat
import uncertainties
import ROOT
from array import array

DEBUG_MODE = False
FILE_IDENTIFIER = 'closure_check.2_truthcheck.py'
def warning(mesg):
    print(f'WARN-{FILE_IDENTIFIER}@ {mesg}')


def isBinning(entry:dict, pETAbin, jETAbin, pPTbin):
    if int(entry['pPtBin'] ) != pPTbin: return False
    if int(entry['jEtaBin']) != jETAbin: return False
    if int(entry['pEtaBin']) != pETAbin: return False
    return True
def AtBinning(entries:list, pETAbin, jETAbin, pPTbin):
    selected_entry = [ entry for entry in entries if isBinning(entry, pETAbin,jETAbin,pPTbin) ]
    if len(selected_entry) != 1:
        if DEBUG_MODE:
            raise IOError(f'[Confused Binning] Binning({pETAbin},{jETAbin},{pPTbin}) matched entry "{selected_entry}"')
        return None
    return selected_entry[0]


class Value:
    def __init__(self, bVAL, bERR, cVAL, cERR, fracCB):
        self.valB = ufloat( float(bVAL), float(bERR) )
        self.valC = ufloat( float(cVAL), float(cERR) )
        self.fracCB = float(fracCB)
    def __str__(self):
        return f'[Value] b={self.valB} c={self.valC} c/b={self.fracCB}'


def ReadCSVEntries(csvFILE) -> list:
    with open(csvFILE, 'r') as fCSV:
        csvENTRIES = csv.DictReader(fCSV)
        return [ csvENTRY for csvENTRY in csvENTRIES ]

class FitValue(Value):
    def __init__(self, entry:dict):
        super().__init__(
                entry['yield_b'], entry['error_b'],
                entry['yield_c'], entry['error_c'],
                entry['frac_c_b']
                )
class TruthValue(Value):
    def __init__(self, entry:dict):
        super().__init__(
                entry['numB'],entry['errB'],
                entry['numC'],entry['errC'],
                float(entry['numC']) / float(entry['numB']) if float(entry['numB']) > 0 else 0.
                )



def mainfunc(calculatedCSV, truthCSV, ptBINNINGs:list):
    f = calculatedCSV

    fit_entries   = ReadCSVEntries(calculatedCSV)
    truth_entries = ReadCSVEntries(truthCSV)

    pt_binning = array('f',ptBINNINGs)
    hist_pt = lambda histNAME: ROOT.TH1F(histNAME,histNAME, len(pt_binning)-1, pt_binning)
    def GetPtHist(histNAME, ptSPECTRUM):
        h = hist_pt(histNAME)
        for pPtBin, val in enumerate(ptSPECTRUM):
            binIdx = pPtBin+1
            if isinstance(val,float):
                h.SetBinContent(binIdx, val)
            if isinstance(val,uncertainties.core.Variable): # ufloat
                h.SetBinContent(binIdx, val.nominal_value)
                h.SetBinError  (binIdx, val.std_dev)
        return h



    hists = []
    estimation_diffC = []
    estimation_diffB = []
    for pEtaBin in [0,1]:
        for jEtaBin in [0,1]:
            fitval = []
            truth = []
            for pPtBin in range(len(ptBINNINGs)-1):
                fit_entry = AtBinning(fit_entries, pEtaBin,jEtaBin,pPtBin)
                truth_entry = AtBinning(truth_entries, pEtaBin,jEtaBin,pPtBin)
                fitvalue = FitValue(fit_entry)
                truthvalue = TruthValue(truth_entry)
                fitval.append(fitvalue)
                truth.append(truthvalue)

                if fitvalue.valB < 0 or fitvalue.valC < 0:
                    warning(f'[GotNegativeValue@bin({pEtaBin},{jEtaBin},{pPtBin})] fitted B : {fitvalue.valB}.  fitted C : {fitvalue.valC} IGNORE this entry')
                    continue

                significance = lambda valF, valT: (valF.nominal_value-valT.nominal_value) / valF.std_dev
                estimation_diffC.append( significance(fitvalue.valC,truthvalue.valC) )
                estimation_diffB.append( significance(fitvalue.valB,truthvalue.valB) )


            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_fitnumB', [v.valB for v in fitval]) )
            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_fitnumC', [v.valC for v in fitval]) )
            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_fitfracCB', [v.fracCB for v in fitval]) )

            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_truthnumB', [v.valB for v in truth]) )
            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_truthnumC', [v.valC for v in truth]) )
            hists.append( GetPtHist(f'bin{pEtaBin}{jEtaBin}_truthfracCB', [v.fracCB for v in truth]) )

    fOUT = ROOT.TFile.Open('closure_check.2_truthcheck.root', 'RECREATE')
    fOUT.cd()
    for h in hists:
        h.Write()

    LOWER=-13
    UPPER=13
    hSigC = ROOT.TH1F('significanceC', 'significance plot', 30, LOWER,UPPER)
    for est_sigC in estimation_diffC:
        if est_sigC < LOWER or est_sigC > UPPER:
            print(f'[OutOfBound] significance of C is {est_sigC} is out of bound')
            continue
        hSigC.Fill(est_sigC)
    hSigC.Write()
    hSigB = ROOT.TH1F('significanceB', 'significance plot', 30, LOWER,UPPER)
    for est_sigB in estimation_diffB:
        if est_sigB < LOWER or est_sigB > UPPER:
            print(f'[OutOfBound] significance of B is {est_sigB} is out of bound')
            continue
        hSigB.Fill(est_sigB)
    hSigB.Write()
    fOUT.Close()
    print(f'[ROOTexported] {fOUT.GetName()} generated')





if __name__ == "__main__":
    # python3 closure_check.2_truthcheck.py $calculated_xs_csv $merged_info_truth_csv ${pPtRange[@]}
    from collections import namedtuple
    import sys
    truth_csv = sys.argv[1]
    calculated_csv = sys.argv[2]
    pt_binning = [ int(v) for v in sys.argv[3:] ]

    truth_csv = 'fake_merged_truthinfo.csv'
    calculated_csv = 'calculated_xs.csv'
    mainfunc(calculated_csv,truth_csv, pt_binning)
