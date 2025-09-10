import ROOT
import numpy as np
import matplotlib.pyplot as plt

# Open the ROOT file
file = ROOT.TFile.Open("dRcheck_jet_to_muon.root")

# Retrieve the histograms
hist_sig = file.Get("mu1SIG")
hist_bkg = file.Get("mu1BKG")

# Convert histograms to numpy arrays
nbins = hist_sig.GetNbinsX()
x_vals = np.array([hist_sig.GetBinCenter(i) for i in range(1, nbins + 1)])
y_sig = np.array([hist_sig.GetBinContent(i) for i in range(1, nbins + 1)])
y_bkg = np.array([hist_bkg.GetBinContent(i) for i in range(1, nbins + 1)])

# Plot histograms
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_sig, color='red', linestyle='-', label="mu1SIG")
plt.plot(x_vals, y_bkg, color='blue', linestyle='-', label="mu1BKG")

# Labels and title
plt.xlabel("$\Delta$ R(jet, $\mu$)")
plt.ylabel("Normalized probabilities")
plt.title("$\Delta$R of jet and muon if NanoAOD recording index")
plt.legend()
plt.grid()
plt.yscale('log')

# Show the plot
plt.savefig("dRplot.mu1andjet.pdf")

# Close the ROOT file
file.Close()
