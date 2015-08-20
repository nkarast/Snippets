#include <iostream>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TLegend.h>
#include <TLatex.h>
#include <TString.h>
#include <TMath.h>
#include <TStyle.h>
#include <stdio.h>
#include <cstring>

using namespace std;

// Definition of asci escape characters for color
#define RESET   "\033[0m"
#define BLACK   "\033[30m"        /* Black */
#define RED     "\033[31m"        /* Red */
#define GREEN   "\033[32m"        /* Green */
#define YELLOW    "\033[33m"        /* Yellow */
#define BLUE    "\033[34m"        /* Blue */
#define MAGENTA   "\033[35m"        /* Magenta */
#define CYAN    "\033[36m"        /* Cyan */
#define WHITE   "\033[37m"        /* White */

#define BOLDBLACK   "\033[1m\033[30m"   /* Bold Black */
#define BOLDRED     "\033[1m\033[31m"   /* Bold Red */
#define BOLDGREEN   "\033[1m\033[32m"   /* Bold Green */
#define BOLDYELLOW  "\033[1m\033[33m"   /* Bold Yellow */
#define BOLDBLUE    "\033[1m\033[34m"   /* Bold Blue */
#define BOLDMAGENTA "\033[1m\033[35m"   /* Bold Magenta */
#define BOLDCYAN    "\033[1m\033[36m"   /* Bold Cyan */
#define BOLDWHITE   "\033[1m\033[37m"   /* Bold White */




void colcout(string str, string color){
    char strCol[1000];
    sprintf(strCol,"%s%s%s",color.c_str(),str.c_str(),RESET);
    cout<<strCol<<endl;
}


void setStyle()
{
    
    gStyle->SetOptStat(0);
    
    gStyle->SetCanvasBorderMode(0); //frame color of canvas
    gStyle->SetCanvasColor(0);  //bkrd color of canvas
    gStyle->SetStatBorderSize(0); //frame style of stat-box 1
    
    gStyle->SetTitleBorderSize(0);
    gStyle->SetTitleFillColor(0);
    gStyle->SetPadColor(0);
    gStyle->SetPadBorderMode(0);
    
    gStyle->SetLineWidth(3); // width of ticks
    gStyle->SetPadTickX(0); //1:ticks on upper,2: ticks+labels on upper xaxis
    gStyle->SetPadTickY(0);
    
    gStyle->SetPadLeftMargin(0.12); // 0.18
    gStyle->SetPadRightMargin(0.08);
    gStyle->SetPadTopMargin(0.07);
    gStyle->SetPadBottomMargin(0.17);
    gStyle->SetFrameLineWidth(2);
    gStyle->SetFrameFillColor(0);
    gStyle->SetPaintTextFormat(".2f");
    
    gStyle->SetTitleOffset(1.1,"X");
    gStyle->SetTitleOffset(1.1,"Y");
    gStyle->SetTextFont(42);
    
}

void setHSG3Style()
{
    
    gStyle->SetOptStat(0);
    
    gStyle->SetFillColor(10);
    gStyle->SetFrameFillColor(10);
    gStyle->SetCanvasColor(10);
    gStyle->SetPadColor(10);
    gStyle->SetTitleFillColor(0);
    gStyle->SetStatColor(10);
    
    gStyle->SetCanvasBorderMode(0);
    gStyle->SetFrameBorderMode(0);
    gStyle->SetPadBorderMode(0);
    gStyle->SetDrawBorder(0);
    gStyle->SetTitleBorderSize(0);
    
    gStyle->SetFuncWidth(2);
    gStyle->SetHistLineWidth(2);
    gStyle->SetFuncColor(2);
    
    gStyle->SetPadTopMargin(0.05);
    gStyle->SetPadBottomMargin(0.16);
    gStyle->SetPadLeftMargin(0.16);
    gStyle->SetPadRightMargin(0.05);
    
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    
    gStyle->SetFrameLineWidth(1);
    gStyle->SetLineWidth(1); // width of ticks
    
}
void setHistoStyle(TH1F* histo)
{
    
    histo->SetTitle("");
    histo->SetLineWidth(3);
    histo->SetTitleSize(0.07,"x");
    histo->SetTitleSize(0.07,"y");
    histo->SetNdivisions(505,"x");
    histo->SetNdivisions(505,"y");
    histo->SetLabelSize(0.07,"x");
    histo->SetLabelSize(0.07,"y");
    histo->SetTitleOffset(1.,"x");
    histo->SetTitleOffset(1.,"y");
}

