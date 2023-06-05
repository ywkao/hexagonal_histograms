{
    TCanvas *c1 = new TCanvas("c1", "", 1200, 900);
    c1->SetGridx();
    c1->SetGridy();
	c1->SetRightMargin(0.15);

    TFile *f = TFile::Open("./data/hexagons.root","R");

    TH2Poly *p = new TH2Poly("hexagonal histograms", "hexagonal histograms", -30, 30, -30, 30);
    p->SetStats(0);
    p->GetXaxis()->SetTitle("x (arb. unit)");
    p->GetYaxis()->SetTitle("y (arb. unit)");
    p->GetZaxis()->SetTitle("Ordinal numbers");

	int counter = 0;

    TGraph *gr;
    TKey *key;
    TIter nextkey(gDirectory->GetListOfKeys());
    while ((key = (TKey*)nextkey())) {
        TObject *obj = key->ReadObj();
        if(obj->InheritsFrom("TGraph")) {
            gr = (TGraph*) obj;
            p->AddBin(gr);
			counter+=1;
        }
    }

    TRandom r;
    p->ChangePartition(100, 100);

    for(int i=0; i<counter; ++i) {
        p->SetBinContent(i+1, i+1);
    }

	//--------------------------------------------------
	// p->GetNcells() are not consistent with counter
	//--------------------------------------------------
	// printf("[INFO] nCells  = %d\n", p->GetNcells());
	// printf("[INFO] counter = %d\n", counter);
	//--------------------------------------------------
    // fill th2poly
	//--------------------------------------------------
    // const int npoints = 10000;
    // for(int i=0; i<npoints; ++i) {
    //     double x = r.Uniform(-200, 200);
    //     double y = r.Uniform(-200, 0);
    //     p->Fill(x,y);
    // }
	//--------------------------------------------------

    p->Draw("colz;text");
    c1->SaveAs("output.png");
}

