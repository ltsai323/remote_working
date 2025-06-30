#!/usr/bin/env python3
import yaml

if __name__ == "__main__":
    import sys
    inFILE = sys.argv[1]
    showVAR = sys.argv[2]

    with open(inFILE, 'r') as fIN:
        print( yaml.safe_load(fIN) [showVAR] )