void setHistoStyle(TProfile* histo)
{
    
    histo->SetTitle("");
    histo->SetLineWidth(3);
    histo->SetTitleSize(0.07,"x");
    histo->SetTitleSize(0.07,"y");
    histo->SetNdivisions(505,"x");
    histo->SetNdivisions(505,"y");
    histo->SetLabelSize(0.07,"x");
    histo->SetLabelSize(0.07,"y");
    histo->SetTitleOffset(1.,"x");
    histo->SetTitleOffset(1.,"y");
}


void setHistoHSG3Style(TH1F* histo)
{
    
    histo->SetTitle("");
    histo->SetLineWidth(0);
    //histo->SetLineWidth(3);
    histo->SetTitleSize(0.07,"x");
    histo->SetTitleSize(0.07,"y");
    histo->SetNdivisions(510,"x");
    histo->SetNdivisions(510,"y");
    histo->SetLabelSize(0.05,"x");
    histo->SetLabelSize(0.05,"y");
    histo->SetTitleOffset(1.1,"x");
    histo->SetTitleOffset(1.1,"y");
}

void drawNorm(TString normtxt)
{
    TLatex *normbox = new TLatex();
    normbox->SetNDC();
    normbox->SetTextSize(0.04);
    normbox->SetTextAngle(90);
    normbox->DrawLatex(0.975,0.18,normtxt);
    normbox->Draw();
}

void drawOverflow(TH1 *h){
    Int_t nx1  = h->GetNbinsX()+1;
    Int_t nx  = h->GetNbinsX();
    Double_t x = h->GetBinContent(nx);
    Double_t x1 = h->GetBinContent(nx1);
    h->SetBinContent(nx,x+x1);
    h->SetBinContent(nx1,0);
    Double_t ex = h->GetBinError(nx);
    Double_t ex1 = h->GetBinError(nx1);
    h->SetBinError(nx,ex+ex1);
    h->SetBinError(nx1,0);
}

void setPadStyle(TPad *pad)
{
    pad->SetTopMargin(0.07);
    pad->SetBottomMargin(0.05);
    pad->SetFrameLineWidth(2);
    pad->SetLeftMargin(0.16);
     //   pad->SetRightMargin(0.20);
    
}

void setsubPadStyle(TPad *pad)
{
    pad->SetBottomMargin(0.4);
    pad->SetFrameLineWidth(2);
    pad->SetLeftMargin(0.14);//016
}




