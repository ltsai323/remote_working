import ROOT
from scipy.interpolate import griddata
import numpy as np

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

import sys
try:
    outFILEname = sys.argv[1]
    file_name = sys.argv[2]
    xVARdef = sys.argv[3]
    yVARdef = sys.argv[4]

    varX = xVARdef.split('=')[0]
    varXrange = [ float(v) for v in xVARdef.split('=')[1].split(',') ]
    varY = yVARdef.split('=')[0]
    varYrange = [ float(v) for v in yVARdef.split('=')[1].split(',') ]
except Exception as e:
    raise IOError(f'\n\n[ExampleUsage] python3 this.py hNLL2Dscan.pdf higgsCombine.scan2D.MultiDimFit.mH120.root numC=100,300 numB=200,400') from e

#file_name = "higgsCombine.scan2D.MultiDimFit.mH120.root"
f = ROOT.TFile(file_name)
t = f.Get("limit")

# Number of points in interpolation
n_points = 1000
#x_range = [150,300]
#y_range = [50,150]
x_range = varXrange
y_range = varYrange

# Number of bins in plot
n_bins = 40

x, y, deltaNLL = [], [], []
for ev in t:
    x.append(getattr(ev, varX))
    y.append(getattr(ev, varY))
    deltaNLL.append(getattr(ev, "deltaNLL"))

min_NLL = min(deltaNLL)
print(f'[MinNLL] got {min_NLL} smaller than 0?')
has_negtive_NLL = min_NLL < 0

if has_negtive_NLL:
    print('[NoBestFit] got Negative NLL')
    bestX = min([ (_d,_x) for _x,_d in zip(x,deltaNLL) ])[1] # find X with minimized deltaNLL
    XrangeL = min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x <= bestX and _d > 1.0+min_NLL ])[1] # minus 1 sigma
    XrangeR = min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x >= bestX and _d > 1.0+min_NLL ])[1] # plus  1 sigma
    print( min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x <  bestX and _d > 1.0+min_NLL ]) )
    print( min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x >  bestX and _d > 1.0+min_NLL ]) )

    bestY = min([ (_d,_y) for _y,_d in zip(y,deltaNLL) ])[1] # find X with minimized deltaNLL
    YrangeL = min([ (_d,_y) for _y,_d in zip(y,deltaNLL) if _y <= bestY and _d > 1.0+min_NLL ])[1]
    YrangeR = min([ (_d,_y) for _y,_d in zip(y,deltaNLL) if _y >= bestY and _d > 1.0+min_NLL ])[1]
else:
    print('[GotBestFit] got minimize NLL=0')
    bestX = x[0]
    try:
        XrangeL = min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x <= bestX and _d > 1.0 ])[1] # minus 1 sigma
        XrangeR = min([ (_d,_x) for _x,_d in zip(x,deltaNLL) if _x >= bestX and _d > 1.0 ])[1] # plus  1 sigma
    except ValueError as e:
        print('[UnableToFindRange] used bestX*0.1 and bestX*3.0')
        XrangeL = bestX * 0.1
        XrangeR = bestX * 3.0
    bestY = y[0]
    try:
        YrangeL = min([ (_d,_y) for _y,_d in zip(y,deltaNLL) if _y <= bestY and _d > 1.0 ])[1]
        YrangeR = min([ (_d,_y) for _y,_d in zip(y,deltaNLL) if _y >= bestY and _d > 1.0 ])[1]
    except ValueError as e:
        print('[UnableToFindRange] used bestY*0.1 and bestY*3.0')
        YrangeL = bestY * 0.1
        YrangeR = bestY * 3.0
XuncL = bestX - XrangeL
XuncR = XrangeR - bestX
YuncL = bestY - YrangeL
YuncR = YrangeR - bestY
print(varX, XrangeL, XrangeR)
print(varY, YrangeL, YrangeR)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Do interpolation
# Convert to numpy arrays as required for interpolation
dnll = np.asarray(deltaNLL)
points = np.array([x, y]).transpose()
# Set up grid
grid_x, grid_y = np.mgrid[x_range[0] : x_range[1] : n_points * 1j, y_range[0] : y_range[1] : n_points * 1j]
grid_vals = griddata(points, dnll, (grid_x, grid_y), "cubic")

# Remove NANS
grid_x = grid_x[grid_vals == grid_vals]
grid_y = grid_y[grid_vals == grid_vals]
grid_vals = grid_vals[grid_vals == grid_vals]
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Define Profile2D histogram
h2D = ROOT.TProfile2D("h", "h", n_bins, x_range[0], x_range[1], n_bins, y_range[0], y_range[1])

for i in range(len(grid_vals)):
    # Factor of 2 comes from 2*NLL
    h2D.Fill(grid_x[i], grid_y[i], 2 * grid_vals[i])

