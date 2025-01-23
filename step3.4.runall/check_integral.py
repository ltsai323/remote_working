#!/usr/bin/env python3
import ROOT
import sys
FILE_IDENTIFIER = 'check_integral.py'
DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')



def getvalues(makehistFILE):
    inFILE = ROOT.TFile.Open(makehistFILE)
    hL = inFILE.Get('jettag0_gjetL_signalRegion').Integral()
    hC = inFILE.Get('jettag0_gjetC_signalRegion').Integral()
    hB = inFILE.Get('jettag0_gjetB_signalRegion').Integral()
    inFILE.Close()

    return (hL, hC, hB)


def formatted_output(
        pEtaBin, jEtaBin, pPtL, pPtR,
        vL, vC, vB
        ):
    out_content = {
            'pEtaBin': pEtaBin,
            'jEtaBin': jEtaBin,
            'pPtL': pPtL,
            'pPtR': pPtR,

            'b_value': vB,
            'b_error': 0.,
            #'b_xs': entries['nB'].value * value_to_xs,
            #'b_xs_err': entries['nB'].error / width,

            'c_value': vC,
            'c_error': 0.,
            #'c_xs': entries['nC'].value * value_to_xs,
            #'c_xs_err': entries['nC'].error / width,

            'l_value': vL,
            'l_error': 0.,
            #'l_xs': entries['nL'].value * value_to_xs,
            #'l_xs_err': entries['nL'].error / width,

            #'fake_value': entries['nFAKE'].value,
            #'fake_error': entries['nFAKE'].error,
            #'fake_xs': entries['nFAKE'].value * value_to_xs,
            #'fake_xs_err': entries['nFAKE'].error / width,
            }
    return out_content

def output_csv_file(csv_content:dict, outCSVfile:str):
    filename = outCSVfile

    import csv
    IGNORE_INVALID_CONTENT = True
    if IGNORE_INVALID_CONTENT:
        BUG('[Ignoring] ignoring invalid entry')
        csv_content = { k:v for k,v in csv_content.items() if not v<0 } # ignore invalid entry
    with open(filename, 'a', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=csv_content.keys())

        ### If the file is empty or newly created, write the header first
        if f_out.tell() == 0: writer.writeheader()

        writer.writerow(csv_content)
    info(f'[Export] put info into csv file "{ filename }"')

if __name__ == '__main__':
    import sys
    makehsit_file = sys.argv[1]
    output_csv = sys.argv[2]
    pEtaBin, jEtaBin, pPtL, pPtR = sys.argv[3:]

    valL, valC, valB = getvalues(makehsit_file)
    output_dict = formatted_output(
            int(pEtaBin), int(jEtaBin), int(pPtL), int(pPtR),
            valL, valC, valB)
    output_csv_file(output_dict, output_csv)

