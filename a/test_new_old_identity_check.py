#!/usr/bin/env python3

import ROOT
def GetFileAndTree(fileNAME):
    f = ROOT.TFile.Open(fileNAME)
    t = f.Get("tree")
    return f,t


def ShowHistDetail(tag, oldval, newval):
    print(f'[{tag}] old {oldval} -- new {newval}')
def CompareFile(tNEW,tOLD, varNAME, theTAG):
    def GetHist(tIN, var, hist):
        tIN.Draw(f'{var}>>{hist}')
        return ROOT.gROOT.FindObject(hist)

    def GetHistFromFile(fIN, hist):
        return fIN.Get(hist)

    print(f'[{theTAG} TreeEntries] old {tOLD.GetEntries()} and new {tNEW.GetEntries()}')
    hNew = GetHist(tNEW, varNAME, f'hNew{theTAG}')
    hOld = GetHist(tOLD, varNAME, f'hOld{theTAG}')
    ShowHistDetail(f'{theTAG} - GetEntries', hOld.GetEntries(), hNew.GetEntries())

def CompareHistFromFile(fNEW,fOLD, histNAME, theTAG):
    hNew = fNEW.Get(histNAME)
    hOld = fOLD.Get(histNAME)

    ShowHistDetail(f'{theTAG} - GetEntries', hOld.GetEntries(), hNew.GetEntries())

if __name__ == "__main__":
    fnew_data, tnew_data = GetFileAndTree('mytesting_data.root')
    fnew_sign, tnew_sign = GetFileAndTree('mytesting_gjetpythia.root')
    fnew_fake, tnew_fake = GetFileAndTree('mytesting_qcdmadgraph.root')

    fold_data, told_data = GetFileAndTree('test_ref/mytesting_data.root')
    fold_sign, told_sign = GetFileAndTree('test_ref/mytesting_gjetpythia.root')
    fold_fake, told_fake = GetFileAndTree('test_ref/mytesting_qcdmadgraph.root')

    test = 1
    if test==1:
        CompareFile(tnew_data,told_data, "photon_pt",'data')
        CompareFile(tnew_sign,told_sign, "photon_pt",'sign')
        CompareFile(tnew_fake,told_fake, "photon_pt",'fake')

    if test == 2:
        CompareHistFromFile(fnew_data,fold_data, "b_Pho_pt",'HdataH')
        CompareHistFromFile(fnew_sign,fold_sign, "b_Pho_pt",'HsignH')
        CompareHistFromFile(fnew_fake,fold_fake, "b_Pho_pt",'HfakeH')

