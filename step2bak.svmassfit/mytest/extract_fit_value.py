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
def mainfunc_getLCBKfactor(inputFILEname:str,outFILEname:str):
    #inputFILEname = "higgsCombineTest.MultiDimFit.mH120.root"
    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valL = snapshot.find('rL')
    valC = snapshot.find('rC')
    valB = snapshot.find('rB')


    def extract_info(v):
        return {
                'value': v.getVal(),
                'error': v.getError(),
        }
    output = {
            'rL': extract_info(valL),
            'rC': extract_info(valC),
            'rB': extract_info(valB),
    }

    import yaml
    info(f'[GenerateYAML] file "{ outFILEname }"')
    with open(outFILEname, 'w') as f_out:
        yaml.dump(output, f_out, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outFILEname }" generated')

    exit(0) # normally exit code
def mainfunc_getinfo(inputFILEname:str,outFILEname:str, loadedVARs:list):

    inFILE = ROOT.TFile.Open(inputFILEname)
    ws = inFILE.Get('w')
    snapshot = GetSnapshotAtMultiDimFit(ws)

    valL = snapshot.find('rL')
    valC = snapshot.find('rC')
    valB = snapshot.find('rB')


    output = {}
    for loadedVAR in loadedVARs:
        v = snapshot.find(loadedVAR)
        output[loadedVAR] = {
                'value': v.getVal(),
                'error': v.getError(),
                'errUp': v.getErrorHi(),
                'errDn': v.getErrorLo(),
                }


    import yaml
    info(f'[GenerateYAML] file "{ outFILEname }"')
    with open(outFILEname, 'w') as f_out:
        yaml.dump(output, f_out, default_flow_style=False)
        info(f'[GenerateYAML] file "{ outFILEname }" generated')





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
    '''
    args: 1.inROOT 2.outYAML 3~N: variables recorded into yaml file and read from root file
    '''
    import sys
    in_root = sys.argv[1]
    out_yaml = sys.argv[2]
    load_vars = sys.argv[3:]

    if len(load_vars) == 0: raise IOError(f'[NoVarialbes] abort')

    mainfunc_getinfo(in_root,out_yaml, load_vars)

    #raise IOError(f'[InvalidMODE] Input mode "{ args.mode }" is invalid, the accepted mode is "test", "LCBinfo" and "Allinfo"\n\n')
