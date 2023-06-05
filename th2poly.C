{
    TCanvas *c1 = new TCanvas("c1", "", 800, 600);
    c1->SetGridx();
    c1->SetGridy();
	c1->SetRightMargin(0.15);

    TFile *f = TFile::Open("./data/hexagons.root","R");

    TH2Poly *p = new TH2Poly("hexagonal histograms", "hexagonal histograms", -30, 30, -40, 25);
    p->SetStats(0);
    p->GetXaxis()->SetTitle("x (cm)");
    p->GetYaxis()->SetTitle("y (cm)");
    p->GetZaxis()->SetTitle("Ordinal numbers");

    TH2Poly *pa = new TH2Poly("another hexagonal histograms", "another hexagonal histograms", -30, 30, -40, 25);
    pa->SetStats(0);
    pa->GetXaxis()->SetTitle("x (cm)");
    pa->GetYaxis()->SetTitle("y (cm)");
    pa->GetZaxis()->SetTitle("Ordinal numbers");

    TH2Poly *pc = new TH2Poly("another hexagonal histograms", "another hexagonal histograms", -30, 30, -40, 25);
    pc->SetStats(0);
    pc->GetXaxis()->SetTitle("x (cm)");
    pc->GetYaxis()->SetTitle("y (cm)");
    pc->GetZaxis()->SetTitle("Ordinal numbers");

	int counter = 0;

    TGraph *gr;
    TKey *key;
    TIter nextkey(gDirectory->GetListOfKeys());
    while ((key = (TKey*)nextkey())) {
        TObject *obj = key->ReadObj();
        if(obj->InheritsFrom("TGraph")) {
            gr = (TGraph*) obj;
            p->AddBin(gr);
            pa->AddBin(gr);
            pc->AddBin(gr);
			counter+=1;
            //if(counter==50) break;
        }
    }

    TRandom r;
    p->ChangePartition(50, 50);

    //TH2Poly *pa = (TH2Poly*) p->Clone("another th2poly pa");

    for(int i=0; i<counter; ++i) {
        p->SetBinContent(i+1, i+1);
        pa->SetBinContent(i+1, counter-i);
        pc->SetBinContent(i+1, i+1);
        //pa->SetBinContent(i+1, i+1);
    }

    //----------------------------------------------------------------------
    // validate self update -> yes, the original pointer is updated
    //----------------------------------------------------------------------
    TH2Poly *pu = p;
    for(int i=0; i<counter; ++i) {
        double va = p->GetBinContent(i+1);
        double vb = pa->GetBinContent(i+1);
        pu->SetBinContent(i+1, va+vb);
    }
    p->Draw("colz;text");

    c1->SaveAs("output_v2.png");
    return;

    //----------------------------------------------------------------------
    // check of TH2Poly::Add(const TH1 *h1, Double_t c1)
    //----------------------------------------------------------------------
    TCanvas *c2 = new TCanvas("c2", "", 2400, 1800);
    c2->Divide(3,3,0.02,0.01);

    // default
    c2->cd(1);
    p->Draw("colz;text");

    c2->cd(2);
    TH1 *h = (TH1*) p;
    h->Draw("text");

    // inverting content, the TH2Poly looks the same after casting
    TH1* ha = (TH1*) pa;
    TH2Poly *pb = (TH2Poly*) ha;

    c2->cd(4);
    pa->SetTitle("another th2poly pa");
    pa->Draw("colz;text");

    c2->cd(5);
    ha->Draw("text");

    c2->cd(6);
    pb->Draw("colz;text");

    // looks not as expected
    int N = p->GetNcells();
    printf(">>> counter = %d\n", counter);
    printf(">>> p->GetNcells() = %d\n", N);
    printf(">>> p->GetNbinsX() = %d\n", p->GetNbinsX());
    printf(">>> p->GetNbinsY() = %d\n", p->GetNbinsY());
    printf(">>> p->GetNbinsZ() = %d\n", p->GetNbinsZ());

    c2->cd(7);
    //TH2Poly *pc = (TH2Poly*) p->Clone("another th2poly pc");
    pc->SetTitle("sum of two th2 poly");
    for(int i=0; i<counter; ++i) {
        double va = p->GetBinContent(i+1);
        double vb = pa->GetBinContent(i+1);
        pc->SetBinContent(i+1, va+vb);
    }
    pc->Draw("colz;text");

    // //TH2Poly *pc = (TH2Poly*) p->Clone("another th2poly pc");
    // pc->SetTitle("sum of two th2 poly");
    // pc->Add(pa, 1); // not working
    // pc->Draw("colz;text");

    // TH1 *hc = (TH1*) pc;
    // //hc->Add(h, ha, 1, 1); // not working
    // for(int i=0; i<counter; ++i) {
    //     double va = h->GetBinContent(i+1);
    //     double vb = ha->GetBinContent(i+1);
    //     hc->SetBinContent(i+1, va+vb);
    // }
    // //hc->Draw("colz;text");

    c2->SaveAs("output_v1.png");
    return;

	//--------------------------------------------------
    // test rest function -> Need to specify option -> works!
	//--------------------------------------------------
    // p->Reset("");

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

    p->Draw("colz;text");
    c1->SaveAs("output.png");

	TFile *fout = new TFile("output.root", "RECREATE");
	fout->cd();
	p->Write();
	fout->Close();
}