void makeRatioPlot(TH1F *h_a, TH1F *h_b, TString histo_a_legend, TString histo_b_legend, TString histo_a_name, TString histo_b_name, TString var_name, TString x_name, TString y_name, TString ratio_name, TString plotDir="./"){
    
    
    colcout("[Warning] - makeRatioPlot() : Make sure that you want histo_a/histo_b ratio.", CYAN);
    
    gStyle->SetOptStat(0);
    
    // Normalize histograms to unity
    //h_a->Scale(1/h_a->Integral());
    //h_b->Scale(1/h_b->Integral());
    
    h_a->Sumw2();
    h_b->Sumw2();
    
    // Set colors and width
    h_a->SetLineColor(kRed);
    h_a->SetLineWidth(2);
    h_b->SetLineColor(kBlue);
    h_b->SetLineWidth(2);
    
    // Create the ratio histogram ratio = a/b
    TH1F *h_ratio = (TH1F*) h_a->Clone();
    h_ratio->Divide(h_b);
    
    TLatex *ks = new TLatex();
    ks->SetNDC();
    ks->SetTextFont(42);
    ks->SetTextSize(0.04);
    ks->SetTextColor(kRed);
    Double_t ksValue = 0.0;
    ksValue = h_a->KolmogorovTest(h_b);
    
    TCanvas *canvas = new TCanvas(x_name.Data(), x_name.Data(), 800,800);
    TPad *pad2 = new TPad("pad2","",0,0,1,0.3);
    setsubPadStyle(pad2);
    pad2->SetGrid();
    pad2->Draw();
    pad2->cd();
    h_ratio->SetTitle("");
    h_ratio->SetMaximum(1.1);
    h_ratio->SetMinimum(0.9);
    h_ratio->Draw("hist");
    h_ratio->GetYaxis()->SetTitle(ratio_name.Data());
    h_ratio->GetXaxis()->SetTitle(x_name.Data());
    h_ratio->GetYaxis()->SetRangeUser(0.9,1.1);
    h_ratio->SetTickLength(0.04,"y");
    h_ratio->SetTickLength(0.15,"x");
    h_ratio->SetMarkerStyle(20);
    h_ratio->SetMarkerColor(kBlack);
    h_ratio->SetMarkerSize(0.8);
    h_ratio->SetTitleSize(0.15,"x");
    h_ratio->SetTitleSize(0.15,"y");
    h_ratio->SetTitleOffset(0.45, "y");
    h_ratio->SetLabelSize(0.12, "x");
    h_ratio->SetLabelSize(0.12, "y");
    h_ratio->SetNdivisions(505, "y");
    canvas->cd();
    
    TPad *pad1 = new TPad("pad1","",0,0.3,1,1);
    setPadStyle(pad1);
    pad1->Draw();
    pad1->cd();
    h_a->SetMinimum(0.);
    h_a->SetTitle("");
    h_a->Draw("hist");
    h_a->SetLabelSize(0.,"x");
    h_a->GetYaxis()->SetTitle(y_name.Data());
    h_b->Draw("hist same");
    TLegend *leg = new TLegend(0.60, 0.70, 0.94, 0.90);
    leg->SetBorderSize(0);
    leg->SetTextFont(42);
    leg->SetTextSize(0.032);
    leg->SetFillColor(0);
    leg->SetNColumns(2);
    leg->AddEntry(h_a,histo_a_legend.Data(),"lep");
    leg->AddEntry(h_b,histo_b_legend.Data(),"lep");
    leg->Draw("same");
    ks->DrawLatex(0.7,0.69,Form("KS-test= %.2f", ksValue));
    
    TString canvasName;
    canvasName = plotDir+var_name+"_"+histo_a_name+"_"+histo_b_name+"_ratio.pdf";
    canvas->SaveAs(canvasName.Data());
    
    
}


