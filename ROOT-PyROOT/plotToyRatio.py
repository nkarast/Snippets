import ROOT as rt
import math

debug = 1

input_file = open("toy_binContent.txt","read")
rt.gStyle.SetOptStat(0)

        
rt.gStyle.SetFillColor(10)
rt.gStyle.SetFrameFillColor(10)
rt.gStyle.SetCanvasColor(10)
rt.gStyle.SetPadColor(10)
rt.gStyle.SetTitleFillColor(0)
rt.gStyle.SetStatColor(10)
                                
rt.gStyle.SetCanvasBorderMode(0)
rt.gStyle.SetFrameBorderMode(0)
rt.gStyle.SetPadBorderMode(0)
rt.gStyle.SetDrawBorder(0)
rt.gStyle.SetTitleBorderSize(0)
                                                    
rt.gStyle.SetFuncWidth(2)
rt.gStyle.SetHistLineWidth(2)
rt.gStyle.SetFuncColor(2)
                                                                
rt.gStyle.SetPadTopMargin(0.05)
rt.gStyle.SetPadBottomMargin(0.16)
rt.gStyle.SetPadLeftMargin(0.12)
rt.gStyle.SetPadRightMargin(0.05)
                                                                                
rt.gStyle.SetPadTickX(1)
rt.gStyle.SetPadTickY(1)
                                                                                        
rt.gStyle.SetFrameLineWidth(1)
rt.gStyle.SetLineWidth(1)


#some holders here....
data = []
asimov = []
toy1 = []
toy2 = []
toy3 = []
toy4 = []
toy5 = []
toy6 = []
toy7 = []
toy8 = []
toy9 = []
toy10 = []

data_error = []
asimov_error = []
asimov_perc_error = []
toy1_error = []
toy2_error = []
toy3_error = []
toy4_error = []
toy5_error = []
toy6_error = []
toy7_error = []
toy8_error = []
toy9_error = []
toy10_error = []


# read the file and fill the lists with the bin content
i=0
for line in input_file.readlines():
    linekeeper = line.split()
    if linekeeper[0]=='---' : continue
    if linekeeper[0] == "DATA:" :
        data.append(float(linekeeper[4]))
    elif linekeeper[0] == "ASIMOV:" :
        asimov.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA:" :
        toy1.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA2:" :
        toy2.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA3:" :
        toy3.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA4:" :
        toy4.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA5:" :
        toy5.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA6:" :
        toy6.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA7:" :
        toy7.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA8:" :
        toy8.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA9:" :
        toy9.append(float(linekeeper[4]))
    elif linekeeper[0] == "TOYDATA10:" :
        toy10.append(float(linekeeper[4]))

# calculate the error of each bin as sqrt(N)
for i in range(len(data)):
    data_error.append(math.sqrt(data[i]))
    asimov_error.append(math.sqrt(asimov[i]))
    asimov_perc_error.append((asimov_error[i]/asimov[i])*100.)
    toy1_error.append(math.sqrt(toy1[i]))
    toy2_error.append(math.sqrt(toy2[i]))
    toy3_error.append(math.sqrt(toy3[i]))
    toy4_error.append(math.sqrt(toy4[i]))
    toy5_error.append(math.sqrt(toy5[i]))
    toy6_error.append(math.sqrt(toy6[i]))
    toy7_error.append(math.sqrt(toy7[i]))
    toy8_error.append(math.sqrt(toy8[i]))
    toy9_error.append(math.sqrt(toy9[i]))
    toy10_error.append(math.sqrt(toy10[i]))

