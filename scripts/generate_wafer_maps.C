#include <map>
#include "TMath.h"
#include "auxiliary.h"

void beautify_plot(bool drawLine = true, bool drawText = true, TString NameTag = "LD_wafer", double extra_angle = 0.0, TString rotationTag = "");

void generate_wafer_maps(TString inputfile, TString outputfile, double range, bool drawLine=false, TString NameTag="LD_wafer", double MarkerSize = 0.7, TString rotationTag = ""){

    double extra_angle = 0.0;

    if(rotationTag=="_rotation150")
        extra_angle = 5. * TMath::Pi() / 6.;
    if(rotationTag=="_rotation30")
        extra_angle = TMath::Pi() / 6.;

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

    printf("[DEBUG] ./scripts/generate_wafer_maps: NameTag = %s, counter = %d\n", NameTag.Data(), counter);

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

    // profile->Draw();
    // c1->SaveAs("test.root");

    //--------------------------------------------------
    // fill information of channel IDs
    //--------------------------------------------------
    p->ChangePartition(100, 100);

    std::map<int, int> map_HGCROC_pin;
    std::map<int, int> map_SiCell_pad;

    if (NameTag.Contains("MH_B")) {
        map_HGCROC_pin = map_HGCROC_pin_MH_B;
        map_SiCell_pad = map_SiCell_pad_MH_B;
    } else if (NameTag.Contains("MH_F")) {
        map_HGCROC_pin = map_HGCROC_pin_MH_F;
        map_SiCell_pad = map_SiCell_pad_MH_F;
    } else if (NameTag.Contains("MH_L")) {
        map_HGCROC_pin = map_HGCROC_pin_MH_L;
        map_SiCell_pad = map_SiCell_pad_MH_L;
    } else if (NameTag.Contains("MH_R")) {
        map_HGCROC_pin = map_HGCROC_pin_MH_R;
        map_SiCell_pad = map_SiCell_pad_MH_R;
    } else if (NameTag.Contains("MH_T")) {
        map_HGCROC_pin = map_HGCROC_pin_MH_T;
        map_SiCell_pad = map_SiCell_pad_MH_T;
    } else if (NameTag.Contains("ML_5")) {
        map_HGCROC_pin = map_HGCROC_pin_ML_5;
        map_SiCell_pad = map_SiCell_pad_ML_5;
    } else if (NameTag.Contains("ML_B")) {
        map_HGCROC_pin = map_HGCROC_pin_ML_B;
        map_SiCell_pad = map_SiCell_pad_ML_B;
    } else if (NameTag.Contains("ML_F")) {
        map_HGCROC_pin = map_HGCROC_pin_ML_F;
        map_SiCell_pad = map_SiCell_pad_ML_F;
    } else if (NameTag.Contains("ML_L")) {
        map_HGCROC_pin = map_HGCROC_pin_ML_L;
        map_SiCell_pad = map_SiCell_pad_ML_L;
    } else if (NameTag.Contains("ML_R")) {
        map_HGCROC_pin = map_HGCROC_pin_ML_R;
        map_SiCell_pad = map_SiCell_pad_ML_R;
    } else {
        map_HGCROC_pin = map_HGCROC_pin_ML_T;
        map_SiCell_pad = map_SiCell_pad_ML_T;
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
    bool drawText = false;
    if(scheme==0) {
        p->SetMarkerSize(MarkerSize);
        p->Draw("colz;text");
        beautify_plot(drawLine, drawText, NameTag, extra_angle, rotationTag);
        c1->SaveAs("output/waferMaps/info_"+NameTag+"_globalChannelId_readoutSequence"+rotationTag+".png");
        // c1->SaveAs("output/waferMaps/info_"+NameTag+"_globalChannelId_readoutSequence"+rotationTag+".pdf");

        p_pin->SetMarkerSize(MarkerSize);
        p_pin->Draw("colz;text");
        beautify_plot(drawLine, drawText, NameTag, extra_angle, rotationTag);
        c1->SaveAs("output/waferMaps/info_"+NameTag+"_HGCROC_pin_chan"+rotationTag+".png");
        // c1->SaveAs("output/waferMaps/info_"+NameTag+"_HGCROC_pin_chan"+rotationTag+".pdf");

        p_sicell->SetMarkerSize(MarkerSize);
        p_sicell->Draw("colz;text");
        beautify_plot(drawLine, drawText, NameTag, extra_angle, rotationTag);
        c1->SaveAs("output/waferMaps/info_"+NameTag+"_SiCell_padId"+rotationTag+".png");
        // c1->SaveAs("output/waferMaps/info_"+NameTag+"_SiCell_padId"+rotationTag+".pdf");
    } else {
        p->SetMarkerSize(MarkerSize);
        p->Draw("colz;text");
        beautify_plot(drawLine, drawText, NameTag, extra_angle, rotationTag);
        c1->SaveAs("test_injection_"+NameTag+".png");
    }

    //-----------------------------------------------------------------
    // Reminder: counter = nCells - 9
    //-----------------------------------------------------------------
    // printf("[INFO] nCells  = %d\n", p->GetNcells());
    // printf("[INFO] counter = %d\n", counter);

}

void beautify_plot(bool drawLine = true, bool drawText = true, TString NameTag = "LD_wafer", double extra_angle = 0.0, TString rotationTag = "") {
    //-----------------------------------------------------------------
    // cosmetics
    //-----------------------------------------------------------------
    if(drawLine) {
        TLine line;
        line.SetLineStyle(1);
        line.SetLineColor(2);
        line.SetLineWidth(2);

        if(NameTag.Contains("ML_L")) {
            for(int i=0; i<14; ++i)
                line.DrawLine(aux::x1_partial_wafer[i], aux::y1_partial_wafer[i], aux::x1_partial_wafer[i+1], aux::y1_partial_wafer[i+1]);
            for(int i=0; i<16; ++i)
                line.DrawLine(aux::x2_partial_wafer[i], aux::y2_partial_wafer[i], aux::x2_partial_wafer[i+1], aux::y2_partial_wafer[i+1]);
        } else if(NameTag.Contains("ML_R")) {
            for(int i=0; i<14; ++i)
                line.DrawLine(aux::x1_LD4_partial_wafer[i], aux::y1_LD4_partial_wafer[i], aux::x1_LD4_partial_wafer[i+1], aux::y1_LD4_partial_wafer[i+1]);
            for(int i=0; i<16; ++i)
                line.DrawLine(aux::x2_LD4_partial_wafer[i], aux::y2_LD4_partial_wafer[i], aux::x2_LD4_partial_wafer[i+1], aux::y2_LD4_partial_wafer[i+1]);
        } else if(NameTag.Contains("MH_F")) {
            for(int i=0; i<aux::N_HD_boundary_points-1; ++i) {
                line.DrawLine(aux::x1_HD_full_wafer[i], aux::y1_HD_full_wafer[i], aux::x1_HD_full_wafer[i+1], aux::y1_HD_full_wafer[i+1]);
                line.DrawLine(aux::x2_HD_full_wafer[i], aux::y2_HD_full_wafer[i], aux::x2_HD_full_wafer[i+1], aux::y2_HD_full_wafer[i+1]);
                line.DrawLine(aux::x3_HD_full_wafer[i], aux::y3_HD_full_wafer[i], aux::x3_HD_full_wafer[i+1], aux::y3_HD_full_wafer[i+1]);
                line.DrawLine(aux::x4_HD_full_wafer[i], aux::y4_HD_full_wafer[i], aux::x4_HD_full_wafer[i+1], aux::y4_HD_full_wafer[i+1]);
                line.DrawLine(aux::x5_HD_full_wafer[i], aux::y5_HD_full_wafer[i], aux::x5_HD_full_wafer[i+1], aux::y5_HD_full_wafer[i+1]);
                line.DrawLine(aux::x6_HD_full_wafer[i], aux::y6_HD_full_wafer[i], aux::x6_HD_full_wafer[i+1], aux::y6_HD_full_wafer[i+1]);
            }
        } else { // LD full wafer
            for(int i=0; i<aux::N_boundary_points-1; ++i) {
                line.DrawLine(aux::x1[i], aux::y1[i], aux::x1[i+1], aux::y1[i+1]);
                line.DrawLine(aux::x2[i], aux::y2[i], aux::x2[i+1], aux::y2[i+1]);
                line.DrawLine(aux::x3[i], aux::y3[i], aux::x3[i+1], aux::y3[i+1]);
                line.DrawLine(aux::x4[i], aux::y4[i], aux::x4[i+1], aux::y4[i+1]);
                line.DrawLine(aux::x5[i], aux::y5[i], aux::x5[i+1], aux::y5[i+1]);
                line.DrawLine(aux::x6[i], aux::y6[i], aux::x6[i+1], aux::y6[i+1]);
            }
        }
    }

    if(drawText) {
        TText text;
        text.SetTextAlign(22);
        text.SetTextFont(43);
        text.SetTextSize(12);

        if(NameTag.Contains("MH_F")) {
            double theta1 = 0. + extra_angle;
            double theta2 = 4*TMath::Pi()/3. + extra_angle;
            double theta3 = 2*TMath::Pi()/3. + extra_angle;

            std::vector<double> theta_angle_text = {0, 0, 120, 120, -120, -120};
            if(rotationTag.Contains("150"))
                theta_angle_text = {-150, -150, -30, -30, 90, 90};
            else if(rotationTag.Contains("30"))
                theta_angle_text = {-30, -30, 90, 90, -150, -150};

            // std::vector<double> theta_angle_text = {0, 0, 120, 120, -120, -120};
            // std::vector<double> theta_angle_text = {-extra_angle, -extra_angle, -extra_angle+120, -extra_angle+120, -extra_angle-120, -extra_angle-120};
            std::vector<double> theta_coordinate_text = {theta1, theta1, theta2, theta2, theta3, theta3};
            std::vector<double> x_coordinate_text = {-6.25, 6.25, -6.25, 6.25, -6.25, 6.25};
            std::vector<double> y_coordinate_text = {26, 26, 26, 26, 26, 26};
            std::vector<TString> v_texts = {"chip-0", "chip-1", "chip-2", "chip-3", "chip-4", "chip-5"};

            double arbUnit_to_cm = 6.9767/20.;

            // evaluate (r, phi) and apply rotation
            for(int i=0; i<6; ++i) {
                text.SetTextAngle(theta_angle_text[i]);
                double theta = theta_coordinate_text[i];
                // printf("%.2f ", theta);
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
            // printf("\n");

        } else { // LD
            double theta1 = -TMath::Pi()/3. + extra_angle;
            double theta2 = TMath::Pi()/3. + extra_angle;
            double theta3 = TMath::Pi() + extra_angle;
            double a = extra_angle * 180. / TMath::Pi();
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
                if(NameTag.Contains("ML_L") && (i==2||i==3||i==4)) continue;
                if(NameTag.Contains("ML_R") && (i==0||i==1||i==5)) continue;

                double angle = theta_angle_text[i] - a;
                angle = (fabs(angle)<90.) ? angle : angle+180;
                text.SetTextAngle(angle);
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

                if(NameTag.Contains("ML_L") && (i==5))
                    text.DrawText(x, y, "chip-1, half-0");
                else if(NameTag.Contains("ML_R") && (i==2))
                    text.DrawText(x, y, "chip-1, half-0");
                else if(NameTag.Contains("ML_R") && (i==3))
                    text.DrawText(x, y, "chip-0, half-1");
                else if(NameTag.Contains("ML_R") && (i==4))
                    text.DrawText(x, y, "chip-0, half-0");
                else
                    text.DrawText(x, y, v_texts[i]);
            }
        }
    }
}
