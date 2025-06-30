#!/usr/bin/env python3

import yaml
from uncertainties import ufloat
FILE_IDENTIFIER = 'merge_fitinfo'
DEBUG_MODE = True
def BUG(mesg):
    if DEBUG_MODE:
        print(f'b-{FILE_IDENTIFIER}@ {mesg}')
def info(mesg):
    print(f'i-{FILE_IDENTIFIER}@ {mesg}')



class YamlContent:
    def __init__(self, yamlFILE):
        with open(yamlFILE, 'r') as fIN:
            content = yaml.safe_load(fIN)

        self.value = float(content['nSIGN']['value'])
        self.error = float(content['nSIGN']['error'])

    @property
    def fitvalue(self): return ufloat(self.value,self.error)


def generate_csvfile(csv_content:dict, outCSVfile:str):
    filename = outCSVfile

    import csv
    IGNORE_INVALID_CONTENT = True
    if IGNORE_INVALID_CONTENT:
        BUG('[Ignoring] ignoring invalid entry')
        csv_content = { k:v for k,v in csv_content.items() if not v<0 } # ignore invalid entry
    with open(filename, 'a', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=csv_content.keys())

        ### If the file is empty or newly created, write the header first
        if f_out.tell() == 0:
            writer.writeheader()
            info(f'[Export] put info into csv file "{ filename }"')

        writer.writerow(csv_content)
    #info(f'[Export] put info into csv file "{ filename }"')
if __name__ == "__main__":
    import sys
    from collections import namedtuple
    output_csv_file = 'merged_fitinfo.csv'
    InArgs = namedtuple('InArgs', 'pEtaBin jEtaBin pPtBin fitinfo_WP0 fitinfo_WPc fitinfo_WPb')
    args = InArgs(*sys.argv[1:])


    N_WP0 = YamlContent(args.fitinfo_WP0)
    N_WPc = YamlContent(args.fitinfo_WPc)
    N_WPb = YamlContent(args.fitinfo_WPb)


    csv_content = {
            'pEtaBin': int(args.pEtaBin), 'jEtaBin': int(args.jEtaBin), 'pPtBin': int(args.pPtBin),
            'N_WP0': N_WP0.fitvalue.nominal_value,
            'N_WP0error': N_WP0.fitvalue.std_dev,
            'N_WPc': N_WPc.fitvalue.nominal_value,
            'N_WPcerror': N_WPc.fitvalue.std_dev,
            'N_WPb': N_WPb.fitvalue.nominal_value,
            'N_WPberror': N_WPb.fitvalue.std_dev,
            }
    generate_csvfile(csv_content, output_csv_file)
