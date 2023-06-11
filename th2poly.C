void th2poly(TString inputfile, TString outputfile, double range, bool drawLine=false){
    TCanvas *c1 = new TCanvas("c1", "", 900, 900);
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

	p->SetMarkerSize(0.7);
    p->Draw("colz;text");

	// the individual cell boundary will not shown without "text" draw option...
	//p->SetLineColor(kBlack);
	//p->SetLineWidth(2);
    //p->Draw("colz");

	if(drawLine) {
		const int N = 16;
		double x1[N] = {15.516288, 12.846043, 12.846043, 10.969655, 10.969655, 9.093267, 9.093267, 7.216878, 7.216878, 5.340490, 5.340490, 3.464102, 3.464102, 1.587713, 1.587713, -0.288675};
		double y1[N] = {25.791667, 24.250000, 22.083333, 21.000000, 18.833333, 17.750000, 15.583333, 14.500000, 12.333333, 11.250000, 9.083333, 8.000000, 5.833333, 4.750000, 2.583333, 1.500000};
		double x2[N] = {-29.228357, -26.558112, -24.681724, -22.805336, -20.928947, -19.052559, -17.176171, -15.299782, -13.423394, -11.547005, -9.670617, -7.794229, -5.917840, -4.041452, -2.165064, -0.288675};
		double y2[N] = {3.041667, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000, 2.583333, 1.500000};
		double x3[N] = {-0.288675, -0.288675, 1.587713, 1.587713, 3.464102, 3.464102, 5.340490, 5.340490, 7.216878, 7.216878, 9.093267, 9.093267, 10.969655, 10.969655, 12.846043, 12.846043};
		double y3[N] = {1.500000, -0.666667, -1.750000, -3.916667, -5.000000, -7.166667, -8.250000, -10.416667, -11.500000, -13.666667, -14.750000, -16.916667, -18.000000, -20.166667, -21.250000, -24.333333};

		TLine line;
		line.SetLineStyle(1);
		line.SetLineColor(2);
		line.SetLineWidth(2);

		for(int i=0; i<N-1; ++i) {
			line.DrawLine(x1[i], y1[i], x1[i+1], y1[i+1]);
			line.DrawLine(x2[i], y2[i], x2[i+1], y2[i+1]);
			line.DrawLine(x3[i], y3[i], x3[i+1], y3[i+1]);
		}
	}

    c1->SaveAs(outputfile);
}

