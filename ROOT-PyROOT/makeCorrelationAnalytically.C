#include <iostream>
#include <TH1F.h>
#include <TFile.h>
#include <TTree.h>
#include <TH1.h>
#include <TH2.h>
#include <TMath.h>
#include <vector>


using namespace std;

	
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


void getStatVariables(TString filename, TString varX, TString varY, Double_t &meanX, Double_t &meanY,  Double_t &stddevX, Double_t &stddevY, Double_t &sumw, Double_t &sumwx, Double_t &sumwy, Double_t &sumwxy, Double_t &covariance, Double_t &correlation, Double_t &correlationError, Int_t &eventsPassed, Int_t region){

  //
  // Int_t region defines :
  // 0 = doWWCR0j
  // 1 = doWWCR1j
  // 2 = doTopCR

  Bool_t doWWCR0j = false;
  Bool_t doWWCR1j = false;
  Bool_t doTopCR  = false;
  
  Double_t n_good_events = 0;
  Double_t sumw_temp = 0;
  Double_t sumwx_temp = 0;
  Double_t sumwy_temp = 0;
  Double_t sumwxy_temp = 0;

  Double_t stdevXnom = 0;
  Double_t stdevYnom = 0;
  
  vector<Float_t> varX_vec;
  vector<Float_t> varY_vec;
  vector<Double_t> weight_vec;
  

  if(region==0) doWWCR0j = true;
  else if(region==1) doWWCR1j = true;
  else if (region==2) doTopCR = true;
  else {
    cout << "getStatVariables: Fatal Error - Non well defined region [0,2]. Exiting..." << endl;
    // return -1;
  }
  
  Double_t EventWeight;
  Float_t Mll, DPhill, Ptll, Mtt_TrackHWW_Clj, MT_TrackHWW_Clj, lepPt0, lepPt1, lepID0, lepID1;
  Int_t nBJets, m_jet_n,m_mu_n, isBlinded, m_el_n;

  TFile *fin = TFile::Open(filename);
  TTree *tin = (TTree*) fin->Get("MVATree");
  
  tin->SetBranchAddress("Mll", &Mll);
  tin->SetBranchAddress("DPhill", &DPhill);
  tin->SetBranchAddress("Ptll", &Ptll);
  tin->SetBranchAddress("nbt", &nBJets);
  tin->SetBranchAddress("MT_TrackHWW_Clj", &MT_TrackHWW_Clj);
  tin->SetBranchAddress("m_jet_n", &m_jet_n);
  tin->SetBranchAddress("m_mu_n", &m_mu_n);
  tin->SetBranchAddress("m_el_n", &m_el_n);
  tin->SetBranchAddress("lepPt0", &lepPt0);
  tin->SetBranchAddress("lepPt1", &lepPt1);
  tin->SetBranchAddress("isBlinded", &isBlinded);
  tin->SetBranchAddress("EventWeight", &EventWeight);
  tin->SetBranchAddress("lepID0", &lepID0);
  tin->SetBranchAddress("lepID1", &lepID1);
  tin->SetBranchAddress("Mtt_TrackHWW_Clj", &Mtt_TrackHWW_Clj);
  
  Long64_t nentries = tin->GetEntries();
	
  Double_t nf_sf_0j=1.;
  Double_t nf_sf_1j=1.;
  
  //Zjets SFs v29
  if( filename.Contains("zjets") ){
    cout << "using nf for zj"<< endl; 
    nf_sf_0j = 1.02;
    nf_sf_1j = 1.3;
  }
  //WW SFs v29
  if( filename.Contains("ww") ){
    cout << "using nf for ww"<< endl; 
    nf_sf_0j = 1.17;
    nf_sf_1j = 1.0;
  }
  //top SFs v29
  if( filename.Contains("ttbar") || filename.Contains("st")) {
    cout << "using nf for top"<< endl; 
    nf_sf_0j = 1.06;
    nf_sf_1j = 1.0;
  }
  
  
  for(Long64_t jentry=0; jentry<nentries; jentry++){
    tin->GetEntry(jentry);
    if(jentry<3) cout << jentry << endl;
    
    Double_t nf_sf=1.;
	  
    //cout << "before cuts :: dphill " << DPhill << endl;
    //-----
    
    bool good_event = true;
    
    /*
      bool emu = false;
      if(lepPt0 > lepPt1) {
      if(fabs(lepID0) == 11) emu = true;
      } else {
      if(fabs(lepID1) == 11) emu = true;
      }
      if (channel[chan_i]=="emu"  && !(m_mu_n==1 && m_el_n==1 && emu) ) good_event = false;
      if (channel[chan_i]=="mue"  && !(m_mu_n==1 && m_el_n==1 && !emu) ) good_event = false;
    */
    
    // cutting for emu_all only
    if (!(m_mu_n==1 && m_el_n==1) ) good_event = false;
    
    // blinding criteria
    if(isBlinded) good_event=false;
    
    
    // Low Pt cuts
    if(!(lepPt0>22000 || lepPt1>22000)) good_event = false;
    if(!(lepPt0>15000 && lepPt1>15000)) good_event = false;
    
    // OS cut
    if(lepID0*lepID1 > 0)  good_event = false;
    
    // cutting for 0 jet
        if(region==0) {if(m_jet_n!=0)  good_event = false;}
	else { if(m_jet_n!=1)  good_event = false; }
    
    
    
    if(doTopCR) {
      if(m_jet_n==0)  good_event = false;
      if(nBJets==0)  good_event = false;
      if(Mtt_TrackHWW_Clj > 0. && TMath::Abs(Mtt_TrackHWW_Clj - 91187.6) <= 25000.) good_event = false;
    }
    else if(doWWCR0j || doWWCR1j) {
      if(m_jet_n==0) {
	if(Ptll < 20000) good_event = false;
	if((Mll<80000 || Mll>150000)) good_event = false;
      } else if(m_jet_n==1) {
	if(Mtt_TrackHWW_Clj > 0. && TMath::Abs(Mtt_TrackHWW_Clj - 91187.6) <= 25000.) good_event = false;
	if(nBJets!=0)  good_event = false;
	if(Mll<80000) good_event = false;
      }
      
    }else { //SR
      if(m_jet_n==0) {
	if(Ptll <= 20000) good_event = false;
      } else if(m_jet_n==1) {
	if(nBJets!=0)  good_event = false;
	if(Mtt_TrackHWW_Clj > 66187.6) good_event = false; 
      }
      if(Mll>80000) good_event = false; 
      if(DPhill>2.8) good_event=false;
      //if(HPt > HPtCut) good_event=false;
    }
    
    if(good_event){
      n_good_events++;

      if(m_jet_n==0) nf_sf = nf_sf_0j;
      else if(m_jet_n==1) nf_sf = nf_sf_1j;
      
      //  EventWeight = nf_sf*EventWeight;

      weight_vec.push_back(EventWeight);

      if(varX.Contains("Mll")) varX_vec.push_back(Mll/1000.);
      else if(varX.Contains("Ptll")) varX_vec.push_back(Ptll/1000.);
      else if(varX.Contains("MT")) varX_vec.push_back(MT_TrackHWW_Clj/1000.);
      else if(varX.Contains("DPhill")) varX_vec.push_back(DPhill);

    

      if(varY.Contains("Mll")) varY_vec.push_back(Mll/1000.);
      else if(varY.Contains("Ptll")) varY_vec.push_back(Ptll/1000.);
      else if(varY.Contains("MT")) varY_vec.push_back(MT_TrackHWW_Clj/1000.);
      else if(varY.Contains("DPhill")) varY_vec.push_back(DPhill);

      //cout << varX_vec.at(0) << "\t" << varY_vec.at(0) << "\t" << weight_vec.size()<< endl;


    }else continue;

  }// for loop

  // Getting stats 
  for(UInt_t i=0; i<varX_vec.size(); i++){
    sumw_temp += weight_vec.at(i);
    sumwx_temp += weight_vec.at(i)*varX_vec.at(i);
    sumwy_temp += weight_vec.at(i)*varY_vec.at(i);
    sumwxy_temp += weight_vec.at(i)*varX_vec.at(i)*varY_vec.at(i);
  }// for varX size

  // getting sumw's
  sumw = sumw_temp;
  sumwx = sumwx_temp;
  sumwy = sumwy_temp;
  sumwxy = sumwxy_temp;
  

  // getting stddev
  for(UInt_t i=0; i<varX_vec.size(); i++){
    stdevXnom += weight_vec.at(i)*(varX_vec.at(i) - sumwx/sumw)*(varX_vec.at(i) - sumwx/sumw);
    stdevYnom += weight_vec.at(i)*(varY_vec.at(i) - sumwy/sumw)*(varY_vec.at(i) - sumwy/sumw);
    
  }// for weight again

  stddevX = TMath::Sqrt(stdevXnom/sumw);
  stddevY = TMath::Sqrt(stdevYnom/sumw);

  // getting weighted mean
  meanX = sumwx/sumw;
  meanY = sumwy/sumw;


  // getting covariance(x,y)
  covariance  = (sumwxy/sumw - sumwx/sumw*sumwy/sumw);
  correlation = (sumwxy/sumw - sumwx/sumw*sumwy/sumw)/(stddevX*stddevY);
  correlationError = (1-correlation*correlation)/TMath::Sqrt(n_good_events);
  eventsPassed = n_good_events;



  // return 0;

}


