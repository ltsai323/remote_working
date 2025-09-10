#!/usr/bin/env python3
import yaml
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

def get_variable_from_yaml(inYAML, varNAME):
    with open(inYAML,'r') as fIN:
        load_vars = yaml.safe_load(fIN)
        return load_vars[varNAME]




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
            format='[basicCONFIG] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S')

    import sys
    #iYAML = 'bbb/datafit_fitinfo.yaml'
    #oBASH = 'hi.sh'
    iYAMLdefault = sys.argv[1] # datafit_datacard.BDT.defaultValue.yaml
    iYAMLnumSIGN = sys.argv[2] # scan.numSIGN2nd.yaml
    oBASH = sys.argv[3]

    nDATA = get_variable_from_yaml(iYAMLdefault, 'nDATA')
    nSIGN = get_variable_from_yaml(iYAMLnumSIGN, 'numSIGN')

    get_value = lambda theVAR: float(theVAR['value'])



    with open(oBASH, 'w') as f_out:
        f_out.write(f'numFAKE_central={get_value(nDATA)-get_value(nSIGN):.1f}')


