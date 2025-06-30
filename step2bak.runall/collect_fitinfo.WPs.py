#!/usr/bin/env python3
import yaml
''' Append collected information to a file.
So this code should be executed for every binning.
Every execution adds a new entry to csv file.
'''

FILE_IDENTIFIER = 'collect_fitinfo.py'
DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')

def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')

def warning(mesg):
    print(f'WARN-{FILE_IDENTIFIER}@ {mesg}')

TEST_YAML = '''
nB:
  composition: 0.047080828380427105
  error: 6.282978207745046
  value: 32.015343802428156
nC:
  composition: 0.09383525852500543
  error: 22.420266156942436
  value: 63.80873416655299
nL:
  composition: 0.8590839130945676
  error: 23.058853254561427
  value: 584.1840039563124
'''

INVALID_VAL = -1 # use val<0 to reject invalid values
class Entry:
    def __init__(self, yamlENTRY:dict):
        self.val = float(yamlENTRY.get('value', 0))
        self.err = float(yamlENTRY.get('error', 0))
        self.frac = float(yamlENTRY.get('composition', 0))
    def __str__(self):
        return f'Entry(value={self.val:.2f},error={self.err:.2f},composition={self.frac:.3f})'
    def empty(self):
        return self.val == 0 and self.err == 0
    @property
    def value(self): return self.val if not self.empty() else INVALID_VAL
    @property
    def error(self): return self.err if not self.empty() else INVALID_VAL

def testfunc_Entry():
    yaml_configurations = yaml.safe_load(TEST_YAML)
    entry_b = Entry(yaml_configurations['nB'])
    entry_c = Entry(yaml_configurations['nC'])
    entry_l = Entry(yaml_configurations['nL'])
    print(entry_b)
    print(entry_c)
    print(entry_l)
    exit()

def GetEntryIgnoreError(yamlCONF:dict, loadKEY:str):
    if not loadKEY in yamlCONF.keys():
        info(f'[skipped] key "{ loadKEY }" is ignored from yaml file.')
        return Entry({})
    return Entry(yamlCONF[loadKEY])

# convert string to int and handle input 
class Binning:
    def __init__(self, pETAbin, jETAbin, pPTlow, pPThigh):
        self.pEtaBin = int(pETAbin)
        self.jEtaBin = int(jETAbin)
        self.pPtL = int(pPTlow)
        self.pPtR = int(pPThigh)
def pho_eta_width(etaBIN:int):
    if etaBIN == 0: return 2. * 1.4442
    if etaBIN == 1: return 2. * (2.5 - 1.566)
    raise IOError(f'[InvalidBin] photon eta bin "{ etaBIN }" is not defined')
def jet_eta_width(etaBIN:int):
    if etaBIN == 0: return 2. * 1.5
    if etaBIN == 1: return 2. * (2.5 - 1.5)
    raise IOError(f'[InvalidBin] jet eta bin "{ etaBIN }" is not defined')
PT_MAX = 1500



def calculate_yaml_information(yamlCONFIGs:dict, binning:Binning, additionalEFFICIENCY:float=1.0):
    content = yamlCONFIGs

    entries = {}
    entries["nB"   ] = GetEntryIgnoreError(content,"nB")
    entries["nC"   ] = GetEntryIgnoreError(content,"nC")
    entries["nL"   ] = GetEntryIgnoreError(content,"nL")
    entries["nFAKE"] = GetEntryIgnoreError(content,"nFAKE")
    entries["nSIGN"] = GetEntryIgnoreError(content,"nSIGN")

    ptR = binning.pPtR if binning.pPtR != -1 else PT_MAX
    if binning.pPtR == -1:
        info(f'[MaxPtBin] Use photon pt {PT_MAX} GeV as the upper bond')
    width = additionalEFFICIENCY * \
            pho_eta_width(binning.pEtaBin) * \
            jet_eta_width(binning.jEtaBin) * \
            (ptR - binning.pPtL)
    value_to_xs = 1. / width
    out_content = {
            'pEtaBin': binning.pEtaBin,
            'jEtaBin': binning.jEtaBin,
            'pPtL': binning.pPtL,
            'pPtR': ptR,

            'b_value': entries['nB'].value,
            'b_error': entries['nB'].error,
            'b_xs': entries['nB'].value * value_to_xs,
            'b_xs_err': entries['nB'].error / width,

            'c_value': entries['nC'].value,
            'c_error': entries['nC'].error,
            'c_xs': entries['nC'].value * value_to_xs,
            'c_xs_err': entries['nC'].error / width,

            'l_value': entries['nL'].value,
            'l_error': entries['nL'].error,
            'l_xs': entries['nL'].value * value_to_xs,
            'l_xs_err': entries['nL'].error / width,

            'fake_value': entries['nFAKE'].value,
            'fake_error': entries['nFAKE'].error,
            'fake_xs': entries['nFAKE'].value * value_to_xs,
            'fake_xs_err': entries['nFAKE'].error / width,
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

def mainfunc(
        fitinfoYAML_WP0:str,
        fitinfoYAML_WPc:str,
        fitinfoYAML_WPb:str,
        outputCSVfile:str,
        dataERA:str,
        pETAbin:str,jETAbin:str,pPTl:str,pPTr:str,
        ):
    try:
        with open(fitinfoYAML, 'r') as fIN:
            info(f'[LoadFitInfo] Loading "{ fitinfoYAML }"')
            content = yaml.safe_load(fIN)
    except FileNotFoundError as e:
        BUG(f'[skipped] File "{ fitinfoYAML }" not found because the fitting failed. skip it')
        exit()

    import EraVariables
    luminosity = EraVariables.luminosity(dataERA)
    binning = Binning(pETAbin,jETAbin,pPTl,pPTr)

    record_content = calculate_yaml_information(content, binning, luminosity)
    output_csv_file(record_content, args.out_csv)

if __name__ == "__main__":
    #testfunc_Entry()

    import sys
    from collections import namedtuple
    InArgs = namedtuple('InArgs', 'fitinfo_WP0_yaml fitinfo_WPc_yaml fitinfo_WPl_yaml out_csv data_era pEtaBin jEtaBin pPtL pPtR')
    args = InArgs(*sys.argv[1:])

    mainfunc(
            args.fitinfo_WP0_yaml,
            args.fitinfo_WPc_yaml,
            args.fitinfo_WPl_yaml,
            args.out_csv,
            args.data_era,
            args.pEtaBin, args.jEtaBin,
            args.pPtL, args.pPtR
            )

