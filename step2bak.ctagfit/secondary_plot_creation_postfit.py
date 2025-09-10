import ROOT
import os

def TakeRatio(outHISTname, hUPPER, hLOWER):
    hU = hUPPER
    hL = hLOWER
    for ibin in range(1,hL.GetNbinsX()+2):
        if hL.GetBinContent(ibin) == 0: hL.SetBinContent(ibin, 1e-8)
    ratio = ROOT.TGraphAsymmErrors()
    ratio.SetName(outHISTname)
    ratio.Divide(hU,hL, 'pois')
    return ratio

def save_histograms_from_folder(input_file_name):
    # Open the input ROOT file
    input_file = ROOT.TFile.Open(input_file_name, "READ")
    if not input_file or input_file.IsZombie():
        print(f"Error: Cannot open file {input_file_name}")
        return

    # List of keys in the ROOT file
    keys = input_file.GetListOfKeys()

    # Loop over all keys (folders and objects) in the ROOT file
    for key in keys:
        obj = key.ReadObj()

        # Check if the object is a directory (folder)
        if isinstance(obj, ROOT.TDirectory):
            folder_name = obj.GetName()
            #output_file_name = f"postfit.{folder_name}.root"
            output_file_name = input_file_name.replace(".root", f".{folder_name}.root")

            # Create a new ROOT file for the current folder's histograms
            output_file = ROOT.TFile.Open(output_file_name, "RECREATE")

            data_mc_ratio = TakeRatio( 'ratio',
                    obj.Get('data_obs'),
                    obj.Get('TotalProcs')
                    )
            data_mc_ratio.Write()


            # Loop over all keys in the current folder
            for hist_key in obj.GetListOfKeys():
                hist = hist_key.ReadObj()
                if isinstance(hist, ROOT.TH1):  # Check if it's a histogram
                    hist.Write()  # Write the histogram to the output file

            output_file.Close()
            print(f"Saved histograms from folder '{folder_name}' into '{output_file_name}'")

    # Close the input file
    input_file.Close()

# Main execution
if __name__ == "__main__":
    import sys
    #input_root_file = "postfit.root"  # Specify the input file name
    input_root_file = sys.argv[1]
    save_histograms_from_folder(input_root_file)
