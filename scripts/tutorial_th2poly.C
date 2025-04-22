//---------------------------------------------------------------------------------------------------- 
// This tutorial code deomonstrate the usage of a TH2Poly object.
//---------------------------------------------------------------------------------------------------- 
void tutorial_th2poly(){
    TString fname = "./output/geometry/ML_F_wafer_geometry.root";
    TString figure = "./output/waferMaps/tutorial.png";

    TCanvas *c1 = new TCanvas("c1", "", 900, 900);
    c1->SetRightMargin(0.15);

    TH2Poly *p = new TH2Poly("hexagonal histograms", "", -14, 14, -14, 14);
    p->SetStats(0); // remove stat pad
    p->SetMarkerSize(0.7); // adjust text size on the bins
    p->GetXaxis()->SetTitle("x (cm)");
    p->GetYaxis()->SetTitle("y (cm)");
    p->GetYaxis()->SetTitleOffset(1.1);

    // load a geometry root file
    TFile *f = TFile::Open(fname,"R");

    // retrieves a TList of all keys in the current directory
    TGraph *gr;
    TKey *key;
    TIter nextkey(gDirectory->GetListOfKeys());

    // register polygonal bins 
    while ((key = (TKey*)nextkey())) {
        TObject *obj = key->ReadObj();
        if(obj->InheritsFrom("TGraph")) {
            gr = (TGraph*) obj;
            p->AddBin(gr);
        }
    }

    // fill values
    int nBins = p->GetNcells()-9;
    for(int i=0; i<nBins; ++i) {
        p->SetBinContent(i+1, (float)i);
    }

    // create a plot
    p->Draw("colz;text");
    gStyle->SetPaintTextFormat(".0f");
    c1->SaveAs(figure);
    f->Close();
}
