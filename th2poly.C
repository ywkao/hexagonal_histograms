#include "include/auxiliary_boundary_lines.h"
#include "include/map_channel_numbers.h"
#include <map>

void beautify_plot(bool drawLine = true, bool drawText = true);

void th2poly(TString inputfile, TString outputfile, double range, bool drawLine=false, TString NameTag="LD_wafer"){
    TCanvas *c1 = new TCanvas("c1", "", 900, 900);
    c1->SetRightMargin(0.15);

    gStyle->SetPaintTextFormat(".0f");

    int scheme = 0;
    TString title;
    //--------------------------------------------------
    // Test profile
    //--------------------------------------------------
    TProfile *profile = new TProfile("profile", "profile", 234, 0, 234, 0, 1024);
    switch(scheme) {
        default:
            for(int i=0; i<234; ++i) {
                double value = (float)i;
                if(i==0) profile->Fill(i, value+1e-6);
                else profile->Fill(i, value);
            }
            break;

        case 1: // scheme: expected injected channels
            title = "Manual specification";
            for(int i=0; i<234; ++i) {
                double value = (float)i;
                if(i==0) profile->Fill(i, value+1e-6);
                else if(i==20) profile->Fill(i, value);
                else if(i==40) profile->Fill(i, value);
                else if(i==60) profile->Fill(i, value);
                else if(i==78) profile->Fill(i, value);
                else if(i==98) profile->Fill(i, value);
                else if(i==118) profile->Fill(i, value);
                else if(i==138) profile->Fill(i, value);
                else if(i==156) profile->Fill(i, value);
                else if(i==176) profile->Fill(i, value);
                else if(i==196) profile->Fill(i, value);
                else if(i==216) profile->Fill(i, value);
                else profile->Fill(i, -300.);
            }
            break;

        case 2: // scheme: results displayed on DQM GUI
            title = "DQM GUI (with readout sequence)";
            for(int i=0; i<234; ++i) {
                double value = (float)i;
                if(i==21) profile->Fill(i, value);
                else if(i==42) profile->Fill(i, value);
                else if(i==64) profile->Fill(i, value);
                else if(i==77) profile->Fill(i, value);
                else if(i==99) profile->Fill(i, value);
                else if(i==120) profile->Fill(i, value);
                else if(i==142) profile->Fill(i, value);
                else if(i==155) profile->Fill(i, value);
                else if(i==177) profile->Fill(i, value);
                else if(i==198) profile->Fill(i, value);
                else if(i==220) profile->Fill(i, value);
                else profile->Fill(i, -300.);
            }
            break;

    }

    // for(int ibin=0; ibin<=235; ++ibin) {
    //     double value = profile->GetBinContent(ibin);
    //     printf("ibin = %d, value = %f\n", ibin, value);
    // }

    //--------------------------------------------------
    // Hexagonal plots
    //--------------------------------------------------
    profile->Draw();
    c1->SaveAs("test.root");
    TFile *f = TFile::Open(inputfile,"R");

    TString newNameTag = NameTag;
    newNameTag.ReplaceAll("_", " ");

    title = newNameTag + " with global channel id (readout sequence)";
    TH2Poly *p = new TH2Poly("hexagonal histograms", title, -1*range, range, -1*range-2, range-2);
    p->SetStats(0);
    p->GetXaxis()->SetTitle("x (cm)");
    p->GetYaxis()->SetTitle("y (cm)");
    p->GetYaxis()->SetTitleOffset(1.1);

    title = newNameTag + " with HGCROC pin/chan";
    TH2Poly *p_pin = new TH2Poly("p_pin", title, -1*range, range, -1*range-2, range-2);
    p_pin->SetStats(0);
    p_pin->GetXaxis()->SetTitle("x (cm)");
    p_pin->GetYaxis()->SetTitle("y (cm)");
    p_pin->GetYaxis()->SetTitleOffset(1.1);

    title = newNameTag + " with Si cell pad Id";
    TH2Poly *p_sicell = new TH2Poly("p_sicell", title, -1*range, range, -1*range-2, range-2);
    p_sicell->SetStats(0);
    p_sicell->GetXaxis()->SetTitle("x (cm)");
    p_sicell->GetYaxis()->SetTitle("y (cm)");
    p_sicell->GetYaxis()->SetTitleOffset(1.1);

    int counter = 0;
    TGraph *gr;
    TKey *key;
    TIter nextkey(gDirectory->GetListOfKeys());
    while ((key = (TKey*)nextkey())) {
        TObject *obj = key->ReadObj();
        if(obj->InheritsFrom("TGraph")) {
            gr = (TGraph*) obj;
            p->AddBin(gr);
            p_pin->AddBin(gr);
            p_sicell->AddBin(gr);
            counter+=1;
        }
    }

    TRandom r;
    p->ChangePartition(100, 100);

    for(int i=0; i<counter; ++i) {
        double value = profile->GetBinContent(i+1);
        p->SetBinContent(i+1, value);

        if(i==0 || i==78 || i==156)
            p_pin->SetBinContent(i+1, 0.000001);
        else
            p_pin->SetBinContent(i+1, map_HGCROC_pin[i]);

        p_sicell->SetBinContent(i+1, map_SiCell_padId[i]);
    }

    p->SetMarkerSize(0.7);
    p->Draw("colz;text");
    beautify_plot(drawLine);
    c1->SaveAs(outputfile);
    c1->SaveAs("info_"+NameTag+"_globalChannelId_readoutSequence.png");

    p_pin->SetMarkerSize(0.7);
    p_pin->Draw("colz;text");
    beautify_plot(drawLine);
    c1->SaveAs("info_"+NameTag+"_HGCROC_pin_chan.png");

    p_sicell->SetMarkerSize(0.7);
    p_sicell->Draw("colz;text");
    beautify_plot(drawLine);
    c1->SaveAs("info_"+NameTag+"_SiCell_padId.png");

    //-----------------------------------------------------------------
    // Reminder: counter = nCells - 9
    //-----------------------------------------------------------------
    // printf("[INFO] nCells  = %d\n", p->GetNcells());
    // printf("[INFO] counter = %d\n", counter);

}

