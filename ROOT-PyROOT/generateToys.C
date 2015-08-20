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

void generateToys()
{
  // Setup
  ROOT::Math::MinimizerOptions::SetDefaultMinimizer("Minuit2");
  ROOT::Math::MinimizerOptions::SetDefaultStrategy(1);
  ROOT::Math::MinimizerOptions::SetDefaultPrintLevel(1);
  RooRandom::randomGenerator()->SetSeed(20141124);

  TFile f("CPmix_kHWW2dot65m_0j_trainv31_v31_allsys_topLumi/125.root");
  RooWorkspace* w = (RooWorkspace*)f.Get("combined");

  RooFIter iter = w->components().fwdIterator();
  RooAbsArg* arg;
  while ((arg = iter.next())) {
    if (arg->IsA() == RooRealSumPdf::Class()) {
      arg->setAttribute("BinnedLikelihood");
      cout << "Activating binned likelihood for " << arg->GetName() << endl;
    }
  }

  ModelConfig* mc = (ModelConfig*)w->obj("ModelConfig");
  RooDataSet* data = (RooDataSet*)w->data("obsData");
  RooArgSet obs = *mc->GetObservables();
  RooArgSet globs = *mc->GetGlobalObservables();
  RooArgSet nuis = *mc->GetNuisanceParameters();
  RooArgSet pois = *mc->GetParametersOfInterest();
  RooAbsPdf* pdf = mc->GetPdf();


  // Profile all parameters assuming epsilon == 0
  w->var("ATLAS_epsilon")->setVal(0.0);
  w->var("ATLAS_epsilon")->setConstant(1);

  cout << "\nGlobal Observables =====" << endl;
  globs.Print("v");
  cout << "\nNuisance Parameters =====" << endl;
  nuis.Print("v");
  cout << "\nParameters of Interest =====" << endl;
  pois.Print("v");

  RooNLLVar* nll = (RooNLLVar*)pdf->createNLL(*data, Constrain(nuis), GlobalObservables(globs), Offset(1));

  RooMinimizer minim(*nll);
  minim.setPrintLevel(1);
  minim.optimizeConst(2);
  minim.setStrategy(ROOT::Math::MinimizerOptions::DefaultStrategy());
  minim.setProfile(1);
  minim.setEps(1);
  minim.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());

  string name = Form("fitresult_%s_%s",pdf->GetName(),data->GetName());
  string title = Form("Result of fit of p.d.f. %s to dataset %s",pdf->GetName(),data->GetName());
  cout << "saving as " << name << endl;
  RooFitResult* r = minim.save(name.c_str(),title.c_str());

  r->Print("v");

  cout << "NLL after minimization " << setprecision(9) << nll->getVal() << endl;

  // Generate a few toy datasets and add them to the workspace
  RooDataSet* toydata = pdf->generate(obs,  Name("toyData"), Verbose(kTRUE), Extended());
  w->import(*toydata);

  // Generate and add a Asimov dataset generated from all parameters at their MLEs
  RooRealVar* poi = (RooRealVar*)pois.first();
  double poiVal = poi->getVal();
  stringstream ss;
  ss << poiVal;

  RooArgSet* genPoiValues = (RooArgSet*)pois.snapshot();
  RooArgSet*  allParams = mc->GetPdf()->getParameters(data);
  RooStats::RemoveConstantParameters(allParams);
  *allParams = *genPoiValues;
  RooArgSet genGlobs;

  cout << "\nGlobal Observables =====" << endl;
  globs.Print("v");
  cout << "\nNuisance Parameters =====" << endl;
  nuis.Print("v");
  cout << "\nParameters of Interest =====" << endl;
  pois.Print("v");

  RooAbsData* thisAsimovData = (RooAbsData*)RooStats::AsymptoticCalculator::MakeAsimovData(*mc, *allParams, genGlobs);
  thisAsimovData->SetName(("asimivData_profiled_for_epsilon_" + ss.str()).c_str());
  thisAsimovData->SetTitle(("Asimov data generated at the profiled values of the NPs for epsilon = " + ss.str()).c_str());
  w->import(*thisAsimovData);

  delete allParams;

  // Go back to nominal and validate Asimov data fit
  w->loadSnapshot("nominalNuis");
  w->loadSnapshot("nominalGlobs");

  cout << "\nGlobal Observables =====" << endl;
  globs.Print("v");
  cout << "\nNuisance Parameters =====" << endl;
  nuis.Print("v");
  cout << "\nParameters of Interest =====" << endl;
  pois.Print("v");

  RooNLLVar* nll_asi = (RooNLLVar*)pdf->createNLL(*thisAsimovData, Constrain(nuis), GlobalObservables(globs), Offset(1));

  RooMinimizer minim_asi(*nll_asi);
  minim_asi.setPrintLevel(1);
  minim_asi.optimizeConst(2);
  minim_asi.setStrategy(ROOT::Math::MinimizerOptions::DefaultStrategy());
  minim_asi.setProfile(1);
  minim_asi.setEps(1);
  minim_asi.minimize(ROOT::Math::MinimizerOptions::DefaultMinimizerType().c_str(), ROOT::Math::MinimizerOptions::DefaultMinimizerAlgo().c_str());

  string name_asi = Form("fitresult_%s_%s",pdf->GetName(),thisAsimovData->GetName());
  string title_asi = Form("Result of fit of p.d.f. %s to dataset %s",pdf->GetName(),thisAsimovData->GetName());
  cout << "saving as " << name_asi << endl;
  RooFitResult* r_asi = minim_asi.save(name_asi.c_str(),title_asi.c_str());

  r_asi->Print("v");

  cout << "Asimov NLL after minimization " << setprecision(9) << nll_asi->getVal() << endl;

  // Go back to nominal and save workspace with added Asimov data and toy data
  w->loadSnapshot("nominalNuis");
  w->loadSnapshot("nominalGlobs");

  w->writeToFile("test.root");

  // Plot data, toy data and Asimov data

  RooPlot* frame1 = w->var("obs_x_em_signalLike_0j_2012")->frame();
  RooPlot* frame2 = w->var("obs_x_em_mainControl_0j_2012")->frame();
  RooPlot* frame3 = w->var("obs_x_em_zbox_0j_2012")->frame();


  data->plotOn(frame1, DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  data->plotOn(frame2, DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  data->plotOn(frame3, DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));

  toydata->plotOn(frame1, LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  toydata->plotOn(frame2, LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  toydata->plotOn(frame3, LineColor(kRed), MarkerStyle(21), MarkerColor(kRed), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));

  thisAsimovData->plotOn(frame1, LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_signalLike_0j_2012"));
  thisAsimovData->plotOn(frame2, LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_mainControl_0j_2012"));
  thisAsimovData->plotOn(frame3, LineColor(kBlue), MarkerStyle(22), MarkerColor(kBlue), DataError(RooAbsData::Poisson), Cut("merged_cat==merged_cat::em_zbox_0j_2012"));

  TCanvas* c = new TCanvas("c","c",900,300);
  c->Divide(3,1);

  c->cd(1);  gPad->SetLogy(); frame1->Draw();
  c->cd(2); frame2->Draw();
  c->cd(3); frame3->Draw();

}
