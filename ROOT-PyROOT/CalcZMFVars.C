// TLorentzVectors that are already defined are 
//lepplus, lepmin which are positive/negative leptons,
//numin and nuplus are their corresponding neutrinos
// dilep = leplus+lepmins
// and met = numin+nuplus

Float_t LeadLepPt, SubLeadLepPt, Ptll, Mt, METRel, WplusM, WminM, phi3, theta1, theta3, cosThetaStar, Phi, Phi1, WoffShellM, WonShellM, cosTheta1, cosTheta2;
TLorentzVector lepplus, lepmin, dilep, nuplus, numin, met;
Float_t pie;
Float_t Mnunu, resyPt, resyPhi, resyEta, resyE, BDPhill, Psill, BPsill, DEtall;


void CalcZMFVars()
{
  
  if(lepplusPt>=lepminPt) {LeadLepPt = lepplusPt; SubLeadLepPt = lepminPt;}
  else {LeadLepPt = lepminPt; SubLeadLepPt = lepplusPt;}

  lepplus.SetPtEtaPhiE(lepplusPt,lepplusEta,lepplusPhi,lepplusE);
  lepmin.SetPtEtaPhiE(lepminPt,lepminEta,lepminPhi,lepminE);
  dilep = lepplus+lepmin;
  Ptll = dilep.Pt();

  nuplus.SetPtEtaPhiE(nuplusPt,nuplusEta,nuplusPhi,nuplusE);
  numin.SetPtEtaPhiE(numinPt,numinEta,numinPhi,numinE);
  met = nuplus + numin;

  Psill = fabs(lepmin.Angle(lepplus.Vect()));

  //ANGLES
  TLorentzVector H, Hr = dilep+met;
  H.SetPtEtaPhiE(yPt,yEta,yPhi,yE);

  TVector3 h_boost = -Hr.BoostVector();
  TLorentzVector Wmin = lepmin+numin;
  TLorentzVector Wplus = lepplus+nuplus;

  TLorentzVector Wmin_Hrest = Wmin;
  Wmin_Hrest.Boost(h_boost);
  TLorentzVector Wplus_Hrest = Wplus;
  Wplus_Hrest.Boost(h_boost);

  TLorentzVector lepplus_Hrest = lepplus;
  lepplus_Hrest.Boost(h_boost);
  TLorentzVector nuplus_Hrest = nuplus;
  nuplus_Hrest.Boost(h_boost);

  TLorentzVector lepmin_Hrest = lepmin;
  lepmin_Hrest.Boost(h_boost);
  TLorentzVector numin_Hrest = numin;
  numin_Hrest.Boost(h_boost);

  BDPhill = fabs(lepmin_Hrest.DeltaPhi(lepplus_Hrest));
  BPsill = fabs(lepmin_Hrest.Angle(lepplus_Hrest.Vect()));


  TVector3 Wp_boost = -Wplus.BoostVector();
  TVector3 Wm_boost = -Wmin.BoostVector();
  
  TVector3 zaxis(0,0,1);

  DEtall = fabs(lepminEta-lepplusEta);

  theta1 = nuplus_Hrest.Angle(Wplus_Hrest.Vect());
  theta3 = lepmin_Hrest.Angle(Wmin_Hrest.Vect());

  TVector3 planeplus = lepplus_Hrest.Vect().Cross(nuplus_Hrest.Vect());
  TVector3 planemin = lepmin_Hrest.Vect().Cross(numin_Hrest.Vect());

  phi3 = planemin.Angle(planeplus);
  phi3 = fabs(phi3);
  
  TLorentzVector q1,q2,q11,q12,q21,q22;
  TVector3 n1,n2,nsc;

  if(Wplus.M()>Wmin.M()) {
    q1 = Wplus;
    q2 = Wmin;
    q11= nuplus;
    q12= lepplus;
    q21= lepmin;
    q22= numin;
  
  }
  else {
    q1 = Wmin;
    q2 = Wplus;
    q11= lepmin;
    q12= numin;
    q21= nuplus;
    q22= lepplus;
  }

  WonShellM = q1.M();
  WoffShellM = q2.M();

  TVector3 q1_boost = -q1.BoostVector() ,q2_boost=-q2.BoostVector();

  TLorentzVector q1_Wr = q1, q2_Wr = q2, q11_Wr = q11, q21_Wr=q21;


  q1.Boost(h_boost);
  q2.Boost(h_boost);
  q11.Boost(h_boost);
  q12.Boost(h_boost);
  q21.Boost(h_boost);
  q22.Boost(h_boost);
  

  theta1=q11.Vect().Angle(q1.Vect());
  theta3=q21.Vect().Angle(q2.Vect());

  TVector3 q1hat(q1.Vect());

  cosThetaStar = q1hat.Unit().CosTheta();
  
  //planes
  n1 = q11.Vect().Cross(q12.Vect());
  n1 = n1.Unit();
  n2= q21.Vect().Cross(q22.Vect());
  n2 = n2.Unit();
  nsc = zaxis.Cross(q1.Vect());
  nsc = nsc.Unit();

  Phi = q1.Vect().Dot(n1.Cross(n2));
  Phi = Phi/fabs(Phi);
  Phi = Phi*acos(-n1.Dot(n2));

  Phi1 = q1.Vect().Dot(n1.Cross(nsc));
  Phi1 = Phi1/fabs(Phi1);
  Phi1 = Phi1*acos(n1.Dot(nsc));
  

 
  q2_Wr.Boost(q1_boost);
  q11_Wr.Boost(q1_boost);

  q1_Wr.Boost(q2_boost);
  q21_Wr.Boost(q2_boost);

  cosTheta1 = -(q2_Wr.Vect().Dot(q11_Wr.Vect()));
  cosTheta1 = cosTheta1/(q2_Wr.Vect().Mag()*q11_Wr.Vect().Mag());
 
  cosTheta2 = -(q1_Wr.Vect().Dot(q21_Wr.Vect()));
  cosTheta2 = cosTheta2/(q1_Wr.Vect().Mag()*q21_Wr.Vect().Mag());
 
  //END ANGLES


  TVector3 tmp=dilep.Vect() +met.Vect();
  Mt = sqrt( pow(dilep.Pt()+met.Pt(),2) - tmp.Mag2()  );


  Float_t dphimin = fabs(lepmin.DeltaPhi(met));
  if((lepplus.DeltaPhi(met))<dphimin) dphimin = fabs(lepplus.DeltaPhi(met));
  
  

  METRel = MET;
  if(dphimin<(pie/2.)) METRel = MET*sin(dphimin);

  WplusM = (lepplus+nuplus).M();
  WminM = (lepmin+numin).M();

  Mnunu = met.M();


  //DEBUG
  resyPt = H.Pt()-Hr.Pt();
  resyPhi = H.Phi()-Hr.Phi();
  resyEta = H.Eta()-Hr.Eta();
  resyE = H.E()-Hr.E();

}