import ROOT
from mymodule import *
from ROOT import SetOwnership

## definition of main funciton
def main():
	## initialise logger
	init_logger()


	## configuration
	filelist_A = ["../plots/plots_uMSim_45degBeam_QGSP_BERT_200M_5dot1MeV/plots_uMSim_45degBeam_QGSP_BERT_200M_5dot1MeV.root"]
	filelist_B = ["../plots/plots_uMSim_45degBeam_QGSP_BERT_RadioactiveDecays_200M_5dot1MeV/uMSim_45degBeam_QGSP_BERT_RadioactiveDecays_200M_5dot1MeV.root"]
	distributions_list_A = ["total_energy", "ioni_energy", "elastic_energy", "inelastic_energy"]
	distributions_list_B = distributions_list_A # if same names else []
	labelsX = ["Total Energy Deposited [keV]", "Ionisation Energy Deposited [keV]", "Elastic Energy Deposited [keV]", "Inelastic Energy Deposited [keV]"]
	outdir = "../plots/compQGSP_Radioactive/"
	outNames = [outdir+"comp_totalEnergy.pdf",outdir+"comp_ionisationEnergy.pdf", outdir+"comp_elasticEnergy.pdf", outdir+"comp_inelasticEnergy.pdf"]
	colors = [ROOT.kRed, ROOT.kBlue]
	doRatio = True
	
	######################################################



	## Check if files do exist
	for fileA,fileB in zip(filelist_A,filelist_B):
		missing = False
		if not (checkFileExist(fileA)): fatal("Missing file: %s" % fileA); missing=True
		if not (checkFileExist(fileA)): fatal("Missing file: %s" % fileB); missing=True
		if missing: return
			


	for filenameA,filenameB in zip(filelist_A,filelist_B):
		for distroA,distroB,label,outName in zip(distributions_list_A,distributions_list_B,labelsX,outNames):
			fileA = ROOT.TFile.Open(filenameA,'READ')
			fileB = ROOT.TFile.Open(filenameB,'READ')

			histA = fileA.Get(distroA).Clone("h1")
			histA.Sumw2()
			histA.SetDirectory(0)
			histB = fileB.Get(distroB).Clone("h2")
			histB.Sumw2()
			histB.SetDirectory(0)


			fileA.Close()
			fileB.Close()

			

			if(not histA): fatal("Object Not Found : %s in %s not found." % (distroA, filenameA)); return
			if(not histB): fatal("Object Not Found : %s in %s not found." % (distroB, filenameB)); return

			histA.SetLineColor(colors[0])
			#histA.SetFillColor(colors[0])
			histB.SetLineColor(colors[1])
			#histB.SetFillColor(colors[1])

			histA.Rebin(20)
			histB.Rebin(20)
			#histA.GetXaxis().SetRangeUser(0,100)
			#histB.GetXaxis().SetRangeUser(0,100)



			canvas, ratio = plotTwoHistos(histA,histB,label,"Entries",\
                					doLegend=True, legend1="QGSP", legend2="QGSP+Radioactive", \
                					legend1Option="lf", legend2Option="lf", \
                					doRatio=True, ratio_legend1="NoRad", ratio_legend2="Rad",  doLogY=True,\
                					drawOption="hist")

			checkDir(outdir)
			canvas.SaveAs(outName)

			






#####################################################
#####################################################

## The main function to run, when running the script
if __name__ == '__main__':
	main()