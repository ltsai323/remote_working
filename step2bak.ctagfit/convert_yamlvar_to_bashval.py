#!/usr/bin/env python3
import logging

log = logging.getLogger(__name__)

def get_range_blah(varNAME, values):
    val_value = int(values['value'])
    val_error = int(values['error'])

    valL1 = val_value / 2
    valL2 = abs(val_value - val_error * 4)
    valL = valL1 if valL1 < valL2 else valL2

    valR1 = val_value * 2
    valR2 = val_value + val_error * 4
    valR = valR1 if valR1 > valR2 else valR2

    if valL < 500: valL = 0
    if valR < 500: valR = 500
    return { f'{varNAME}_rangeL': valL,  f'{varNAME}_rangeR': valR, f'{varNAME}_central': val_value }
def get_range_plusminus3sigma(varNAME, values):
    val_value = int(values['value'])
    val_error = int(values['error'])

    return { f'{varNAME}_rangeL': val_value-3*val_error,  f'{varNAME}_rangeR': val_value+3*val_error, f'{varNAME}_central': val_value }

def convertYamlVarToBash(inYAML, outBASH, varFUNC):
    import yaml
    with open(inYAML,'r') as fIN:
        load_vars = yaml.safe_load(fIN)

    log.debug('loaded variables')
    for varNAME, vals in load_vars.items():
        log.debug(f'  -> {varNAME}: {vals}')

    with open(outBASH, 'w') as fOUT:
        for varNAME, vals in load_vars.items():
            the_vars = varFUNC(varNAME,vals)
            for key,val in the_vars.items():
                fOUT.write(f'{key}={val}\n')




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format='[basicCONFIG] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    import sys
    #iYAML = 'bbb/datafit_fitinfo.yaml'
    #oBASH = 'hi.sh'
    iYAML = sys.argv[1]
    oBASH = sys.argv[2]

    #convertYamlVarToBash(iYAML,oBASH, get_range_plusminus3sigma)
    convertYamlVarToBash(iYAML,oBASH, get_range_blah)

