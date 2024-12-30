#!/usr/bin/env python3

import ROOT

import sys


iFILE = ROOT.TFile.Open(sys.argv[1])

iTREE = iFILE.Get('tree')
canv = ROOT.TCanvas("c1", "", 800,600)
canv.SetLogy()
iTREE.Draw("jet_SVdr", "jet_SVdr > 0 && jet_SVdr < 1")
canv.SaveAs("hi.png")
iTREE.Draw("jet_SVdr")
canv.SaveAs("hi.all.png")

