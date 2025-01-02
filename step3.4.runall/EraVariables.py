#!/usr/bin/env python3

### in fb inv
LUMINOSITY = {
        '2022EE': 333,
        'UL2016PostVFP': 19.52,
        }
def luminosity(dataERA:str) -> float:
    if dataERA not in LUMINOSITY.keys():
        raise IOError(f'[InvalidKey] input data era "{ dataERA }" is invalid. Available options are {LUMINOSITY.keys()}')
    return 1000. * LUMINOSITY[dataERA] # convert fb inv to pb inv
