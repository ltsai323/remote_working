import ROOT
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

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
y_stack *= 26.6169 # luminosity
yerr_stack = np.sqrt(yerr_signal**2 + yerr_qcd**2)
yerr_stack *= 26.6169

# Calculate ratio: data / (signal + QCD)
ratio = np.divide(y_data, y_stack, out=np.zeros_like(y_data), where=y_stack!=0)
ratio_err = np.divide(yerr_data, y_stack, out=np.zeros_like(yerr_data), where=y_stack!=0)

# Create figure and gridspec
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])  # 3:1 height ratio

# Upper plot: Data vs. Signal + QCD stack
ax0 = plt.subplot(gs[0])
ax0.errorbar(x_data, y_data, yerr=yerr_data, fmt='o', label='Run2022EFG', color='black')
ax0.bar(x_signal, y_stack, width=x_signal[1] - x_signal[0], align='center', label='gjet Madgraph + QCD', color='orange', alpha=0.7)
ax0.bar(x_signal, y_qcd  , width=x_signal[1] - x_signal[0], align='center', label='QCD', color='gray', alpha=0.7)
ax0.set_yscale('log')
ax0.set_ylabel("Events")
ax0.set_title("Photon pt distribution: Data vs Signal+QCD")
ax0.legend()

# Lower plot: Ratio (Data / Stack)
ax1 = plt.subplot(gs[1], sharex=ax0)
ax1.errorbar(x_data, ratio, yerr=ratio_err, fmt='o', color='black')
ax1.axhline(1, color='red', linestyle='--')  # Reference line at ratio = 1
ax1.set_xlabel("Photon pt [GeV]")
ax1.set_ylabel("Data / (Signal+QCD)")
ax1.set_ylim(0.5, 1.5)  # Adjust this range as needed for your ratio


class LoadHistFromTFile:
    def __init__(self, fNAME, hNAME):
        self.f = ROOT.TFile.Open(fNAME)
        self.h = self.f.Get(hNAME)

def __del__(self):
        self.f.Close()

if __name__ == "__main__":
    load_data = LoadHistFromTFile("data_signalregion.root",'Pho_pt')
    load_sign = LoadHistFromTFile("gjetMadgraph.root"     ,'Pho_pt')
    load_qcd  = LoadHistFromTFile("QCDMadgraph.root"      ,'Pho_pt')
    # Get arrays from histograms
    x_data, y_data, yerr_data       = hist_to_array(load_data.h)
    x_signal, y_signal, yerr_signal = hist_to_array(load_sign.h)
    x_qcd, y_qcd, yerr_qcd          = hist_to_array(load_qcd .h)



    # Adjust layout
    plt.tight_layout()

    # Save the plot
    outfilename = 'hCOMP_wholePhottonPT.pdf'
    plt.savefig(outfilename)
    print(f"[OutFig] {outfilename}")
    plt.show()

