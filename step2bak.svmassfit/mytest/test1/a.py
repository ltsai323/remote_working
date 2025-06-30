#!/usr/bin/env python3

import ROOT

def gettree(tNAME, recFILE):
    tree = ROOT.TTree(tNAME, '')
    tree.ReadFile(recFILE)
    return tree

tfit = gettree('tfit', 'record_fit.txt')
truth = gettree('truth', 'record_truth.txt')

canv = ROOT.TCanvas('c','',800,800)
graph_fit = ROOT.TGraph()

tfit.Draw("l:pt", "eta==0", "AP")
tfit.Show(3)

gfit=ROOT.gPad.GetPrimitive("Graph")

gfit.SetMarkerSize(5)
gfit.Draw()
canv.SaveAs("hi.png")