void plot_comp(TH1F* histo1, TH1F* histo2, TString sample, TString var_nameX, TString var_nameY, TString ratio_name, TString legend1, TString legend2, TString outputdir) {
    
    setHSG3Style();
    
    Bool_t doPrelim = false;
    Bool_t doRatio = true;
    Bool_t doNorm = true;
    TString Lumi = "20.3";
    Int_t canvX = 0;
    Int_t canvY = 0;
    if(doRatio) {canvX=800; canvY=800;}
    else  {canvX=800; canvY=600;}
    
	if(doNorm) {
		histo1->Scale(1/histo1->Integral());
		histo2->Scale(1/histo2->Integral());
	}
	setHistoStyle(histo1);
	setHistoStyle(histo2);
	histo1->SetLineColor(14);//kBlack);
	histo2->SetLineColor(kRed-2);
    histo1->SetLineStyle(2);
    
	//sys histo
	TCanvas *canvas = new TCanvas(sample+"_"+histo1->GetName(),sample+"_"+histo1->GetName(),canvX,canvY);
	//find max
	Float_t max = histo1->GetMaximum();
	if(histo2->GetMaximum() > max) max =  histo2->GetMaximum();
	histo1->SetMaximum(2*max);
	histo1->SetMinimum(0.);
	if(doRatio){
		TPad *pad2 = new TPad("pad2","",0,0,1,0.3);
		setsubPadStyle(pad2);
		pad2->SetGrid();
		pad2->Draw();
		pad2->cd();
		TH1F *h_ratio = (TH1F*) histo1->Clone();
		h_ratio->Divide(histo2);
        h_ratio->SetLineStyle(1);
        h_ratio->SetMarkerStyle(20);
        h_ratio->SetLineColor(kBlack);
        h_ratio->SetMarkerColor(kBlack);
        h_ratio->SetMarkerSize(0.8); //1.2
		h_ratio->SetTitleSize(0.14,"x"); //0.12
		h_ratio->SetTitleSize(0.14,"y");
		h_ratio->SetTitleOffset(0.45,"y");
		h_ratio->SetLabelSize(0.12,"x");
		h_ratio->SetLabelSize(0.12,"y");
        h_ratio->SetTitleOffset(1.3,"x");
		h_ratio->SetMaximum(1.6);
		h_ratio->SetMinimum(0.4);
		h_ratio->Draw("E");
		h_ratio->GetYaxis()->SetTitle(ratio_name);
		h_ratio->GetXaxis()->SetTitle(var_nameX);
		h_ratio->SetTickLength(0.04,"y");
		h_ratio->SetTickLength(0.15,"x");

		canvas->cd();
		TPad *pad1 = new TPad("pad1","",0,0.3,1,1);
		setPadStyle(pad1);
		pad1->Draw();
		pad1->cd();
        histo1->SetLineStyle(1);
        histo1->Draw("histo E");
        histo2->Draw("histo same E");
        histo1->SetLabelSize(0.,"x");
        histo1->GetXaxis()->SetTitle(var_nameX);
        histo1->GetYaxis()->SetTitle(var_nameY);
	} else {

        histo1->Draw("histo E");
        histo2->Draw("histo same E");
        
        histo1->GetXaxis()->SetTitle(var_nameX);
        histo1->GetYaxis()->SetTitle(var_nameY);
	}
	//draw legend
	TLegend *leg = new TLegend(0.6,0.65,0.9,0.9);
	leg->SetBorderSize(0);
	leg->SetTextSize(0.045);//0.032
	leg->SetFillColor(0);
	leg->AddEntry(histo1," "+legend1+" "+sample,"l");
	leg->AddEntry(histo2," "+legend2+" "+sample,"l");
	leg->Draw();
	TLatex * lumi = new TLatex();
	lumi->SetNDC();
	lumi->SetTextFont(42);
	lumi->SetTextSize(0.04);
	lumi->SetTextColor(1);
	lumi->DrawLatex(0.22, 0.8, "#sqrt{s} = 8 TeV,  #int L dt = "+Lumi+" fb^{-1}");
	
    /*TLatex * chan = new TLatex();
	chan->SetNDC();
	chan->SetTextFont(42);
	chan->SetTextSize(0.04);
	chan->SetTextColor(1);
    
	if(channel=="ee") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW^{(*)} #rightarrow e#nue#nu + "+jet_bin);
	else if(channel=="mumu") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW^{(*)} #rightarrow e#nu#mu#nu + "+jet_bin);
	else if(channel=="emu") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW^{(*)} #rightarrow #mu#nue#nu + "+jet_bin);
	else if(channel=="mue") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW^{(*)} #rightarrow #mu#nu#mu#nu + "+jet_bin);
	else if(channel=="all") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW^{(*)} #rightarrow l#nul#nu + "+jet_bin);
	else if(channel=="emu_all") chan->DrawLatex(0.19, 0.73, "H #rightarrow WW^{(*)} #rightarrow e#nu#mu#nu/#mu#nue#nu + "+jet_bin);
     */
    
	//KS test
	double KS_value = histo1->KolmogorovTest(histo2);
	//if(isnan(KS_value)) KS_value = -999;
	TLatex *KS = new TLatex();
	KS->SetNDC();
	KS->SetTextFont(42);
	KS->SetTextSize(0.04);
	KS->SetTextColor(1);
    KS->DrawLatex(0.27, 0.64, Form("KS-test: %.2f",KS_value));
    
	if(doPrelim){
		TLatex * prelim = new TLatex();
		prelim->SetNDC();
		prelim->SetTextFont(42);
		prelim->SetTextColor(1);
		prelim->SetTextSize(0.05);
		prelim->DrawLatex(0.24, 0.88, "#font[72]{ATLAS} Preliminary");
	} else {
		
		TLatex * prelim = new TLatex();
		prelim->SetNDC();
		prelim->SetTextFont(42);
		prelim->SetTextColor(1);
		prelim->SetTextSize(0.05);
		prelim->DrawLatex(0.26, 0.88, "#font[72]{ATLAS} Internal");
	}
    
	canvas->Print(outputdir+sample+"_"+histo1->GetName()+"_comp.eps");
	canvas->Print(outputdir+sample+"_"+histo1->GetName()+"_comp.pdf");
    canvas->Print(outputdir+sample+"_"+histo1->GetName()+"_comp.C");
    
}

