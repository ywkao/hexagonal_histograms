#include "include/auxiliary_boundary_lines.h"

void th2poly(TString inputfile, TString outputfile, double range, bool drawLine=false){
    TCanvas *c1 = new TCanvas("c1", "", 900, 900);
	c1->SetRightMargin(0.15);

    TFile *f = TFile::Open(inputfile,"R");

    TH2Poly *p = new TH2Poly("hexagonal histograms", "Low density wafer map with pad id", -1*range, range, -1*range, range);
    p->SetStats(0);
    p->GetXaxis()->SetTitle("x (arb. unit)");
    p->GetYaxis()->SetTitle("y (arb. unit)");
    //p->GetZaxis()->SetTitle("Ordinal numbers");
    p->GetYaxis()->SetTitleOffset(1.1);

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
		// load N_boundary_points, x1, x2, x3, y1, y2, y3 from auxiliary_boundary_lines.h

		TLine line;
		line.SetLineStyle(1);
		line.SetLineColor(2);
		line.SetLineWidth(2);

		for(int i=0; i<aux::N_boundary_points-1; ++i) {
			line.DrawLine(aux::x1[i], aux::y1[i], aux::x1[i+1], aux::y1[i+1]);
			line.DrawLine(aux::x2[i], aux::y2[i], aux::x2[i+1], aux::y2[i+1]);
			line.DrawLine(aux::x3[i], aux::y3[i], aux::x3[i+1], aux::y3[i+1]);
			line.DrawLine(aux::x4[i], aux::y4[i], aux::x4[i+1], aux::y4[i+1]);
			line.DrawLine(aux::x5[i], aux::y5[i], aux::x5[i+1], aux::y5[i+1]);
			line.DrawLine(aux::x6[i], aux::y6[i], aux::x6[i+1], aux::y6[i+1]);
		}
	}

    c1->SaveAs(outputfile);
}