# Loop over bins: if content = 0 then set 999
for ibin in range(1, h2D.GetNbinsX() + 1):
    for jbin in range(1, h2D.GetNbinsY() + 1):
        if h2D.GetBinContent(ibin, jbin) == 0:
            xc = h2D.GetXaxis().GetBinCenter(ibin)
            yc = h2D.GetYaxis().GetBinCenter(jbin)
            h2D.Fill(xc, yc, 999)

# Set up canvas
canv = ROOT.TCanvas("canv", "canv", 600, 600)
canv.SetTickx()
canv.SetTicky()
canv.SetLeftMargin(0.115)
canv.SetBottomMargin(0.115)
# Extract binwidth
xw = (x_range[1] - x_range[0]) / n_bins
yw = (y_range[1] - y_range[0]) / n_bins

# Set histogram properties
h2D.SetContour(999)
h2D.SetTitle("")
h2D.GetXaxis().SetTitle(f'{varX} = {bestX:.1f} {{}}^{{+{XuncR:.1f}}}_{{-{XuncL:.1f}}}')
h2D.GetXaxis().SetTitleSize(0.05)
h2D.GetXaxis().SetTitleOffset(0.9)
h2D.GetXaxis().SetRangeUser(x_range[0], x_range[1] - xw)

h2D.GetYaxis().SetTitle(f'{varY} = {bestY:.1f} {{}}^{{+{YuncR:.1f}}}_{{-{YuncL:.1f}}}')
h2D.GetYaxis().SetTitleSize(0.05)
h2D.GetYaxis().SetTitleOffset(0.9)
h2D.GetYaxis().SetRangeUser(y_range[0], y_range[1] - yw)

h2D.GetZaxis().SetTitle("-2 #Delta ln L")
h2D.GetZaxis().SetTitleSize(0.05)
h2D.GetZaxis().SetTitleOffset(0.8)

h2D.SetMaximum(25)

# Make confidence interval contours
c68, c95 = h2D.Clone(), h2D.Clone()
c68.SetContour(2)
c68.SetContourLevel(1, 2.3)
c68.SetLineWidth(3)
c68.SetLineColor(ROOT.kBlack)
c95.SetContour(2)
c95.SetContourLevel(1, 5.99)
c95.SetLineWidth(3)
c95.SetLineStyle(2)
c95.SetLineColor(ROOT.kBlack)

# Draw histogram and contours
h2D.Draw("COLZ")

# Draw lines for SM point
vline = ROOT.TLine(1, y_range[0], 1, y_range[1] - yw)
vline.SetLineColorAlpha(ROOT.kGray, 0.5)
vline.Draw("Same")
hline = ROOT.TLine(x_range[0], 1, x_range[1] - xw, 1)
hline.SetLineColorAlpha(ROOT.kGray, 0.5)
hline.Draw("Same")

# Draw contours
c68.Draw("cont3same")
c95.Draw("cont3same")

# Make best fit and sm points
gBF = ROOT.TGraph()
gBF.SetPoint(0, grid_x[np.argmin(grid_vals)], grid_y[np.argmin(grid_vals)])
gBF.SetMarkerStyle(34)
gBF.SetMarkerSize(2)
gBF.SetMarkerColor(ROOT.kBlack)
gBF.Draw("P")



# Add legend
leg = ROOT.TLegend(0.6, 0.67, 0.8, 0.87)
#leg.SetHeader(f'{varX}({bestX:.1f}) {varY}({bestY:.1f})', 'C')
leg.SetBorderSize(0)
leg.SetFillColor(0)
leg.AddEntry(gBF, "Best fit", "P")
leg.AddEntry(c68, "1#sigma CL", "L")
leg.AddEntry(c95, "2#sigma CL", "L")
leg.Draw()

canv.Update()
canv.SaveAs(outFILEname)


if '.pdf' in outFILEname or '.png' in outFILEname:
    out_file_name = outFILEname.replace('.pdf', '') if '.pdf' in outFILEname else outFILEname.replace('.png', '')
    import yaml
    out_yaml_name = f'{out_file_name}.yaml'
    with open(out_yaml_name, 'w') as fOUT:
        dump_dict = {
                varX: { 'value': bestX, 'error': (XuncL+XuncR)/2., 'errUp': XuncR, 'errDn': XuncL },
                varY: { 'value': bestY, 'error': (YuncL+YuncR)/2., 'errUp': YuncR, 'errDn': YuncL },
                }
        yaml.dump( dump_dict, fOUT )
    print(f'[YamlExport] {out_yaml_name} generated')
    out_bash_name = f'{out_file_name}.sh'
    with open(out_bash_name, 'w') as fOUT:
        fOUT.write(f'{varX}_value={bestX:.2f}\n{varX}_error={(XuncL+XuncR)/2.:.2f}\n{varY}_value={bestY:.2f}\n{varY}_error={(YuncL+YuncR)/2.:.2f}\n')
    print(f'[BashExport] {out_bash_name} generated')