void plot_comp3(TH1F* histo1, TH1F* histo2, TH1F* histo3, TString channel, TString jetbin, TString cut_name, TString sample, TString var_nameX,
                TString var_nameY, TString ratio_name, TString file1_name, TString file2_name, TString file3_name, TString outputdir) {
    
    setHSG3Style();
    
	TString jet_bin = "";
	if(jetbin=="0jet") jet_bin = "0 jet";
	if(jetbin=="1jet") jet_bin = "1 jet";
	if(jetbin=="2jet") jet_bin = "2 jet";
    
    Bool_t doPrelim = false;
    Bool_t doAtlas = false;
    Bool_t doRatio = false;
    Bool_t doNorm = true;
    TString Lumi = "20.7";
    Int_t canvX = 0;
    Int_t canvY = 0;
    if(doRatio) {canvX=800; canvY=800;}
    else  {canvX=800; canvY=600;}
    
	if(doNorm) {
		histo1->Scale(1/histo1->Integral());
		histo2->Scale(1/histo2->Integral());
		histo3->Scale(1/histo3->Integral());
	}
	setHistoStyle(histo1);
	setHistoStyle(histo2);
	setHistoStyle(histo3);
	histo1->SetLineColor(kRed);
	histo2->SetLineColor(kBlue);
	histo2->SetLineStyle(2);
	histo3->SetLineColor(kBlack);
	histo3->SetLineStyle(3);
    
	//sys histo
	TCanvas *canvas = new TCanvas(sample+"_"+histo1->GetName(),sample+"_"+histo1->GetName(),canvX,canvY);
	//find max
	Float_t max = histo1->GetMaximum();
	if(histo2->GetMaximum() > max) max =  histo2->GetMaximum();
	if(histo3->GetMaximum() > max) max =  histo3->GetMaximum();
	histo1->SetMaximum(2*max);
	histo1->SetMinimum(0.);
	if(doRatio){
		TPad *pad2 = new TPad("pad2","",0,0,1,0.3);
		setsubPadStyle(pad2);
		pad2->SetGrid();
		pad2->Draw();
		pad2->cd();
		TH1F *h_ratio = (TH1F*) histo2->Clone();
		h_ratio->Divide(histo1);
		TH1F *h_ratio2 = (TH1F*) histo3->Clone();
		h_ratio2->Divide(histo1);
        
        //h_ratio->SetMarkerStyle(20);
        //h_ratio->SetMarkerColor(kBlack);
        //h_ratio->SetMarkerSize(0.8); //1.2
		h_ratio->SetTitleSize(0.15,"x");
		h_ratio->SetTitleSize(0.12,"y");
		h_ratio->SetTitleOffset(0.45,"y");
		h_ratio->SetLabelSize(0.17,"x");
		h_ratio->SetLabelSize(0.17,"y");
		h_ratio->SetMaximum(1.5);
		h_ratio->SetMinimum(0.5);
		h_ratio->Draw("E");
		h_ratio2->Draw("E same");
        
		h_ratio->GetYaxis()->SetTitle(ratio_name);
		h_ratio->GetXaxis()->SetTitle(var_nameX);
		h_ratio->SetTickLength(0.04,"y");
		h_ratio->SetTickLength(0.15,"x");
		canvas->cd();
		TPad *pad1 = new TPad("pad1","",0,0.3,1,1);
		setPadStyle(pad1);
		pad1->Draw();
		pad1->cd();
        histo1->Draw("histo");
        histo2->Draw("histo same");
        histo3->Draw("histo same");
        histo1->SetLabelSize(0.,"x");
        histo1->GetXaxis()->SetTitle(var_nameX);
        histo1->GetYaxis()->SetTitle(var_nameY);
	} else {
        
        histo1->Draw("histo");
        histo2->Draw("histo same");
        histo3->Draw("histo same");
        histo1->GetXaxis()->SetTitle(var_nameX);
        histo1->GetYaxis()->SetTitle(var_nameY);
	}
	//draw legend
	TLegend *leg = new TLegend(0.7,0.7,0.92,0.91);
	leg->SetBorderSize(0);
	leg->SetTextSize(0.05);
	leg->SetFillColor(0);
	leg->AddEntry(histo1," "+file1_name,"l");
	leg->AddEntry(histo2," "+file2_name,"l");
	leg->AddEntry(histo3," "+file3_name,"l");
    
	leg->Draw();
	TLatex * lumi = new TLatex();
	lumi->SetNDC();
	lumi->SetTextFont(42);
	lumi->SetTextSize(0.05);
	lumi->SetTextColor(1);
	//lumi->DrawLatex(0.22, 0.8, "#sqrt{s} = 8 TeV  #int L dt = "+Lumi+" fb^{-1}");
    lumi->DrawLatex(0.24, 0.8, "Simulation   #sqrt{s} = 8 TeV");
	TLatex * chan = new TLatex();
	chan->SetNDC();
	chan->SetTextFont(42);
	chan->SetTextSize(0.044);
	chan->SetTextColor(1);
	if(channel=="ee") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW* #rightarrow e#nue#nu + "+jet_bin + "s");
	else if(channel=="mumu") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW* #rightarrow e#nu#mu#nu + "+jet_bin + "s");
	else if(channel=="emu") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW* #rightarrow #mu#nue#nu + "+jet_bin + "s");
	else if(channel=="mue") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW* #rightarrow #mu#nu#mu#nu + "+jet_bin + "s");
	else if(channel=="all") chan->DrawLatex(0.21, 0.73, "H #rightarrow WW* #rightarrow l#nul#nu + "+jet_bin + "s");
	else if(channel=="emu_all") chan->DrawLatex(0.22, 0.73, "H #rightarrow WW* #rightarrow e#nu#mu#nu/#mu#nue#nu + "+jet_bin + "s");
	//KS test
	/* double KS_value = histo1->KolmogorovTest(histo2); */
    
	//if(isnan(KS_value)) KS_value = -999;
	/* TLatex *KS = new TLatex(); */
	/* KS->SetNDC(); */
	/* KS->SetTextFont(42); */
	/* KS->SetTextSize(0.05); */
	/* KS->SetTextColor(1); */
    /* KS->DrawLatex(0.27, 0.64, Form("KS-test: %.2f",KS_value)); */
    
	TLatex * prelim = new TLatex();
	prelim->SetNDC();
	prelim->SetTextFont(42);
	prelim->SetTextColor(1);
	prelim->SetTextSize(0.05);
	if(doPrelim) prelim->DrawLatex(0.26, 0.88, "#font[72]{ATLAS} Preliminary");
	else if(doAtlas) prelim->DrawLatex(0.26, 0.88, "#font[72]{ATLAS}");
	else prelim->DrawLatex(0.26, 0.88, "#font[72]{ATLAS} Internal");
    
	canvas->Print(outputdir+sample+"_"+histo1->GetName()+"_comp2.eps");
	canvas->Print(outputdir+sample+"_"+histo1->GetName()+"_comp2.pdf");
    
}
