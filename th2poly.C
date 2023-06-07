void th2poly(TString inputfile, TString outputfile, double range, bool drawLine=false){
    TCanvas *c1 = new TCanvas("c1", "", 1200, 900);
	c1->SetRightMargin(0.15);

    TFile *f = TFile::Open(inputfile,"R");

    TH2Poly *p = new TH2Poly("hexagonal histograms", "hexagonal histograms", -1*range, range, -1*range, range);
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

	//-----------------------------------------------------------------
	// p->GetNcells() are not consistent with counter (likely nCells-9)
	//-----------------------------------------------------------------
	// printf("[INFO] nCells  = %d\n", p->GetNcells());
	// printf("[INFO] counter = %d\n", counter);
	//-----------------------------------------------------------------

    p->Draw("colz;text");

	if(drawLine) {
		TLine line;
		line.SetLineStyle(2);
		line.SetLineWidth(2);
		line.DrawLine(0, 1, 14.7, 23.5);
		line.DrawLine(0, 1, 12.2, -23);
		line.DrawLine(0, 1, -27, 1);
	}

    c1->SaveAs(outputfile);
}

