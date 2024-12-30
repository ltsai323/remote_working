#!/usr/bin/env python3
import ROOT
from collections import namedtuple
import os
import sys
import yaml
from pprint import pprint

def info(mesg):
    print(f'i@ {mesg}')


def get_entries(tFILE:ROOT.TFile, histNAME='jettag0_data_dataSideband'):
    h = tFILE.Get(histNAME)
    return h.Integral()


inARGs = namedtuple('inARGs', 'inFILE histNAME outNAME fracL fracC fracB fracFAKE')
def get_yaml_configurables( yamlFILE:str ):
    yaml_default_content = '''
nB:
  composition: 0.03
nC:
  composition: 0.14
nL:
  composition: 0.8
nFAKE:
  composition: 0.
    '''
    if yamlFILE:
        with open(yamlFILE,'r') as fIN:
            yaml_configurables = yaml.safe_load(fIN)
        info(f'[get_yaml_configurables] Got yaml file "{ yamlFILE }"')
    else:
        yaml_configurables = yaml.safe_load(yaml_default_content)
        info(f'[get_yaml_configurables] No input yaml found, use default yaml configurations.')


    if 'nFAKE' not in yaml_configurables.keys():
        yaml_configurables['nFAKE'] = { 'composition': 0.1 }
        info('[get_yaml_configurables] No "nFAKE" in yaml configurations, use 10%')
    return yaml_configurables
def IOargs(argv) -> inARGs:
    def print_help():
        raise IOError(
    '''
    access input args

    arg0: input root file
    arg1: data hist name
    arg2: output bash name
    arg3 (opt): input yaml file contains the L/C/B compositions
    ''' )
    defaultVAL = [None, None, None, None]
    try:
        inFILE = argv[1]
        hNAME  = argv[2]
        outFILE= argv[3]
        yaml_content = get_yaml_configurables( argv[4] if len(argv)>4 else None )
    except IndexError as e:
        print_help()
    

    return inARGs(
            inFILE, hNAME, outFILE,
            yaml_content['nL']['composition'],
            yaml_content['nC']['composition'],
            yaml_content['nB']['composition'],
            yaml_content['nFAKE']['composition']
    )

    
if __name__ == "__main__":
    arg = IOargs(sys.argv)

    tFILE = ROOT.TFile.Open(arg.inFILE)
    entries = get_entries(tFILE, arg.histNAME)
    

    entries_without_fake = entries * (1. - float(arg.fracFAKE) )
    out_template = {
            'nDATA': entries,
            'initL': entries_without_fake * float(arg.fracL),
            'initC': entries_without_fake * float(arg.fracC),
            'initB': entries_without_fake * float(arg.fracB),
            'initSIGN': entries * (1.-float(arg.fracFAKE)),
            'initFAKE': entries * float(arg.fracFAKE),
            }
    info('[UsedValue]')
    info( '    nDATA   = {}'.format(out_template['nDATA']))
    info( '    initSIGN= {} with {}% composition'.format(out_template['initSIGN'], 100.-float(arg.fracFAKE)*100.))
    info( '    initFAKE= {} with {}% composition'.format(out_template['initFAKE'], float(arg.fracFAKE)*100.))
    info( '    initL   = {} with frac = {}'.format(out_template['initL'],arg.fracL))
    info( '    initC   = {} with frac = {}'.format(out_template['initC'],arg.fracC))
    info( '    initB   = {} with frac = {}'.format(out_template['initB'],arg.fracB))


    with open(arg.outNAME, 'w') as f_out:
        f_out.write('\n'.join( f'{key}={value}' for key,value in out_template.items() ))