void beautify_plot(bool drawLine = true, bool drawText = true) {
    //-----------------------------------------------------------------
    // cosmetics
    //-----------------------------------------------------------------
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

    if(drawText) {
        TText text;
        text.SetTextAlign(22);
        text.SetTextFont(43);
        text.SetTextSize(12);

        double theta1 = -TMath::Pi()/3.;
        double theta2 = TMath::Pi()/3.;
        double theta3 = TMath::Pi();
        std::vector<double> theta_angle_text = {60, 60, -60, -60, 0, 0};
        std::vector<double> theta_coordinate_text = {theta1, theta1, theta2, theta2, theta3, theta3};
        //std::vector<double> x_coordinate_text = {-6.25, 6.25, -6.25, 6.25, -6.25, 6.25};
        std::vector<double> x_coordinate_text = {-6.25, 6.25, -5, 7.5, -6.25, 6.25};
        std::vector<double> y_coordinate_text = {23.5, 23.5, 26, 26, 26.4, 26.4};
        std::vector<TString> v_texts = {"chip-0, half-1", "chip-0, half-0",
                                        "chip-1, half-1", "chip-1, half-0",
                                        "chip-2, half-1", "chip-2, half-0"};

        double arbUnit_to_cm = 17./24.;

        // evaluate (r, phi) and apply rotation
        for(int i=0; i<6; ++i) {
            text.SetTextAngle(theta_angle_text[i]);
            double theta = theta_coordinate_text[i];
            double cos_theta = TMath::Cos(theta);
            double sin_theta = TMath::Sin(theta);

            double x = x_coordinate_text[i];
            double y = y_coordinate_text[i];
            double r = sqrt(pow(x,2)+pow(y,2));
            double cos_phi = x/r;
            double sin_phi = y/r;
            x = r*(cos_phi*cos_theta + sin_phi*sin_theta)*arbUnit_to_cm;
            y = r*(sin_phi*cos_theta - cos_phi*sin_theta)*arbUnit_to_cm;
            text.DrawText(x, y, v_texts[i]);
        }
    }
}