if debug:
    print ' data = ', data
    print ' data_error = ', data_error, '\n'

    print ' asimov = ', asimov
    print ' asimov_error = ', asimov_error, '\n'

    print ' toy1 = ', toy1
    print ' toy1_error = ', toy1_error, '\n'
    
    print ' toy2 = ', toy2
    print ' toy2_error = ', toy2_error, '\n'
    
    print ' toy3 = ', toy3
    print ' toy3_error = ', toy3_error, '\n'
    
    print ' toy4 = ', toy4
    print ' toy4_error = ', toy4_error, '\n'
    
    print ' toy5 = ', toy5
    print ' toy5_error = ', toy5_error, '\n'
    
    print ' toy6 = ', toy6
    print ' toy6_error = ', toy6_error, '\n'
    
    print ' toy7 = ', toy7
    print ' toy7_error = ', toy7_error, '\n'
    
    print ' toy8 = ', toy8
    print ' toy8_error = ', toy8_error, '\n'

    print ' toy9 = ', toy9
    print ' toy9_error = ', toy9_error, '\n'
    
    print ' toy10 = ', toy10
    print ' toy10_error = ', toy10_error, '\n'
    print ' length = ', len(toy10), len(toy10_error)

    print ' asimov percentage error : ', asimov_perc_error
    print ' max asimov error : ', max(asimov_perc_error)



# define the histograms
h_data = rt.TH1F("data","data",40, -1.,1.)
h_asimov = rt.TH1F("asimov","asimov",40, -1.,1.)
h_toy1 = rt.TH1F("toy21","toy21",40, -1.,1.)
h_toy2 = rt.TH1F("toy22","toy22",40, -1.,1.)
h_toy3 = rt.TH1F("toy23","toy23",40, -1.,1.)
h_toy4 = rt.TH1F("toy24","toy24",40, -1.,1.)
h_toy5 = rt.TH1F("toy25","toy25",40, -1.,1.)
h_toy6 = rt.TH1F("toy26","toy26",40, -1.,1.)
h_toy7 = rt.TH1F("toy27","toy27",40, -1.,1.)
h_toy8 = rt.TH1F("toy28","toy28",40, -1.,1.)
h_toy9 = rt.TH1F("toy29","toy29",40, -1.,1.)
h_toy10 = rt.TH1F("toy30","toy30",40, -1.,1.)

h_data.Sumw2()
h_asimov.Sumw2()
h_toy1.Sumw2()
h_toy2.Sumw2()
h_toy3.Sumw2()
h_toy4.Sumw2()
h_toy5.Sumw2()
h_toy6.Sumw2()
h_toy7.Sumw2()
h_toy8.Sumw2()
h_toy9.Sumw2()
h_toy10.Sumw2()

# set the bin content and error for each histo
for i in range(1, 41):
    h_data.SetBinContent(i, data[i-1])
    h_data.SetBinError(i, data_error[i-1])

    h_asimov.SetBinContent(i,asimov[i-1])
    h_asimov.SetBinError(i,asimov_error[i-1])

    h_toy1.SetBinContent(i,toy1[i-1])
    h_toy1.SetBinError(i,toy1_error[i-1])

    h_toy2.SetBinContent(i,toy2[i-1])
    h_toy2.SetBinError(i,toy2_error[i-1])

    h_toy3.SetBinContent(i,toy3[i-1])
    h_toy3.SetBinError(i,toy3_error[i-1])

    h_toy4.SetBinContent(i,toy4[i-1])
    h_toy4.SetBinError(i,toy4_error[i-1])

    h_toy5.SetBinContent(i,toy5[i-1])
    h_toy5.SetBinError(i,toy5_error[i-1])

    h_toy6.SetBinContent(i,toy6[i-1])
    h_toy6.SetBinError(i,toy6_error[i-1])

    h_toy7.SetBinContent(i,toy7[i-1])
    h_toy7.SetBinError(i,toy7_error[i-1])

    h_toy8.SetBinContent(i,toy8[i-1])
    h_toy8.SetBinError(i,toy8_error[i-1])

    h_toy9.SetBinContent(i,toy9[i-1])
    h_toy9.SetBinError(i,toy9_error[i-1])

    h_toy10.SetBinContent(i,toy10[i-1])
    h_toy10.SetBinError(i,toy10_error[i-1])



# make the ratio histograms and set their names
ratio_asimov = h_asimov.Clone()
ratio_asimov.Divide(h_asimov)
ratio_asimov.SetNameTitle("ratio_asimov","ratio_asimov")

ratio_asimov_2sigma = ratio_asimov.Clone()
for i in range(1,41):
    ratio_asimov_2sigma.SetBinContent(i, ratio_asimov.GetBinContent(i))
    ratio_asimov_2sigma.SetBinError(i, 2.*ratio_asimov.GetBinError(i))
