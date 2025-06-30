void plot_fit_truth() {
    // Load tree from text file
    TTree *tfit = new TTree("tfit", "");
    tfit->ReadFile("record_fit.txt");

    TTree *truth = new TTree("truth", "");
    truth->ReadFile("record_truth.txt");

    // Create canvas
    TCanvas *canv = new TCanvas("c", "", 800, 800);

    // Draw graph from tfit where eta == 0
    tfit->Draw("l:pt", "eta==0", "AP");

    //// Access the drawn TGraph from current pad
    //TGraph *gfit = (TGraph*)gPad->GetPrimitive("Graph");
    //if (gfit) {
    //    gfit->SetMarkerStyle(20);
    //    gfit->SetMarkerSize(5);
    //    gfit->Draw();
    //}

}
