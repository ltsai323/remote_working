#!/usr/bin/env python3
import ROOT

def CheckEntries(inFILE, outTAG):
    iFILE = ROOT.TFile.Open(inFILE)
    iTREE = iFILE.Get('tree')
    print(f'[{outTAG}] got entries {iTREE.GetEntries()}')

if __name__ == "__main__":
    origData = 'mytesting_data.root'
    origSign = 'mytesting_gjetmadgraph.root'
    origFake = 'mytesting_qcdmadgraph.root'
    testData = 'testnew_my_modified_code/mytesting_data.root'
    testSign = 'testnew_my_modified_code/mytesting_gjetmadgraph.root'
    testFake = 'testnew_my_modified_code/mytesting_qcdmadgraph.root'

    CheckEntries(origData, 'orig data')
    CheckEntries(testData, 'test data')

    CheckEntries(origFake, 'orig QCD')
    CheckEntries(testFake, 'test QCD')
