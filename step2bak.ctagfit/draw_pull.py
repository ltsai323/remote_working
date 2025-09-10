#!/usr/bin/env python3
### python3 aa.py higgsCombine4thSimulFit.MultiDimFit.mH120.123456.root limit NC
import sys
import ROOT
import yaml


def main( inFILE, theVAR, fitYAML ):
    ifile = ROOT.TFile.Open(inFILE)
    tree = ifile.Get('limit')
    expr = theVAR
    with open(fitYAML, 'r') as fIN:
        fit_result = yaml.safe_load(fIN)

        nTRUTH = float(fit_result[theVAR]['value'])
        nERROR = float(fit_result[theVAR]['error'])

    ROOT.gROOT.SetBatch(True)         # 不開視窗
    ROOT.gStyle.SetOptStat(0)         # 關閉預設統計框
    ROOT.gStyle.SetOptFit(0)          # 我們自畫 fit 文字（不使用預設 fit box）

    c1 = ROOT.TCanvas("c1", "Gaussian Fit", 900, 700)
    c1.SetMargin(0.10, 0.05, 0.12, 0.06)

    # 產生臨時 hist：如同 C++ 的 limit->Draw("NC")
    # 若你想控制 binning，可改成 "NC>>h(60,min,max)"
    draw_opt = ""
    draw_spec = expr
    code = tree.Draw(f'({draw_spec} - {nTRUTH:.1f})/{nERROR:.1f}')
    if code and code <= 0:
        raise RuntimeError(f"Draw('{draw_spec}') returned {code}; check your expression or tree content.")

    # 取得 ROOT 自動建立的 htemp
    htemp = ROOT.gPad.GetPrimitive("htemp")
    if not htemp:
        raise RuntimeError("Cannot find 'htemp' on pad. Try specifying explicit histogram, e.g. 'NC>>h(60,min,max)'.")

    htemp.SetTitle(f";Pull ({expr}={nTRUTH:.1f}+-{nERROR:.1f});Entries")
    htemp.SetLineWidth(2)
    htemp.Draw("E")

    # 高斯擬合
    # 你也可以指定範圍，例如 TF1('gaus','gaus', xmin, xmax) 並用 htemp.Fit(f,'RQ')
    fitopts = "RQ"  # R=Fit range from function, Q=quiet
    #fitres = htemp.Fit("gaus", fitopts)
    fitres = htemp.Fit("gaus")
    gaus = htemp.GetFunction("gaus")
    if not gaus:
        raise RuntimeError("Gaussian fit failed or function not attached.")

    # 擬合後重畫（確保圖層）
    htemp.Draw("E")
    gaus.SetLineWidth(3)
    gaus.Draw("SAME")

    # 取出結果
    mean  = gaus.GetParameter(1)
    emean = gaus.GetParError(1)
    sigma = gaus.GetParameter(2)
    esig  = gaus.GetParError(2)
    chi2  = gaus.GetChisquare()
    ndf   = gaus.GetNDF()
    prob  = ROOT.TMath.Prob(chi2, int(ndf)) if ndf > 0 else 0.0
    entries = int(htemp.GetEntries())

    # 在畫布上放一個 TPaveText 顯示擬合結果（NDC 座標）
    pave = ROOT.TPaveText(0.62, 0.62, 0.88, 0.88, "NDC")
    pave.SetFillColor(0)
    pave.SetTextFont(42)
    pave.SetTextSize(0.03)
    pave.SetBorderSize(1)
    pave.AddText("Gaussian fit")
    pave.AddText(f"Mean = {mean:.4g} #pm {emean:.2g}")
    pave.AddText(f"#sigma = {sigma:.4g} #pm {esig:.2g}")
    pave.AddText(f"#chi^2/ndf = {chi2:.2f} / {ndf}")
    pave.AddText(f"Prob = {prob:.3g}")
    pave.AddText(f"Entries = {entries}")
    pave.Draw()

    c1.Update()
    c1.SaveAs(f"hPull_{expr}.pdf")


if __name__ == "__main__":
    inFILE = sys.argv[1] # higgsCombine4thSimulFit.MultiDimFit.mH120.123456.root
    theVAR = sys.argv[2] # NC
    fitYAML = sys.argv[3] # scan2D_4th.yaml
    main(inFILE, theVAR, fitYAML)