ratio_asimov_2sigma.SetNameTitle("ratio_asimov_2sigma","ratio_asimov_2sigma")



ratio_toy1 = h_toy1.Clone()
ratio_toy1.Divide(h_asimov)
ratio_toy1.SetNameTitle("ratio_toy1","ratio_toy1")

ratio_toy2 = h_toy2.Clone()
ratio_toy2.Divide(h_asimov)
ratio_toy2.SetNameTitle("ratio_toy2","ratio_toy2")

ratio_toy3 = h_toy3.Clone()
ratio_toy3.Divide(h_asimov)
ratio_toy3.SetNameTitle("ratio_toy3","ratio_toy3")

ratio_toy4 = h_toy4.Clone()
ratio_toy4.Divide(h_asimov)
ratio_toy4.SetNameTitle("ratio_toy4","ratio_toy4")

ratio_toy5 = h_toy5.Clone()
ratio_toy5.Divide(h_asimov)
ratio_toy5.SetNameTitle("ratio_toy5","ratio_toy5")

ratio_toy6 = h_toy6.Clone()
ratio_toy6.Divide(h_asimov)
ratio_toy6.SetNameTitle("ratio_toy6","ratio_toy6")

ratio_toy7 = h_toy7.Clone()
ratio_toy7.Divide(h_asimov)
ratio_toy7.SetNameTitle("ratio_toy7","ratio_toy7")

ratio_toy8 = h_toy8.Clone()
ratio_toy8.Divide(h_asimov)
ratio_toy8.SetNameTitle("ratio_toy8","ratio_toy8")

ratio_toy9 = h_toy9.Clone()
ratio_toy9.Divide(h_asimov)
ratio_toy9.SetNameTitle("ratio_toy9","ratio_toy9")

ratio_toy10 = h_toy10.Clone()
ratio_toy10.Divide(h_asimov)
ratio_toy10.SetNameTitle("ratio_toy10","ratio_toy10")

# put some color in your life... (same color pattern as the likelihood scan)
ratio_asimov.SetLineColor(rt.kBlack)
ratio_asimov.SetFillColor(rt.kYellow-10)
#ratio_asimov.SetFillStyle(3001)

ratio_asimov_2sigma.SetLineColor(rt.kBlack)
ratio_asimov_2sigma.SetFillColor(rt.kGreen+1)
ratio_asimov_2sigma.SetFillStyle(3002)

ratio_toy1.SetLineColor(33)
ratio_toy1.SetMarkerStyle(20)
ratio_toy1.SetMarkerColor(33)

ratio_toy2.SetLineColor(28)
ratio_toy2.SetMarkerStyle(20)
ratio_toy2.SetMarkerColor(28)

ratio_toy3.SetLineColor(218)
ratio_toy3.SetMarkerStyle(20)
ratio_toy3.SetMarkerColor(218)

ratio_toy4.SetLineColor(227)
ratio_toy4.SetMarkerStyle(20)
ratio_toy4.SetMarkerColor(227)

ratio_toy5.SetLineColor(rt.kBlue-6)
ratio_toy5.SetMarkerStyle(20)
ratio_toy5.SetMarkerColor(rt.kBlue-6)

ratio_toy6.SetLineColor(222)
ratio_toy6.SetMarkerStyle(20)
ratio_toy6.SetMarkerColor(222)

ratio_toy7.SetLineColor(39)
ratio_toy7.SetMarkerStyle(20)
ratio_toy7.SetMarkerColor(39)

ratio_toy8.SetLineColor(rt.kPink)
ratio_toy8.SetMarkerStyle(20)
ratio_toy8.SetMarkerColor(rt.kPink)

ratio_toy9.SetLineColor(rt.kMagenta)
ratio_toy9.SetMarkerStyle(20)
ratio_toy9.SetMarkerColor(rt.kMagenta)

ratio_toy10.SetLineColor(rt.kGreen-4)
ratio_toy10.SetMarkerStyle(20)
ratio_toy10.SetMarkerColor(rt.kGreen-4)

