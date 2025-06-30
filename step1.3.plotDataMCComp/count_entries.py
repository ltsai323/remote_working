#!/usr/bin/env python3

import ROOT

def CountEntries( filepathFORchain ):
    chain = ROOT.TChain('ggNtuplizer/EventTree')
    chain.Add(filepathFORchain)

    return chain.GetEntries()

def countEntries_single(file) -> int:
    tfile = ROOT.TFile.Open(file)
    try:
        ttree = tfile.Get('ggNtuplizer/EventTree')
        out = ttree.GetEntries()
        return out
    except ReferenceError as e:
        print('[Input File Got Error] {file}. Ignore this file...')
        print(e)
    finally:
        tfile.Close()
def CountEntries_tree( filepathFORchain ):
    import subprocess
    res = subprocess.run(f'ls {filepathFORchain}', capture_output=True, text=True, shell=True)
    return sum(countEntries_single(r) for r in res.stdout.split('\n') if r )

def FilledEntries(rootFILE):
    tfile = ROOT.TFile.Open(rootFILE)
    ttree = tfile.Get('t')

    entries = -99
    for event in ttree:
        entries = event.integratedGenWeight
        break
    tfile.Close()
    return entries

def GotEntriesFromFile(pathFILE, resultROOT):
    sum_entries = 0
    with open(pathFILE,'r') as fIN:
        for line in fIN.readlines():
            sum_entries += countEntries_single(line.strip())

    filled_entries = FilledEntries(resultROOT)
    print(f'[File] {pathFILE}')
    print(f'[result]   Total Entries {sum_entries:20d} - Filled Entries {filled_entries:20.0f} = {sum_entries-filled_entries}')
    print('')
if __name__ == "__main__":
    #entries = CountEntries(input_files)

    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_GJetPythia/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/GJet_Pt-20to40_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_GJetPythia/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/GJet_Pt-20toInf_DoubleEMEnriched_MGG-40to80_TuneCP5_13TeV_Pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_GJetPythia/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCP5_13TeV_Pythia8.root')

    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT50to100_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')
    GotEntriesFromFile('/home/ltsai/ReceivedFile/GJet/listedPaths/UL16Post_QCDMadgraph/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.txt',
'/home/ltsai/ReceivedFile/GJet/latestsample/UL2016PostVFP/step3.btagSFappended/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraphMLM-pythia8.root')









