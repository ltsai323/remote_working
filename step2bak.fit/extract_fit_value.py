#!/usr/bin/env python3

import ROOT
from collections import namedtuple
def info(mesg):
    print(f'i@ {mesg}')


def GetSnapshotAtMultiDimFit(wSPACE, snapshotNAME:str='MultiDimFit'):
    return wSPACE.getSnapshot(snapshotNAME)

def GetFitValueFromMultiDimFit(sSHOT, var:str):
    loaded_var = sSHOT.find(var)
    return loaded_var.getVal()

def GetFitErrorFromMultiDimFit(sSHOT, var:str):
    loaded_var = sSHOT.find(var)
    return loaded_var.getError()








def mainfunc_getGJetinfo(inputFILEname:str,outFILEname:str):
    #inputFILEname = "higgsCombineTest.MultiDimFit.mH120.root"
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valS = snapshot.find('nSIGN')
    valF = snapshot.find('nFAKE')
    totVal = valS.getVal() + valF.getVal()


    def extract_info(v, totalVALUE:float):
        return {
                'value': v.getVal(),
                'error': v.getError(),
                #'errHi': v.getErrorHi(),
                #'errLo': v.getErrorLo(),
                'composition': v.getVal() / totalVALUE,
        }
    output = {
            'nSIGN': extract_info(valS, totVal),
            'nFAKE': extract_info(valF, totVal),
    }

    import yaml
    info(f'[GenerateYAML] file "{ outFILEname }"')
    with open(outFILEname, 'w') as f_out:
        yaml.dump(output, f_out, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outFILEname }" generated')

    exit(0) # normally exit code
def mainfunc_getALLinfo(inputFILEname:str,outFILEname:str):
    #inputFILEname = "higgsCombineTest.MultiDimFit.mH120.root"
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valS = snapshot.find('nSIGN')
    valF = snapshot.find('nFAKE')
    valL = snapshot.find('nL')
    valC = snapshot.find('nC')
    valB = snapshot.find('nB')
    totVal = valL.getVal() + valC.getVal() + valB.getVal()


    def extract_info(v, totalVALUE:float):
        return {
                'value': v.getVal(),
                'error': v.getError(),
                #'errHi': v.getErrorHi(),
                #'errLo': v.getErrorLo(),
                'composition': v.getVal() / totalVALUE,
        }
    output = {
            'nL': extract_info(valL, totVal),
            'nC': extract_info(valC, totVal),
            'nB': extract_info(valB, totVal),
            'nFAKE': { 'value': valF.getVal(), 'error': valF.getError() },
    }
    
    import yaml
    info(f'[GenerateYAML] file "{ outFILEname }"')
    with open(outFILEname, 'w') as f_out:
        yaml.dump(output, f_out, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outFILEname }" generated')

    exit(0) # normally exit code
def mainfunc_getLCBinfo(inputFILEname:str,outFILEname:str):
    #inputFILEname = "higgsCombineTest.MultiDimFit.mH120.root"
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valL = snapshot.find('nL')
    valC = snapshot.find('nC')
    valB = snapshot.find('nB')
    totVal = valL.getVal() + valC.getVal() + valB.getVal()


    def extract_info(v, totalVALUE:float):
        return {
                'value': v.getVal(),
                'error': v.getError(),
                #'errHi': v.getErrorHi(),
                #'errLo': v.getErrorLo(),
                'composition': v.getVal() / totalVALUE,
        }
    output = {
            'nL': extract_info(valL, totVal),
            'nC': extract_info(valC, totVal),
            'nB': extract_info(valB, totVal),
    }
    
    import yaml
    info(f'[GenerateYAML] file "{ outFILEname }"')
    with open(outFILEname, 'w') as f_out:
        yaml.dump(output, f_out, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outFILEname }" generated')

    exit(0) # normally exit code


    

def testfunc():
    inputFILEname = "higgsCombineTest.MultiDimFit.mH120.root"
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valL = GetFitValueFromMultiDimFit(snapshot,'nL')
    valC = GetFitValueFromMultiDimFit(snapshot,'nC')
    valB = GetFitValueFromMultiDimFit(snapshot,'nB')
    print(valL.getVal(), valC.getVal(), valB.getVal())
    exit()

if __name__ == "__main__":
    import sys
    inARGs = namedtuple('inARGs', 'mode in_root out_yaml')
    args = inARGs(*sys.argv[1:])

    if args.mode == 'LCBinfo':
        mainfunc_getLCBinfo(args.in_root, args.out_yaml)
    if args.mode == 'Allinfo':
        mainfunc_getALLinfo(args.in_root, args.out_yaml)
    if args.mode == 'inclusiveinfo':
        mainfunc_getGJetinfo(args.in_root, args.out_yaml)

    if args.mode == 'test':
        testfunc()

    raise IOError(f'[InvalidMODE] Input mode "{ args.mode }" is invalid, the accepted mode is "test", "LCBinfo" and "Allinfo"\n\n')
