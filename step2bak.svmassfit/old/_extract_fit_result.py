#!/usr/bin/enb python3
import ROOT

class FitVar:
    def __init__(self,var):
        self.val = var.getVal()
        self.err = var.getError()
        self.errUp = var.getErrorHi()
        self.errDn = var.getErrorLo()
    def __str__(self):
        return f'val = {self.val}+-{self.err}. And errUp {self.errUp} / errDn {self.errDn}'

def GetFitResult(inFILE:str) -> dict:
    #inFILE = 'multidimfitTest.root'

    infile = ROOT.TFile.Open(inFILE)
    fitres = infile.Get('fit_mdf')
    var_dict = { v.GetName():v for v in  fitres.floatParsFinal() }
    infile.Close()

    return { name:FitVar(var) for name,var in var_dict.items() }
def ShowFitResult(inFILE:str) -> None:
    fitres = GetFitResult(inFILE)
    for n,fitr in fitres.items():
        print(n,fitr)

def test_func():
    ShowFitResult('multidimfitTest.root')
    fitres = GetFitResult('multidimfitTest.root')
    exit()

if __name__ == "__main__":
    test_func()
