#!/usr/bin/env python3
import csv
import ROOT
from array import array
from collections import namedtuple
CollectedData = namedtuple('CollectedData', 'all_pts fit_yieldL fit_yieldC fit_yieldB fit_yieldF fit_XSL fit_XSC fit_XSB fit_XSF')
FILE_IDENTIFIER = 'csv_to_root.py'
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
        self.pPtL = int(csvENTRY['pPtL'])
        self.pPtR = int(csvENTRY['pPtR'])
        #if self.pPtR == -1: self.pPtR = 1500
    def __str__(self):
        return f'Binning(pEta={self.pEtaBin},jEta={self.jEtaBin}, pPt={self.pPtL})'

class CSVEntry:
    def __init__(self, csvENTRY, valNAME, errNAME):
        self.val = float(csvENTRY.get(valNAME, -1))
        self.err = float(csvENTRY.get(errNAME, -1))
    def is_valid(self): return self.val != -1 and self.err != -1
    def __repr__(self):
        return f'({self.val:.2e}+-{self.err:.2e})'

def FitYieldB(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'b_value', 'b_error')
def FitYieldC(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'c_value', 'c_error')
def FitYieldL(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'l_value', 'l_error')
def FitYieldFake(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'fake_value', 'fake_error')
def FitXSB(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'b_xs', 'b_xs_err')
def FitXSC(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'c_xs', 'c_xs_err')
def FitXSL(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'l_xs', 'l_xs_err')
def FitXSFake(csvENTRY) -> CSVEntry:
    return CSVEntry(csvENTRY, 'fake_xs', 'fake_xs_err')

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
    fit_yieldL = BinningCollection()
    fit_yieldF = BinningCollection()

    fit_XSB = BinningCollection()
    fit_XSC = BinningCollection()
    fit_XSL = BinningCollection()
    fit_XSF = BinningCollection()

    with open(inFILE, 'r') as f_in:
        reader = csv.DictReader(f_in)
        for entry in reader:
            binning = Binning(entry)
            fit_yieldB.add_entry(binning,FitYieldB(entry))
            fit_yieldC.add_entry(binning,FitYieldC(entry))
            fit_yieldL.add_entry(binning,FitYieldL(entry))
            fit_yieldF.add_entry(binning,FitYieldFake(entry))

            fit_XSB.add_entry(binning,FitXSB(entry))
            fit_XSC.add_entry(binning,FitXSC(entry))
            fit_XSL.add_entry(binning,FitXSL(entry))
            fit_XSF.add_entry(binning,FitXSFake(entry))

    ptrange1 = fit_yieldL.pt_range()
    ptrange2 = fit_yieldF.pt_range()
    all_pts = ptrange1 if len(ptrange1)>len(ptrange2) else ptrange2
    return CollectedData(
            all_pts,
            fit_yieldL, fit_yieldC, fit_yieldB, fit_yieldF,
            fit_XSL, fit_XSC, fit_XSB, fit_XSF,
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
    hists = record_to_hist(collectedDATA, 'fit_yieldL')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_yieldC')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_yieldB')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_yieldF')
    for h in hists: h.Write()

    hists = record_to_hist(collectedDATA, 'fit_XSL')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_XSC')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_XSB')
    for h in hists: h.Write()
    hists = record_to_hist(collectedDATA, 'fit_XSF')
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
    #show_binning_collection(csv_info.fit_yieldF)
    #print(csv_info.all_pts)
    create_root(csv_info, outFILE)

