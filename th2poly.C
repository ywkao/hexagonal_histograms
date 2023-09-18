#include "include/auxiliary_boundary_lines.h"
#include "include/auxiliary_boundary_lines_partial_wafer.h"
#include "include/auxiliary_boundary_lines_HD_full_wafer.h"
#include "include/map_channel_numbers.h"
#include <map>

void beautify_plot(bool drawLine = true, bool drawText = true, TString NameTag = "LD_wafer");

void th2poly(TString inputfile, TString outputfile, double range, bool drawLine=false, TString NameTag="LD_wafer", double MarkerSize = 0.7){
    TCanvas *c1 = new TCanvas("c1", "", 900, 900);
    c1->SetRightMargin(0.15);
    gStyle->SetPaintTextFormat(".0f");

    //--------------------------------------------------
    // Hexagonal plots
    //--------------------------------------------------
    TFile *f = TFile::Open(inputfile,"R");

    TString title;
    TString newNameTag = NameTag;
    newNameTag.ReplaceAll("_", " ");

    title = newNameTag + " with global channel id (readout sequence)";
    TH2Poly *p = new TH2Poly("hexagonal histograms", title, -1*range, range, -1*range, range);
    p->SetStats(0);
    p->GetXaxis()->SetTitle("x (cm)");
    p->GetYaxis()->SetTitle("y (cm)");
    p->GetYaxis()->SetTitleOffset(1.1);

    title = newNameTag + " with HGCROC pin/chan";
    TH2Poly *p_pin = new TH2Poly("p_pin", title, -1*range, range, -1*range, range);
    p_pin->SetStats(0);
    p_pin->GetXaxis()->SetTitle("x (cm)");
    p_pin->GetYaxis()->SetTitle("y (cm)");
    p_pin->GetYaxis()->SetTitleOffset(1.1);

    title = newNameTag + " with Si cell pad Id";
    TH2Poly *p_sicell = new TH2Poly("p_sicell", title, -1*range, range, -1*range, range);
    p_sicell->SetStats(0);
    p_sicell->GetXaxis()->SetTitle("x (cm)");
    p_sicell->GetYaxis()->SetTitle("y (cm)");
    p_sicell->GetYaxis()->SetTitleOffset(1.1);

    // load polygonal bins
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

    printf("[DEBUG] th2poly::counter = %d\n", counter);

    //--------------------------------------------------
    // Test profile
    //--------------------------------------------------
    int scheme = 0;
    TProfile *profile = new TProfile("profile", "profile", counter, 0, counter, 0, 1024);
    switch(scheme) {
        default:
            for(int i=0; i<counter; ++i) {
                double value = (float)i;
                if(i==0) profile->Fill(i, value+1e-6);
                else profile->Fill(i, value);
            }
            break;

        case 1: // scheme: expected injected channels
            title = "Manual specification";
            for(int i=0; i<counter; ++i) {
                // test on calibration channels
                if(i==18 || i==57 || i==96 || i==135 || i==174 || i==213) {
                    profile->Fill(i, 100);
                }
                continue;

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
            for(int i=0; i<counter; ++i) {
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

    profile->Draw();
    c1->SaveAs("test.root");

    //--------------------------------------------------
    // fill information of channel IDs
    //--------------------------------------------------
    p->ChangePartition(100, 100);

    std::map<int, int> map_HGCROC_pin;
    std::map<int, int> map_SiCell_pad;

    if(NameTag.Contains("partial")) {
        map_HGCROC_pin = map_HGCROC_pin_partial_wafer;
        map_SiCell_pad = map_SiCell_pad_partial_wafer;
    } else if (NameTag.Contains("HD")){
        map_HGCROC_pin = map_HGCROC_pin_HD_full_wafer;
        map_SiCell_pad = map_SiCell_pad_HD_full_wafer;
    } else { // LD full
        map_HGCROC_pin = map_HGCROC_pin_full_wafer;
        map_SiCell_pad = map_SiCell_pad_full_wafer;
    }

    for(int i=0; i<counter; ++i) {
        double value = profile->GetBinContent(i+1);
        p->SetBinContent(i+1, value);

        if(i%78==0)
            p_pin->SetBinContent(i+1, 0.000001);
        else
            p_pin->SetBinContent(i+1, map_HGCROC_pin[i]);

        p_sicell->SetBinContent(i+1, map_SiCell_pad[i]);
    }

    // plotting
    if(scheme==0) {
        p->SetMarkerSize(MarkerSize);
        p->Draw("colz;text");
        beautify_plot(drawLine, true, NameTag);
        c1->SaveAs("waferMaps/info_"+NameTag+"_globalChannelId_readoutSequence.png");
        c1->SaveAs("waferMaps/info_"+NameTag+"_globalChannelId_readoutSequence.pdf");

        p_pin->SetMarkerSize(MarkerSize);
        p_pin->Draw("colz;text");
        beautify_plot(drawLine, true, NameTag);
        c1->SaveAs("waferMaps/info_"+NameTag+"_HGCROC_pin_chan.png");
        c1->SaveAs("waferMaps/info_"+NameTag+"_HGCROC_pin_chan.pdf");

        p_sicell->SetMarkerSize(MarkerSize);
        p_sicell->Draw("colz;text");
        beautify_plot(drawLine, true, NameTag);
        c1->SaveAs("waferMaps/info_"+NameTag+"_SiCell_padId.png");
        c1->SaveAs("waferMaps/info_"+NameTag+"_SiCell_padId.pdf");
    } else {
        p->SetMarkerSize(MarkerSize);
        p->Draw("colz;text");
        beautify_plot(drawLine, true, NameTag);
        c1->SaveAs("test_injection_"+NameTag+".png");
    }

    //-----------------------------------------------------------------
    // Reminder: counter = nCells - 9
    //-----------------------------------------------------------------
    // printf("[INFO] nCells  = %d\n", p->GetNcells());
    // printf("[INFO] counter = %d\n", counter);

}

void beautify_plot(bool drawLine = true, bool drawText = true, TString NameTag = "LD_wafer") {
    //-----------------------------------------------------------------
    // cosmetics
    //-----------------------------------------------------------------
    if(drawLine && NameTag.Contains("partial")) {
        TLine line;
        line.SetLineStyle(1);
        line.SetLineColor(2);
        line.SetLineWidth(2);

        for(int i=0; i<14; ++i)
            line.DrawLine(aux::x1_partial_wafer[i], aux::y1_partial_wafer[i], aux::x1_partial_wafer[i+1], aux::y1_partial_wafer[i+1]);

        for(int i=0; i<16; ++i)
            line.DrawLine(aux::x2_partial_wafer[i], aux::y2_partial_wafer[i], aux::x2_partial_wafer[i+1], aux::y2_partial_wafer[i+1]);

    } else if(drawLine && NameTag.Contains("HD")) {
        TLine line;
        line.SetLineStyle(1);
        line.SetLineColor(2);
        line.SetLineWidth(2);

        for(int i=0; i<aux::N_HD_boundary_points-1; ++i) {
            line.DrawLine(aux::x1_HD_full_wafer[i], aux::y1_HD_full_wafer[i], aux::x1_HD_full_wafer[i+1], aux::y1_HD_full_wafer[i+1]);
            line.DrawLine(aux::x2_HD_full_wafer[i], aux::y2_HD_full_wafer[i], aux::x2_HD_full_wafer[i+1], aux::y2_HD_full_wafer[i+1]);
            line.DrawLine(aux::x3_HD_full_wafer[i], aux::y3_HD_full_wafer[i], aux::x3_HD_full_wafer[i+1], aux::y3_HD_full_wafer[i+1]);
        }

    } else if(drawLine) {
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

        if(NameTag.Contains("HD")) {
            double theta1 = 0.;
            double theta2 = 4*TMath::Pi()/3.;
            double theta3 = 2*TMath::Pi()/3.;

            std::vector<double> theta_angle_text = {0, 0, 120, 120, -120, -120};
            std::vector<double> theta_coordinate_text = {theta1, theta1, theta2, theta2, theta3, theta3};

            std::vector<double> x_coordinate_text = {-6.25, 6.25, -6.25, 6.25, -6.25, 6.25};
            std::vector<double> y_coordinate_text = {26, 26, 26, 26, 26, 26};
            std::vector<TString> v_texts = {"chip-0", "chip-1", "chip-2", "chip-3", "chip-4", "chip-5"};

            double arbUnit_to_cm = 6.9767/20.;

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

        } else { // LD
            double theta1 = -TMath::Pi()/3.;
            double theta2 = TMath::Pi()/3.;
            double theta3 = TMath::Pi();
            std::vector<double> theta_angle_text = {60, 60, -60, -60, 0, 0};
            std::vector<double> theta_coordinate_text = {theta1, theta1, theta2, theta2, theta3, theta3};
            std::vector<double> x_coordinate_text = {-6.25, 6.25, -6.25, 6.25, -6.25, 6.25};
            std::vector<double> y_coordinate_text = {26, 26, 26, 26, 26, 26};
            std::vector<TString> v_texts = {"chip-0, half-1", "chip-0, half-0",
                                            "chip-1, half-1", "chip-1, half-0",
                                            "chip-2, half-1", "chip-2, half-0"};

            double arbUnit_to_cm = 6.9767/20.;

            // evaluate (r, phi) and apply rotation
            for(int i=0; i<6; ++i) {
                if(NameTag.Contains("partial") && (i==2||i==3||i==4)) continue;
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

                if(NameTag.Contains("partial") && (i==5))
                    text.DrawText(x, y, "chip-1, half-0");
                else
                    text.DrawText(x, y, v_texts[i]);
            }
        }
    }
}
