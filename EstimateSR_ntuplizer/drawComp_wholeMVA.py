import ROOT
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec

# Load the ROOT files
data_file = ROOT.TFile.Open("data_signalregion.root")
signal_file = ROOT.TFile.Open("gjetMadgraph.root")
qcd_file = ROOT.TFile.Open("QCDMadgraph.root")

# Get the histograms
data_hist = data_file.Get("MyMVA")
signal_hist = signal_file.Get("MyMVA")
qcd_hist = qcd_file.Get("MyMVA")

# Convert ROOT histograms to numpy arrays for plotting
def hist_to_array_normal_content(hist):
    nbins = hist.GetNbinsX()
    x = np.array([hist.GetBinCenter(i+1) for i in range(nbins)])
    y = np.array([hist.GetBinContent(i+1) for i in range(nbins)])
    y_err = np.array([hist.GetBinError(i+1) for i in range(nbins)])
    return x, y, y_err
def hist_to_array_with_overflowbin(hist):
    x,y,y_err = hist_to_array_normal_content(hist)
    x_bin_0 = x[0] - 2.*(x[1]-x[0])
    x_bin_0_int = x[0] - 1.*(x[1]-x[0])
    y_bin_0 = hist.GetBinContent(0)
    yerr_bin_0 = hist.GetBinError(0)

    x_bin_f = x[-1] + 2.*(x[-1]-x[-2])
    x_bin_f_int = x[-1] + 1.*(x[-1]-x[-2])
    y_bin_f = hist.GetBinContent( hist.GetNbinsX()+1 )
    yerr_bin_f = hist.GetBinError( hist.GetNbinsX()+1 )

    new_x = np.concatenate((np.array([x_bin_0,x_bin_0_int]),x,np.array([x_bin_f_int,x_bin_f])))
    new_y = np.concatenate((np.array([y_bin_0,0.]),y,np.array([0.,y_bin_f])))
    new_yerr = np.concatenate((np.array([yerr_bin_0,0.]),y_err,np.array([0.,yerr_bin_f])))
    print(f'got new y0, yf = {y_bin_0} and {y_bin_f}')
    #print(f'origx = {x}')
    #print(f'new_x = {new_x}')
    #print(f'x_bin_0 = {x_bin_0} and x_bin_f = {x_bin_f}')
    return new_x, new_y, new_yerr
def hist_to_array(hist):
    return hist_to_array_with_overflowbin(hist)
    #return hist_to_array_normal_content(hist)



# Get arrays from histograms
x_data, y_data, yerr_data = hist_to_array(data_hist)
x_signal, y_signal, yerr_signal = hist_to_array(signal_hist)
x_qcd, y_qcd, yerr_qcd = hist_to_array(qcd_hist)

# Stack signal and QCD samples
y_stack = y_signal + y_qcd
y_stack *= 26.6169 # luminosity
yerr_stack = np.sqrt(yerr_signal**2 + yerr_qcd**2)


# Calculate ratio: data / (signal + QCD)
ratio = np.divide(y_data, y_stack, out=np.zeros_like(y_data), where=y_stack!=0)
ratio_err = np.divide(yerr_data, y_stack, out=np.zeros_like(yerr_data), where=y_stack!=0)

# Create figure and gridspec
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])  # 3:1 height ratio

# Upper plot: Data vs. Signal + QCD stack
ax0 = plt.subplot(gs[0])
print(x_data)
ax0.errorbar(x_data, y_data, yerr=yerr_data, fmt='o', label='Run2022EFG', color='black')
ax0.bar(x_signal, y_stack, width=x_signal[1] - x_signal[0], align='center', label='gjet Madgraph + QCD', color='orange', alpha=0.7)
ax0.bar(x_signal, y_qcd  , width=x_signal[1] - x_signal[0], align='center', label='QCD', color='gray', alpha=0.7)
#ax0.set_yscale('log')
ax0.set_ylabel("Events")
ax0.set_title("Photon BDTG score: data and MC comparison")
ax0.legend()

# Lower plot: Ratio (Data / Stack)
ax1 = plt.subplot(gs[1], sharex=ax0)
ax1.errorbar(x_data, ratio, yerr=ratio_err, fmt='o', color='black')
ax1.axhline(1, color='red', linestyle='--')  # Reference line at ratio = 1
ax1.set_xlabel("BDTG score")
ax1.set_ylabel("Data / (Signal+QCD)")
ax1.set_ylim(0.5, 4.5)  # Adjust this range as needed for your ratio

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig("hCOMP_wholeMVA.pdf")
plt.show()

# Close the ROOT files
data_file.Close()
signal_file.Close()
qcd_file.Close()