void makeCorrelationAnalytically(){
  
  TString inputdir = "/data/atlas/users/nikosk/HWWMVACode/higgs_tmvapp/higgs_tmvapp_4var_spin0vBgr_spin2pvBgr_allinputs_ptllmll_v00-02-29_lead22sublead15_met20_20_njet_85btag_dphillCut/H125/Nominal/Normal/";

  Bool_t doWWCR0j = false;
  Bool_t doWWCR1j = false;
  Bool_t doTopCR = true;

  Int_t region = -1;
  if(doWWCR0j) region = 0;
  else if(doWWCR1j) region = 1;
  else if(doTopCR) region = 2;


  Int_t sampN = 12;
  TString samples[sampN];
  samples[0] = "dataUnblind";
  samples[1] = "st";
  samples[2] = "ttbar";
  samples[3] = "wg";
  samples[4] = "wgs";
  samples[5] = "wjets";
  samples[6] = "ww";
  samples[7] = "wzzz";
  samples[8] = "zjets";
  samples[9] = "ggf125";
  samples[10]= "ggH125spin2p";
  samples[11]="allbackgrounds";

  Int_t varN=4;
  TString variable[varN];
  variable[0] = "Mll";
  variable[1] = "DPhill";
  variable[2] = "Ptll";
  variable[3] = "MT_TrackHWW";

  TString jetbin = "_1jet";
  TString chan = "_emu_all";


  for(Int_t samp_i = 0; samp_i<sampN; samp_i++){
    TString outputname = "CorrelationOutput/"+samples[samp_i]+"_correlationHists_TopCR1j.root";
    TFile *fout = new TFile(outputname, "RECREATE");

    
    vector<Float_t> mll_vec;
    vector<Float_t> dphill_vec;
    vector<Float_t> mt_vec;
    vector<Float_t> ptll_vec;
    vector<Double_t> weight_vec;
       

    for(Int_t var_i = 0; var_i<varN; var_i++){
      for(Int_t var_j = 0; var_j<varN; var_j++){
	if(var_i==var_j) continue;
	
	Int_t n_good_events = 0;
	
	cout << "########################   START    #########################" << endl;
	cout << "@ makeCorrelations : Making correlation coefficient calculation for "<< samples[samp_i] << " & for " << variable[var_i] << ".vs."<< variable[var_j] << endl;


	// Load the histogram files to get Mean/RMS
	/*	TString hist_addname = "_WWCR0j_v2_hist.root";

	TString hist_filename = inputdir+samples[samp_i]+hist_addname;
	TFile *f1 = TFile::Open(hist_filename);
	
	TString var_i_name = variable[var_i]+jetbin+chan;
	TString var_j_name = variable[var_j]+jetbin+chan;
	
	TH1F *hist_i = (TH1F*) f1->Get(var_i_name);
	TH1F *hist_j = (TH1F*) f1->Get(var_j_name);
	
	// These values are in GeV, while in ntuple on MeV
	Double_t mean_i, mean_j;
	Double_t rms_i, rms_j;
	Double_t stddev_i, stddev_j;
	
	mean_i   = hist_i->GetMean();
	rms_i    = hist_i->GetRMS();
	stddev_i = rms_i;  // for 1d histo rms == stdev 
	
	mean_j   = hist_j->GetMean();
	rms_j    = hist_j->GetRMS();
	stddev_j = rms_j;  // for 1d histo rms == stdev 
	
	f1->Close();
	delete f1;
	
	cout << "(mean,rms 1),(mean,rms 2) = " << mean_i << "\t" << rms_i <<"\t" << mean_j <<"\t" << rms_j<< endl;
	
	*/	

	TString ntuple_addname = ".root";
	TString ntuple_filename = inputdir+samples[samp_i]+ntuple_addname;
	TFile *f2 = TFile::Open(ntuple_filename);
	TTree *tin = (TTree*) f2->Get("MVATree");
	
	Double_t sumw, sumwx, sumwy, sumwxy, meanX, meanY, stddevX, stddevY, covariance, correlation, correlationError;
	Int_t eventsPassed;

	
	cout << "Getting Stats for region " << region << endl;
	getStatVariables(ntuple_filename, variable[var_i], variable[var_j], meanX, meanY,  stddevX, stddevY, sumw, sumwx, sumwy, sumwxy, covariance, correlation, correlationError, eventsPassed, region);
	  cout << " ----- getStatVariables Output ---- " << endl;
	  cout << "w.meanX ["<<variable[var_i]<<"] = " << meanX << endl;
	  cout << "w.meanY ["<<variable[var_j]<<"] = " << meanY << endl;
	  cout << "stddevX ["<<variable[var_i]<<"] = " << stddevX << endl;
	  cout << "stddevY ["<<variable[var_j]<<"] = " << stddevY << endl;
	  cout << "sumw = " << sumw << endl;
	  cout << "sumwx ["<<variable[var_i]<<"] = " << sumwx << endl;
	  cout << "sumwy ["<<variable[var_j]<<"] = " << sumwy << endl;
	  cout << "sumwxy ["<<variable[var_i]<<","<<variable[var_j]<< "] = " << sumwxy << endl;
	  cout << "Cov(X,Y) = \t" << covariance << endl;
	  cout << "r(X,Y) +/- dr = \t" << correlation << " +/-  " << correlationError << endl;
	  cout << "Events passed all cuts = " << eventsPassed << endl;
	  cout << "---------------------------------------------------------------------------" << endl;
	  



	
  

	
	Double_t EventWeight;
	Float_t Mll, DPhill, Ptll, Mtt_TrackHWW_Clj, MT_TrackHWW_Clj, lepPt0, lepPt1, lepID0, lepID1;
	Int_t nBJets, m_jet_n,m_mu_n, isBlinded, m_el_n;
	
	TString corr_histname, title_addname;
	if(doWWCR0j) title_addname="_WWCR0j";
	if(doWWCR1j) title_addname="_WWCR1j";
	if(doTopCR) title_addname="_TopCR";
	corr_histname = "correlation_"+variable[var_i]+"_"+variable[var_j]+title_addname+jetbin+chan;
	
	TH1F *h_corr = new TH1F(corr_histname,corr_histname , 20, -4, 4);
	h_corr->Sumw2();

	tin->SetBranchAddress("Mll", &Mll);
	tin->SetBranchAddress("DPhill", &DPhill);
	tin->SetBranchAddress("Ptll", &Ptll);
	tin->SetBranchAddress("nbt", &nBJets);
	tin->SetBranchAddress("MT_TrackHWW_Clj", &MT_TrackHWW_Clj);
	tin->SetBranchAddress("m_jet_n", &m_jet_n);
	tin->SetBranchAddress("m_mu_n", &m_mu_n);
	tin->SetBranchAddress("m_el_n", &m_el_n);
	tin->SetBranchAddress("lepPt0", &lepPt0);
	tin->SetBranchAddress("lepPt1", &lepPt1);
	tin->SetBranchAddress("isBlinded", &isBlinded);
	tin->SetBranchAddress("EventWeight", &EventWeight);
	tin->SetBranchAddress("lepID0", &lepID0);
	tin->SetBranchAddress("lepID1", &lepID1);
	tin->SetBranchAddress("Mtt_TrackHWW_Clj", &Mtt_TrackHWW_Clj);
	
	Long64_t nentries = tin->GetEntries();
	

	//Double_t sumw = 0;
	//Double_t sumwmll =0;

	Double_t nf_sf_0j=1.;
	Double_t nf_sf_1j=1.;
	//if(samples[samp_i]=="ww" && doWWCR0j) nf_sf=1.17;
	//if(samples[samp_i]=="ww" && doWWCR1j) nf_sf=1.0;
	//if((samples[samp_i]=="ttbar" || samples[samp_i]=="st") && doTopCR) 
	
	//Zjets SFs v29
	if( (samples[samp_i]).Contains("zjets") ){
	  cout << "using nf for zj"<< endl; 
	  nf_sf_0j = 1.02;
	  nf_sf_1j = 1.3;
	}
	//WW SFs v29
	if( (samples[samp_i]).Contains("ww") ){
	  cout << "using nf for ww"<< endl; 
	  nf_sf_0j = 1.17;
	  nf_sf_1j = 1.0;
	}
	//top SFs v29
	if( (samples[samp_i]).Contains("ttbar") || (samples[samp_i]).Contains("st")) {
	  cout << "using nf for top"<< endl; 
	  nf_sf_0j = 1.06;
	  nf_sf_1j = 1.0;
	}
	
	
	
	Double_t corr;
	
	cout << "starting loop over " << nentries << " entries..." << endl;
	
	
	for(Long64_t jentry=0; jentry<nentries; jentry++){
	  tin->GetEntry(jentry);
	  if(jentry<3) cout << jentry << endl;
	  
	  Double_t nf_sf=1.;
	  
	  //cout << "before cuts :: dphill " << DPhill << endl;
	  //-----
	  
	  bool good_event = true;
	  
	  /*
	    bool emu = false;
	    if(lepPt0 > lepPt1) {
	    if(fabs(lepID0) == 11) emu = true;
	    } else {
	    if(fabs(lepID1) == 11) emu = true;
	    }
	    if (channel[chan_i]=="emu"  && !(m_mu_n==1 && m_el_n==1 && emu) ) good_event = false;
	    if (channel[chan_i]=="mue"  && !(m_mu_n==1 && m_el_n==1 && !emu) ) good_event = false;
	  */
	  
	  // cutting for emu_all only
	  if (!(m_mu_n==1 && m_el_n==1) ) good_event = false;
	  
	// blinding criteria
	  if(isBlinded) good_event=false;
	  
	  
	// Low Pt cuts
	if(!(lepPt0>22000 || lepPt1>22000)) good_event = false;
	if(!(lepPt0>15000 && lepPt1>15000)) good_event = false;
	
	// OS cut
	if(lepID0*lepID1 > 0)  good_event = false;
	
	// cutting for 0 jet
	if(doWWCR0j) {if(m_jet_n!=0)  good_event = false;}
	else {if(m_jet_n!=1)  good_event = false;}
	
       
	
	if(doTopCR) {
	  if(m_jet_n==0)  good_event = false;
	  if(nBJets==0)  good_event = false;
	  if(Mtt_TrackHWW_Clj > 0. && TMath::Abs(Mtt_TrackHWW_Clj - 91187.6) <= 25000.) good_event = false;
	}
	else if(doWWCR0j || doWWCR1j) {
	  if(m_jet_n==0) {
	    if(Ptll < 20000) good_event = false;
	    if((Mll<80000 || Mll>150000)) good_event = false;
	  } else if(m_jet_n==1) {
	    if(Mtt_TrackHWW_Clj > 0. && TMath::Abs(Mtt_TrackHWW_Clj - 91187.6) <= 25000.) good_event = false;
	    if(nBJets!=0)  good_event = false;
	    if(Mll<80000) good_event = false;
	  }
	  
	}else { //SR
	  if(m_jet_n==0) {
	    if(Ptll <= 20000) good_event = false;
	  } else if(m_jet_n==1) {
	    if(nBJets!=0)  good_event = false;
	    if(Mtt_TrackHWW_Clj > 66187.6) good_event = false; 
	  }
	  if(Mll>80000) good_event = false; 
	  if(DPhill>2.8) good_event=false;
	  //if(HPt > HPtCut) good_event=false;
	}
	
       
	
	if(good_event){
	  n_good_events++;

	  //sumw+=EventWeight;
	  //sumwmll+=(Mll/1000.)*EventWeight;

	  // mll_vec.push_back(Mll/1000.);
	  //ptll_vec.push_back(Ptll/1000.);
	  //mt_vec.push_back(MT_TrackHWW_Clj/1000.);
	  //dphill_vec.push_back(DPhill);
	  //weight_vec.push_back(EventWeight);
	  
	  if(m_jet_n==0) nf_sf = nf_sf_0j;
	  else if(m_jet_n==1) nf_sf = nf_sf_1j;
	  //else if(jet_i==2) nf_sf = nf_sf_2j;
	  

	  //cout << "found good event " << endl;
	  EventWeight = nf_sf*EventWeight;

	  // cout <<"Before Multiplication: \t" << Mll << "\t" << DPhill << "\t" << EventWeight << endl;
	  Mll = (Mll/1000.);
	  DPhill = DPhill;
	  Ptll = (Ptll/1000.);
	  MT_TrackHWW_Clj = MT_TrackHWW_Clj/1000.;
	  
	  //cout <<"After Multiplication: \t" << Mll << "\t" << DPhill << endl;
	  Double_t corr_num = -999.;
	  Double_t corr_denom = stddevX*stddevY;
	  
	  if(variable[var_i].Contains("Mll") && variable[var_j].Contains("DPhill")){
	    corr_num = (Mll - meanX)*(DPhill-meanY);
	  }
	  else if(variable[var_i].Contains("DPhill") && variable[var_j].Contains("Mll")){
	    corr_num = (DPhill - meanX)*(Mll-meanY);
	  }
	  else if(variable[var_i].Contains("Mll") && variable[var_j].Contains("Ptll")){
	    corr_num = (Mll - meanX)*(Ptll-meanY);
	  }
	  else if(variable[var_i].Contains("Ptll") && variable[var_j].Contains("Mll")){
	    corr_num = (Ptll - meanX)*(Mll-meanY);
	  }
	  else if(variable[var_i].Contains("Mll") && variable[var_j].Contains("MT")){
	    corr_num = (Mll - meanX)*(MT_TrackHWW_Clj-meanY);
	  }
	  else if(variable[var_i].Contains("MT") && variable[var_j].Contains("Mll")){
	    corr_num = (MT_TrackHWW_Clj - meanX)*(Mll-meanY);
	  }
	  else if(variable[var_i].Contains("DPhill") && variable[var_j].Contains("Ptll")){
	    corr_num = (DPhill - meanX)*(Ptll-meanY);
	  }
	  else if(variable[var_i].Contains("Ptll") && variable[var_j].Contains("DPhill")){
	    corr_num = (Ptll - meanX)*(DPhill-meanY);
	  }
	  else if(variable[var_i].Contains("DPhill") && variable[var_j].Contains("MT")){
	    corr_num = (DPhill - meanX)*(MT_TrackHWW_Clj-meanY);
	  }
	  else if(variable[var_i].Contains("MT") && variable[var_j].Contains("DPhill")){
	    corr_num = (MT_TrackHWW_Clj - meanX)*(DPhill-meanY);
	  }
	  else if(variable[var_i].Contains("Ptll") && variable[var_j].Contains("MT")){
	    corr_num = (Ptll - meanX)*(MT_TrackHWW_Clj-meanY);
	  }
	   else if(variable[var_i].Contains("MT") && variable[var_j].Contains("Ptll")){
	    corr_num = (MT_TrackHWW_Clj - meanX)*(Ptll-meanY);
	  }


	  corr = corr_num/corr_denom;

	  h_corr->Fill(corr, EventWeight);


	}// good_event
	else continue;       
    }// for loop

	cout << "# good_events = " << n_good_events << endl;

	/*	Double_t nsumw=0;
	Double_t nsumwxy=0;
	Double_t nsumwx=0;
	Double_t nsumwy=0;
	Double_t nstdevX,nstde
	cout << "for mt ptll"<< endl;
	Double_t nstdevXnom =0;
	Double_t nstdevYnom=0;
	for(int i=0; i<mll_vec.size(); i++){
	  nsumw+=weight_vec.at(i);
	  nsumwx+=weight_vec.at(i)*mll_vec.at(i);
	  nsumwy+=weight_vec.at(i)*ptll_vec.at(i);
	  nsumwxy+=weight_vec.at(i)*mll_vec.at(i)*ptll_vec.at(i);
	  //	  nstdevXnom += weight_vec.at(i)
	 
	}//size vec

	//geting weighted mean for X, Y variables;
	Double_t weight_meanX = 0;
	Double_t weight_meanY = 0;
	for(int i=0; i<mll_vec.size(); i++){
	  nstdevXnom += weight_vec.at(i)*(mll_vec.at(i) - nsumwx/nsumw)*(mll_vec.at(i) - nsumwx/nsumw);
	  nstdevYnom += weight_vec.at(i)*(ptll_vec.at(i) - nsumwy/nsumw)*(ptll_vec.at(i) - nsumwy/nsumw);
	}

	nstdevX = TMath::Sqrt(nstdevXnom/nsumw);
	nstdevY = TMath::Sqrt(nstdevYnom/nsumw);

	cout << "StdDevX, StdDevY vs RMS_x, RMS_y = " << nstdevX << " , " << nstdevY << " vs " << rms_i << " , " << rms_j << endl;
	

	Double_t correlationFactor = (nsumwxy/nsumw - nsumwx/nsumw*nsumwy/nsumw)/(nstdevX*nstdevY);
	cout << "Correlation factor Calculated: " << correlationFactor << " +/- " << (1-correlationFactor*correlationFactor)/TMath::Sqrt(n_good_events)<< " (of n events = " << n_good_events << " ) " <<  endl;

	*/
	//cout << "Weighted Mean = " << sumwmll/sumw << endl;


    //000000   the code for 1 file ---- 00000     
    
	fout->cd();
	h_corr->Write();
	//zif(out2D)out2D->Write();
	//fout->Close();
	f2->Close();


      }// for var_j
  
      cout << "--------------   END  ---------------\n" << endl;
     
    }//for var_i

    fout->Close();
  
    
  }// for samp_i
  




    //drawOverflow(h_corr_mll_dphill);
  //  h_corr_mll_dphill->Draw();
  // cout << "h_corr_mll_dphill : (Mean, RMS) : (" << h_corr_mll_dphill->GetMean() << "," << h_corr_mll_dphill->GetRMS()<<")" << endl;
    
}// end of script


