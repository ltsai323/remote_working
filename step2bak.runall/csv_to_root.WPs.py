#!/usr/bin/env python3
import csv
import ROOT
from array import array
from collections import namedtuple
from uncertainties import ufloat
#CollectedData = namedtuple('CollectedData', 'all_pts fit_yieldL fit_yieldC fit_yieldB fit_yieldF fit_XSL fit_XSC fit_XSB fit_XSF fracL fracC fracB')
CollectedData = namedtuple('CollectedData', 'all_pts fit_yieldB  fit_yieldC fit_XSB  fit_XSC fit_CoverB')
load_csv_labels_value_and_error = namedtuple('load_csv_labels_value_and_error', 'value error')
FILE_IDENTIFIER = 'csv_to_root.WPs.py'
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')

DEBUG_MODE = False
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')


class Binning:
    def __init__(self, csvENTRY):
        self.pEtaBin = int(csvENTRY['pEtaBin'])
        self.jEtaBin = int(csvENTRY['jEtaBin'])
        self.pPtL = int( float(csvENTRY['pPtL']) )
        self.pPtR = int( float(csvENTRY['pPtR']) )
        #if self.pPtR == -1: self.pPtR = 1500
    def __str__(self):
        return f'Binning(pEta={self.pEtaBin},jEta={self.jEtaBin}, pPt={self.pPtL})'

class CSVEntry:
    def __init__(self, csvENTRY, valueANDerror:load_csv_labels_value_and_error):
        self.val = float(csvENTRY.get(valueANDerror.value, -1))
        self.err = float(csvENTRY.get(valueANDerror.error, -1))
    def is_valid(self): return self.val != -1 and self.err != -1
    def __repr__(self):
        return f'({self.val:.2e}+-{self.err:.2e})'


def FitYieldB(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, load_csv_labels_value_and_error('yield_b', 'error_b'))
def FitYieldC(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, load_csv_labels_value_and_error('yield_b', 'error_c'))
def FitXSB(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, load_csv_labels_value_and_error('xs_b', 'xs_b_error'))
def FitXSC(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, load_csv_labels_value_and_error('xs_c', 'xs_c_error'))
def FitCoverB(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, load_csv_labels_value_and_error('frac_c_b', 'frac_c_b'))

class BinningCollection:
    def __init__(self):
        self.bin_0_0 = {}
        self.bin_0_1 = {}
        self.bin_1_0 = {}
        self.bin_1_1 = {}
        self.allpts = []
    def add_entry(self, binning:Binning, entry:CSVEntry):
        if not entry.is_valid(): return
        if binning.pEtaBin == 0 and binning.jEtaBin == 0:
            self.bin_0_0[binning.pPtL] = entry
        if binning.pEtaBin == 0 and binning.jEtaBin == 1:
            self.bin_0_1[binning.pPtL] = entry
        if binning.pEtaBin == 1 and binning.jEtaBin == 0:
            self.bin_1_0[binning.pPtL] = entry
        if binning.pEtaBin == 1 and binning.jEtaBin == 1:
            self.bin_1_1[binning.pPtL] = entry
        self.allpts.append( binning.pPtL )
        self.allpts.append( binning.pPtR )
    def pt_range(self):
        return sorted(list(set(self.allpts)))
    def is_valid(self):
        return len(self.allpts) > 0

def show_binning_collection(binnCOLL:BinningCollection):
    print(f'pEta0 jEta0 : {binnCOLL.bin_0_0}')
    print(f'all pt : {binnCOLL.pt_range()}')


def read_csv_entry(inFILE) -> CollectedData:
    fit_yieldB = BinningCollection()
    fit_yieldC = BinningCollection()

    fit_XSB = BinningCollection()
    fit_XSC = BinningCollection()

    fit_CoverB = BinningCollection()

    with open(inFILE, 'r') as f_in:
        reader = csv.DictReader(f_in)
        for entry in reader:
            binning = Binning(entry)
            fit_yieldB.add_entry(binning,FitYieldB(entry))
            fit_yieldC.add_entry(binning,FitYieldC(entry))

            fit_XSB.add_entry(binning,FitXSB(entry))
            fit_XSC.add_entry(binning,FitXSC(entry))

            fit_CoverB.add_entry(binning,FitCoverB(entry))

    ptrange1 = fit_yieldC.pt_range()
    ptrange2 = fit_yieldB.pt_range()
    all_pts = ptrange1 if len(ptrange1)>len(ptrange2) else ptrange2
    return CollectedData(
            all_pts,
            fit_yieldB, fit_yieldC,
            fit_XSB, fit_XSC,
            fit_CoverB
            )

def create_root(collectedDATA:CollectedData, outFILE:str):
    def get_var_with_check(s, name):
        if not hasattr(s,name):
            info(f'[ignored] collected data does not own instance "{ name }"')
            return
        inst = getattr(s,name)
        if inst.is_valid(): return inst
        info(f'[ignored] "{ name }" in collected data does not contain any data.')
        return None
    def BinninColl_to_TH1F(binCOLL:BinningCollection, binNAME:str, nameTAG:str) -> ROOT.TH1F:
        if binCOLL == None: return None
        full_pt_range = binCOLL.pt_range()
        bin_instance = getattr(binCOLL, binNAME)
        maxbin = len(bin_instance)

        h = ROOT.TH1F(f'{binNAME}_{nameTAG}', nameTAG, maxbin, array('d',full_pt_range[:maxbin+1]))
        BUG(f'[all pt ranges] "{ full_pt_range }"')
        BUG(f'[all bins] "{bin_instance.keys()}"')
        for ptL, entry in bin_instance.items():
            bin_idx = 1 + full_pt_range.index(ptL)
            BUG(f'[BinIdx] ptL "{ ptL }" got bin index "{ bin_idx }"')
            h.SetBinContent(bin_idx,entry.val)
            h.SetBinError  (bin_idx,entry.err)
        return h

    def record_to_hist(collDATA,name) -> list:
        collected_hists = []
        inst = get_var_with_check(collectedDATA, name)
        if inst: collected_hists.append(BinninColl_to_TH1F(inst, 'bin_0_0', name))
        inst = get_var_with_check(collectedDATA, name)
        if inst: collected_hists.append(BinninColl_to_TH1F(inst, 'bin_0_1', name))
        inst = get_var_with_check(collectedDATA, name)
        if inst: collected_hists.append(BinninColl_to_TH1F(inst, 'bin_1_0', name))
        inst = get_var_with_check(collectedDATA, name)
        if inst: collected_hists.append(BinninColl_to_TH1F(inst, 'bin_1_1', name))
        return collected_hists


    out_file = ROOT.TFile(outFILE, 'recreate')
    out_file.cd()
    hists = record_to_hist(collectedDATA, 'fit_yieldC')
    for h in hists: h.Write()

    hists = record_to_hist(collectedDATA, 'fit_XSC')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_XSB')
    for h in hists: h.Write()

    hists = record_to_hist(collectedDATA, 'fit_CoverB')
    for h in hists: h.Write()

    out_file.Close()
    info(f'[ExportFile] Root file "{ outFILE }" generated')


if __name__ == "__main__":
    import sys
    inARGs = namedtuple('inARGs', 'in_csv')
    in_args = inARGs(*sys.argv[1:])
    inFILE = in_args.in_csv
    outFILE = inFILE.replace('.csv', '.root')

    csv_info = read_csv_entry(inFILE)

    create_root(csv_info, outFILE)

