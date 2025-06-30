#!/usr/bin/env python3

import csv
from uncertainties import ufloat
import ROOT
import ctypes


FILE_IDENTIFIER = 'closure_check.export_estimation'
DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')



HIST_NAMES = {
'WP0': 'BDT_data_signalRegion',
'WPcL': 'BDTWPcL_data_signalRegion',
'WPcM': 'BDTWPcM_data_signalRegion',
'WPcT': 'BDTWPcT_data_signalRegion',
'WPbL': 'BDTWPbL_data_signalRegion',
'WPbM': 'BDTWPbM_data_signalRegion',
'WPbT': 'BDTWPbT_data_signalRegion',
'truthL': 'BDT_ljet_truthvalue',
'truthC': 'BDT_cjet_truthvalue',
'truthB': 'BDT_bjet_truthvalue',
}

def generate_csvfile(csvCONTENT:dict, outCSVfile:str):
    filename = outCSVfile

    import csv
    csv_content = csvCONTENT
    csv_content = { k:v for k,v in csvCONTENT.items() if not v<0 } # ignore invalid entry
    if len(csv_content) != len(csvCONTENT):
        BUG('[Ignoring] ignoring invalid entry')


    with open(filename, 'a', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=csv_content.keys())

        ### If the file is empty or newly created, write the header first
        if f_out.tell() == 0:
            writer.writeheader()
            info(f'[Export] put info into csv file "{ filename }"')

        writer.writerow(csv_content)
    #info(f'[Export] put info into csv file "{ filename }"')


def get_intragral_err(tFILE, hNAME):
    h = tFILE.Get(hNAME)
    #the_error = ROOT.Double_t()
    the_error = ctypes.c_double()
    the_value = h.IntegralAndError(1,h.GetNbinsX(), the_error)

    return ufloat(the_value, the_error.value)


def mainfunc(
        makehistFILE:str,
        pETAbin:int, jETAbin:int,pPTbin:int,
        fakeFITINFO:str='fake_merged_fitinfo.csv',
        fakeTRUTHINFO:str='fake_merged_truthinfo.csv',
        usedWPc:str='WPcM', usedWPb:str='WPbL'
        ):
    ff = ROOT.TFile.Open(makehistFILE)

    pEtaBin = int(pETAbin)
    jEtaBin = int(jETAbin)
    pPtBin  = int(pPTbin)

    numWP0 = get_intragral_err(ff, HIST_NAMES['WP0'])
    numWPc = get_intragral_err(ff, HIST_NAMES['WPcM'])
    numWPb = get_intragral_err(ff, HIST_NAMES['WPbL'])

    numTruthL = get_intragral_err(ff, HIST_NAMES['truthL'])
    numTruthC = get_intragral_err(ff, HIST_NAMES['truthC'])
    numTruthB = get_intragral_err(ff, HIST_NAMES['truthB'])

    entry_fake_numer = {
            'pEtaBin': pEtaBin,
            'jEtaBin': jEtaBin,
            'pPtBin':  pPtBin,
            'N_WP0':     numWP0.nominal_value,
            'N_WP0error':numWP0.std_dev,
            'N_WPc':     numWPc.nominal_value,
            'N_WPcerror':numWPc.std_dev,
            'N_WPb':     numWPb.nominal_value,
            'N_WPberror':numWPb.std_dev,
            }
    generate_csvfile(entry_fake_numer, fakeFITINFO)

    entry_truth_value = {
            'pEtaBin': pEtaBin,
            'jEtaBin': jEtaBin,
            'pPtBin':  pPtBin,
            'numL':numTruthL.nominal_value,
            'errL':numTruthL.std_dev,
            'numC':numTruthC.nominal_value,
            'errC':numTruthC.std_dev,
            'numB':numTruthB.nominal_value,
            'errB':numTruthB.std_dev,
            }
    generate_csvfile(entry_truth_value, fakeTRUTHINFO)



if __name__ == "__main__":
    import sys

    inFILE  = str(sys.argv[1])
    pEtaBin = int(sys.argv[2])
    jEtaBin = int(sys.argv[3])
    pPtBin  = int(sys.argv[4])

    fitinfo = str(sys.argv[5]) if len(sys.argv)>5 else 'fake_merged_fitinfo.csv'
    truthinfo = str(sys.argv[6]) if len(sys.argv)>6 else 'fake_merged_fitinfo.csv'

    usedWPc = str(sys.argv[7]) if len(sys.argv)>7 else 'WPcM'
    usedWPb = str(sys.argv[8]) if len(sys.argv)>8 else 'WPbL'


    mainfunc(inFILE,
            pEtaBin, jEtaBin, pPtBin,
            fitinfo, truthinfo,
            usedWPc,usedWPb
            )
