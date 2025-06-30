#!/usr/bin/env python3

import ROOT

def GetSmallTree(inTREE, nEVT=10):
    sampletree = inTREE.CloneTree(nEVT)
    #print(sampletree.GetEntries())
    sampletree.SetDirectory(0)

    return sampletree

