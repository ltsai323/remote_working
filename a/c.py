import ROOT
import matplotlib.pyplot as plt
import numpy as np

# Load the ROOT files
data_file = ROOT.TFile.Open("data_signalregion.root")
signal_file = ROOT.TFile.Open("gjetMadgraph.root")
qcd_file = ROOT.TFile.Open("QCDMadgraph.root")

# Get the histograms
data_hist = data_file.Get("Pho_pt")
signal_hist = signal_file.Get("Pho_pt")
qcd_hist = qcd_file.Get("Pho_pt")

# Convert ROOT histograms to numpy arrays for plotting
def hist_to_array(hist):
    nbins = hist.GetNbinsX()
    x = np.array([hist.GetBinCenter(i+1) for i in range(nbins)])
    y = np.array([hist.GetBinContent(i+1) for i in range(nbins)])
    y_err = np.array([hist.GetBinError(i+1) for i in range(nbins)])
    return x, y, y_err

# Get arrays from histograms
x_data, y_data, yerr_data = hist_to_array(data_hist)
x_signal, y_signal, yerr_signal = hist_to_array(signal_hist)
x_qcd, y_qcd, yerr_qcd = hist_to_array(qcd_hist)

# Stack signal and QCD samples
y_stack = y_signal + y_qcd
#https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Run_3_Analysis
y_stack *= 26.6169 # luminosity
yerr_stack = np.sqrt(yerr_signal**2 + yerr_qcd**2)

# Plot the data and the stacked histogram
plt.errorbar(x_data, y_data, yerr=yerr_data, fmt='o', label='Data', color='black')
plt.bar(x_signal, y_stack, width=x_signal[1] - x_signal[0], align='center', label='Signal + QCD', color='orange', alpha=0.7)

# Add legend and labels
plt.legend()
plt.yscale('log')
plt.xlabel("Photon pt [GeV]")
plt.ylabel("Events")
plt.title("Photon pt distribution: Data vs Signal+QCD")

# Save the plot
plt.savefig("hi.png")
plt.show()

# Close the ROOT files
data_file.Close()
signal_file.Close()
qcd_file.Close()
