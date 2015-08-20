#include <iostream>
#include <iomanip>
#include <sstream>

#include "TFile.h"
#include "TCanvas.h"

#include "RooWorkspace.h"
#include "RooRealSumPdf.h"
#include "RooDataSet.h"
#include "RooAbsPdf.h"
#include "RooNLLVar.h"
#include "RooMinimizer.h"
#include "RooRealVar.h"
#include "RooFitResult.h"
#include "RooRandom.h"
#include "RooPlot.h"

#include "RooStats/ModelConfig.h"
#include "RooStats/AsymptoticCalculator.h"

using namespace std;
using namespace RooFit;
using namespace RooStats;

void plot_toys()
{
  TFile* f = new TFile("/project/atlas/users/tlenz/HWWStatisticsCode_v31/CPmix_kHWW2dot65m_0j_trainv31_v31_allsys_topLumi_toys.root");
  RooWorkspace* w = (RooWorkspace*)f->Get("combined");

  RooDataSet* data = (RooDataSet*)w->data("obsData");
  RooDataSet* toydata = (RooDataSet*)w->data("toyData");
  RooDataSet* toydata2 = (RooDataSet*)w->data("toyData4");
  RooDataSet* thisAsimovData = (RooDataSet*)w->data("asimivData_profiled_for_epsilon_0"); //asimivData_profiled_for_epsilon_0
  
  RooPlot* frame1 = w->var("obs_x_em_signalLike_0j_2012")->frame();
  //  RooPlot* frame2 = w->var("obs_x_em_mainControl_0j_2012")->frame();
  // RooPlot* frame3 = w->var("obs_x_em_zbox_0j_2012")->frame();
  
  data->plotOn(frame1, Name("data"), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  //data->plotOn(frame2, Name("data"), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  //data->plotOn(frame3, Name("data"), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));
  
  toydata->plotOn(frame1, Name("toy1"), LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  //toydata->plotOn(frame2, Name("toy1"), LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  //toydata->plotOn(frame3, Name("toy1"), LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));
  
  toydata2->plotOn(frame1, Name("toy4"), LineColor(kGreen), MarkerStyle(21), MarkerColor(kGreen), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  //toydata2->plotOn(frame2, Name("toy4"), LineColor(kGreen), MarkerStyle(21), MarkerColor(kGreen), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  //toydata2->plotOn(frame3, Name("toy4"), LineColor(kGreen), MarkerStyle(21), MarkerColor(kGreen), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));
  
  thisAsimovData->plotOn(frame1, Name("asimov"), LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  //thisAsimovData->plotOn(frame2, Name("asimov"), LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  //thisAsimovData->plotOn(frame3, Name("asimov"), LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));
  
  TCanvas* c = new TCanvas("c","c",1800,600);
  //c->Divide(3,1);
  
  /*c->cd(1);*/ /*gPad->SetLogy();*/ frame1->Draw();
  
  
  //c->cd(2); frame2->Draw();
  //draw legend
  TLegend *leg = new TLegend(0.48, 0.60, 0.84, 0.80, NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(62);
  leg->SetTextSize(0.04);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(1001);
  leg->SetNColumns(1);
  leg->AddEntry(frame1->findObject("data"),"data","pl");
  leg->AddEntry(frame1->findObject("toy1"),"toy1","pl");
  leg->AddEntry(frame1->findObject("toy4"),"toy4","pl");
  leg->AddEntry(frame1->findObject("asimov"),"asimov","pl");
	leg->Draw();
	//c->cd(3); frame3->Draw();
	c->Print("toys_linear.pdf");
}