# make a canvas and plot the ratio histograms
canvas = rt.TCanvas("ratio","ratio", 800,600)
canvas.cd()
ratio_asimov.SetTitle("")
ratio_asimov.GetYaxis().SetRangeUser(-1,6)
ratio_asimov.GetYaxis().SetTitle("Toy/Asimov")
ratio_asimov.GetXaxis().SetTitle("BDT Output")
ratio_asimov_2sigma.SetTitle("")
ratio_asimov_2sigma.GetYaxis().SetRangeUser(-1,6)
ratio_asimov_2sigma.GetYaxis().SetTitle("Toy / Asimov")
ratio_asimov_2sigma.GetYaxis().SetTitleSize(0.06)
ratio_asimov_2sigma.GetYaxis().SetTitleOffset(0.50)
ratio_asimov_2sigma.GetXaxis().SetTitle("Remapped BDT Output")
ratio_asimov_2sigma.GetXaxis().SetTitleSize(0.06)
ratio_asimov_2sigma.Draw("E4")
ratio_asimov.Draw("E4 same")
ratio_toy1.Draw("esame")
ratio_toy2.Draw("esame")
ratio_toy3.Draw("esame")
ratio_toy4.Draw("esame")
ratio_toy5.Draw("esame")
ratio_toy6.Draw("esame")
ratio_toy7.Draw("esame")
ratio_toy8.Draw("esame")
ratio_toy9.Draw("esame")
ratio_toy10.Draw("esame")
ratio_toy2.Draw("esame")

prelim = rt.TLatex()
prelim.SetNDC()
prelim.SetTextFont(42)
prelim.SetTextColor(1)
prelim.SetTextSize(0.06)
prelim.DrawLatex(0.19, 0.86, "#font[72]{ATLAS} Internal")
lumi = rt.TLatex()
lumi.SetNDC()
lumi.SetTextFont(42)
lumi.SetTextSize(0.04)
lumi.SetTextColor(1)
lumi.DrawLatex(0.17, 0.79, "#sqrt{s} = 8 TeV,  #int L dt = 20.3 fb^{-1}")

chan = rt.TLatex()
chan.SetNDC()
chan.SetTextFont(42)
chan.SetTextSize(0.04)
chan.SetTextColor(1)
chan.DrawLatex(0.16, 0.71, "H #rightarrow WW^{(*)} #rightarrow e#nu#mu#nu/#mu#nue#nu + 0 jets")

leg = rt.TLegend(0.62, 0.70, 0.94, 0.90)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.032)
leg.SetFillColor(0)
leg.SetNColumns(2)
leg.AddEntry(ratio_asimov," 1#sigma","f")
leg.AddEntry(ratio_asimov_2sigma," 2#sigma","f")
leg.AddEntry(ratio_toy1," toy21","lep")
leg.AddEntry(ratio_toy2," toy22","lep")
leg.AddEntry(ratio_toy3," toy23","lep")
leg.AddEntry(ratio_toy4," toy24","lep")
leg.AddEntry(ratio_toy5," toy25","lep")
leg.AddEntry(ratio_toy6," toy26","lep")
leg.AddEntry(ratio_toy7," toy27","lep")
leg.AddEntry(ratio_toy8," toy28","lep")
leg.AddEntry(ratio_toy9," toy29","lep")
leg.AddEntry(ratio_toy10," toy30","lep")
leg.Draw("same")

canvas.SaveAs("toys_over_asimov_2sigma_newToys_21_30.pdf")

# to be safe, save them in a root file too...
outfile = rt.TFile("ratio_toys_newToys_21_30.root","recreate")
outfile.cd()
h_asimov.Write()
h_data.Write()
h_toy1.Write()
h_toy2.Write()
h_toy3.Write()
h_toy4.Write()
h_toy5.Write()
h_toy6.Write()
h_toy7.Write()
h_toy8.Write()
h_toy9.Write()
h_toy10.Write()
ratio_asimov.Write()
ratio_toy1.Write()
ratio_toy2.Write()
ratio_toy3.Write()
ratio_toy4.Write()
ratio_toy5.Write()
ratio_toy6.Write()
ratio_toy7.Write()
ratio_toy8.Write()
ratio_toy9.Write()
ratio_toy10.Write()
outfile.Close()

