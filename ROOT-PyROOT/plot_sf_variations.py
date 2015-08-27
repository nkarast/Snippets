##
# @author    Nikos Karastathis < nkarast .at. cern .dot. ch >
#
# @brief     Macro to make the SF validation plots and generate the tex
#
import os
import sys
import time 
from array import array
import ROOT as rt
from optparse import OptionParser
from logging import *

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Prints out the help menu of main
#	Inputs:  [None]
#	Returns: [None]
def usage():
	c="""
Options:
--sf-file 		: the SF file [if not given, main exits]

--point, -p		: specify selection/isolation point [can be csv]

--trigger		: specify trigger [can be csv]

--period 		: specify period [can be csv]

--outdir, -o 	: specify output directory [if not given 
					plots-sf-DD-MM-YYYY will be created]

--tex, -t 		: if given a tex will be generated	

--do-plot-iso 	: [flag - default: False] adds the isolation points

--do-fine 		: [flag - default: False] do fine binning eta-phi

--do-syst 		: [flag - default: False] do also MC systematic variations

--do-png  		: [flag - default: False] save canvas as png

--do-all 		: [flag - default: False] do all selections/isolation points, 
											all triggers, all variations

--debug, -d 	: [flag - default: False] logger prints out everything above 
											debug (default: info)				

--do-compile, -c: [flag - default: False] compile generated TeX with pdflated

--do-clean		: [flag - default: False] after TeX compilation clean up 
											intermediate files

--do-tex-only	: [flag - default: False] Don't make plots, only TeX

--help, -h		: [flag - default: False] Print help


Returns: [None]"""
	print(c)


#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Get the efficiency latex to be drawn on plot
#	Inputs: - x 	= x position
#			- text 	= the text string
#			- color	= the color of text (default black)
#	Returns: - TLatex object
def getEffLatex(x, text, color=1):

    xlep = rt.TLatex(x, 0.93, text)
    xlep.SetNDC()
    xlep.SetTextFont(42)
    xlep.SetTextSize(0.045)
    xlep.SetTextAlign(12)
    xlep.SetTextColor(color)
    xlep.Draw()

    return xlep

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Returns a string with the date in DD-MM-YYYY , separator can be set
#	Inputs: sep -> the separator in date, [default : - ]
#	Returns: date string
def getDate(sep="-"):
	return time.strftime("%d"+sep+"%m"+sep+"%Y")

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Check if a file exists, else raise SystemExit
#	Inputs: - infile 	=  the filename
#	Returns: [None]
def checkFile(infile):
	if os.path.isfile(infile): 
		info("Opening file %s... OK" % infile)
	else:
		fatal("File does not exist! Terminating...")
		raise SystemExit(0)

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Set the gStyle 
#	Inputs:  [None]
#	Returns: [None]
def setStyle():
	rt.gStyle.SetOptStat(0)
	rt.gStyle.SetPadTopMargin(0.10)
	rt.gStyle.SetPadBottomMargin(0.15)
	rt.gStyle.SetPadLeftMargin(0.15)
	rt.gStyle.SetPadRightMargin(0.20)
	rt.gStyle.SetPaintTextFormat('0.2f')
	rt.gStyle.SetPalette(1)
	rt.gROOT.ForceStyle()

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Checks if a directory exists, if not it can create it
#	Inputs:  directory  = the directory to check
#			 create [bool] = Create the directory if it does not exist
#	Returns: True  -> Directory already exists
#			 False -> Directory did not exist and maybe (if create=True) now it does
def checkDir(directory, create=True):
    if not os.path.exists(directory):
        if create: os.makedirs(directory)
        return False
	return True


#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Draws a histogram and saves the canvas in pdf format (or png if png==True)
#	Inputs:	hist		-> The histogram to be drawn
#			point		-> The isolation point - used for savename and TLatex
#			trigger		-> The trigger - used for savename and TLatex
#			region		-> The detector region - used for savename, TLatex and draw option
#			sample		-> "Data", "MC" or "Data/MC" [is lower() and replace("/","_")]
#			variable	-> The variable to be plotted [placeholder for more?]
#			variation	-> "Nominal", "stat/syst_up/down", or "[variation]_over_Nominal"
#			outdir		-> Output directory
#			png	[Bool]	-> If true save canvas as png else pdf (default)
#	Returns: [None]
def drawHist(hist, point, trigger, region, sample, variable, variation, outdir, png=False):
	## the sample and variations transformed to lower case, and "/" are removed from the sample
	canvas_id = "plot_prepTP_"+point+"_"+region+"_Match_"+trigger+"_probe_"+region+"_"+variable+"_"+sample.lower().replace("/","_")+"_"+variation.lower()
	canvas = rt.TCanvas(canvas_id,canvas_id, 750, 600)
	canvas.cd()
	setStyle()
	draw_opt = 'COLZ TEXT'
	if 'endcap' in region:
		draw_opt = 'COLZ TEXT90' ## pretty!

	##	check if the current variations is the ratio of [variation]_over_Nominal and 
	#	split the string using the _over_ 
	if("over" in variation):
		ztitle = sample+" "+variation.lower().split("_over_")[0]+" / "+variation.lower().split("_over_")[1]
	else:
		ztitle = sample+" "+variation

	hist.GetZaxis().SetTitle(ztitle)
	hist.GetZaxis().SetTitleOffset(1.25)
	hist.GetZaxis().SetRangeUser(0.3, 1.1)
	hist.GetZaxis().CenterTitle()
	hist.Draw(draw_opt)

	## get the efficiency latex - to be drawn above histo border
	lpr = getEffLatex(0.10, '%s  %s/%s' %(region, trigger.replace('HLT_', ''), point))
	lpr.Draw()

	## check if the outdir exists, else create it
	dummy_bool = checkDir(outdir)

	## change the suffix pdf or png
	if(png): saveName = outdir +"/"+ canvas_id+".png"
	else: saveName = outdir +"/"+ canvas_id+".pdf"
	canvas.SaveAs(saveName)

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
##	Generates a TeX file with the summary plots. If configured, the function also compiles it.
#	Inputs:	tex_name		-> the name of the TeX file to be generated
#			plot_folder		-> the folder containing the plots
#			slide_title		-> the title of the presentation
#			selections 		-> the list of selections/isolation points 
#			triggers		-> the list of triggers
#			regions 		-> the list of detector regions
#			png	[Bool]		-> If true the plots are in .png format, else .pdf (default : pdf)
#			compile	[Bool]	-> If true the TeX file is compiled into a pdf (default: False)
#			clean [Bool]	-> If true & compile true, only the .tex and .pdf files will remain 
#	Returns: [None]
def makeTex(tex_name, plot_folder, slide_title, selections, triggers, regions, png=False, compile=False, clean=True):

	### tex file name

	if ".tex" in tex_name :
		filename=tex_name
	else:
		filename=tex_name+".tex"

	fileout = open(filename, "w")

	if(png): suffix=".png"
	else: suffix=".pdf"

	variables = [ 
				['Efficiency' , ['data_nominal', 'mc_nominal', 'data_mc_nominal']],
				['Uncertainties' , ['data_stat_down_over_nominal', 'data_stat_up_over_nominal' , 
									'mc_syst_down_over_nominal', 'mc_syst_up_over_nominal']]
				]


	def a(str):
		fileout.write(str+"\n")
	
	a("\documentclass[aspectratio=169,hyperref={pdfpagelayout=SinglePage}]{beamer}")
	a("\usetheme{default}")
	a("\usepackage{graphicx}")
	a("\usepackage{xspace}")
	a("\usepackage{amsmath}")
	a("\usepackage{multicol}")
	a("\\begin{document}")
	a("\\title["+slide_title+"]{"+slide_title+"}")
	a("\\author{Muon Trigger Signature Group}")
	a("\\date{\\today}")
	a("\\begin{frame}")
	a("\\titlepage")
	a("\end{frame}")
	a("\\begin{frame}[allowframebreaks]")
	a("\\frametitle{Table of Contents [Clickable]}")
	a("\\tiny{")
	a("\\begin{multicols}{2}")
	a("\\tableofcontents")
	a("\end{multicols}")
	a("}") #//small
	a("\end{frame}")

	for selection in selections:
		a(" ")
		rpl_sel = selection.replace("_","\_")
		a("\\section{"+rpl_sel+"}")
		a("\\begin{frame}")
		a("\\begin{center}")
		a("\\Large{\\textbf{"+rpl_sel+"}}\\\\")
		a("\\end{center}")
		a("\\end{frame}")
		


		for trigger in triggers:
			a(" ")
			rpl_trig = trigger.replace("_","\_")
			a("\\subsection{"+rpl_trig+"}")
			a("\\begin{frame}")
			a("\\begin{center}")
			a("\\Large{\\textbf{"+rpl_trig+"}}\\\\")
			a("\\end{center}")
			a("\\end{frame}")
			


			for region in regions:
				for ivar in variables:
					a("\\begin{frame}")
					a("\\frametitle{\small{"+ivar[0]+" "+rpl_trig+" "+region+"}}")
					a("\\begin{center}")
					if "Uncertainties" in ivar[0]: a("\\begin{columns}")

					count = 0
					for jvar in ivar[1]:

						if(len(ivar[1])!=4):
							perCent = 1./len(ivar[1])

							#a("\centering")
							plot_name = plot_folder+"/plot_prepTP_"+selection+"_"+region+"_Match_"+trigger+"_probe_"+region+"_eff_etaphi_coarse_"+jvar+suffix
							
							if count==1:
								a("\\includegraphics[width=0.38\\textwidth]{"+plot_name+"}\\\\")
							else:
								a("\\includegraphics[width=0.38\\textwidth]{"+plot_name+"}\\xspace")
							count = count + 1

						else:
							perCent = 0.5
							if(count % 2 == 0):
								a("\\column{%.02f\\textwidth}"% perCent)
								a("\centering")
							plot_name = plot_folder+"/plot_prepTP_"+selection+"_"+region+"_Match_"+trigger+"_probe_"+region+"_eff_etaphi_coarse_"+jvar+suffix
							a("\\includegraphics[width=0.75\\textwidth]{"+plot_name+"}\\\\")
							count = count+1
					
					if "Uncertaint" in ivar[0]: a("\\end{columns}")
					a("\\end{center}")
					a("\\end{frame}")
					a(" ")
					a("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
					a(" ")
	a(" ")
	a("\\end{document}")
	fileout.close()

	if(compile):
		cmd = "pdflatex "+filename
		os.system(cmd)
		os.system(cmd) # twice to get toc

		if(clean):
			to_remove = ["aux", "log", "nav", "out", "snm", "toc"]
			for rmv in to_remove:
				warning("Cleaning up files : %s " % filename[:-3]+rmv)
				cmd2 = "rm "+filename[:-3]+rmv
				os.system(cmd2)
			

		


#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

##	This is the main function
#	
#	Configure the option parser and the logger
#	Initialise the isolation points, triggers, regions, data periods, etc
#	Open the sf-file provided and draw the histograms!
#
#	Options:	--sf-file 		: the SF file [if not given, main exits]
#				--point, -p		: specify selection/isolation point [can be csv]
#				--trigger		: specify trigger [can be csv]
#				--period 		: specify period [can be csv]
#				--outdir, -o 	: specify output directory [if not given plots-sf-DD-MM-YYYY will be created]
#				--tex, -t 		: if given a tex will be generated [if not given "summary_plots.tex" will be created]
#
#				
#				
#				--do-plot-iso 	: [flag - default: False] adds the isolation points
#				--do-fine 		: [flag - default: False] do fine binning eta-phi
#				--do-syst 		: [flag - default: False] do also MC systematic variations
#				--do-png  		: [flag - default: False] save canvas as png
#				--do-all 		: [flag - default: False] do all selections/isolation points, all triggers, all variations
#				--debug, -d 	: [flag - default: False] logger prints out everything above debug (default: info)
#				--do-compile, -c: [flag - default: False] compile generated TeX with pdflated
#				--do-clean		: [flag - default: False] after TeX compilation clean up intermediate files
#				--do-tex-only	: [flag - default: False] Don't make plots, only TeX
#				--help, -h		: [flag - default: False] Print help
#
#				
#	Returns: [None]
def main():
	## Setup the parser
	parser = OptionParser(add_help_option=False)

	parser.add_option('--sf-file',			type='string',	default=None,			dest='sf_file')
	parser.add_option('--point', '-p',		type='string',	default=None,			dest='arg_point')
	parser.add_option('--trigger',	    	type='string',	default=None,         	dest='arg_trig')
	parser.add_option('--period',       	type='string',	default=None,			dest='arg_period')
	parser.add_option('--outdir', '-o', 	type='string',	default=None,          	dest='outdir')
	parser.add_option('--tex', '-t',		type='string',	default=None, 			dest='tex_file')

	parser.add_option('--do-plot-iso',   		action='store_true', default=False,   dest='do_plot_iso')
	parser.add_option('--do-fine',   			action='store_true', default=False,   dest='do_fine_bin')
	parser.add_option('--do-syst',   			action='store_true', default=False,   dest='do_syst')
	parser.add_option('--do-png',   			action='store_true', default=False,   dest='do_png')
	parser.add_option('--do-all',   			action='store_true', default=False,   dest='do_all')
	parser.add_option('-d', '--debug', 			action='store_true', default=False,   dest='debug')
	parser.add_option('--do-compile',   		action='store_true', default=False,   dest='compile')
	parser.add_option('--do-clean',   			action='store_true', default=False,   dest='clean')
	parser.add_option('--do-tex-only', 			action='store_true', default=False,   dest='tex_only')
	parser.add_option('--help','-h', 			action='store_true', default=False,   dest='help')

	(options, args) = parser.parse_args()

	if(options.help): usage()

	## Switch rt to batch mode 
	rt.gROOT.SetBatch(True)
	setStyle()

	## Initialise logging
	FORMAT = '%(asctime)-15s : %(levelname)-8s : %(message)s'
	if options.debug:
		basicConfig(format=FORMAT, level=DEBUG, datefmt='%H:%M:%S')
	else:
		basicConfig(format=FORMAT, level=INFO, datefmt='%H:%M:%S')


	## Check the input file 
	if (options.sf_file == None) and (options.tex_only==False):
		critical("No SF file provided. Exiting...")
		raise SystemExit(0)
	if(options.tex_only==False):	
		checkFile(options.sf_file)

	## Check the output directory
	if options.outdir == None:
		m_outdir = 	"plots-sf-"+getDate()
		warning("Output directory was not given. Created output directory : %s" % m_outdir)
	else:
		m_outdir = options.outdir


	## Check the period(s)
	periods= []
	if options.arg_period==None :
		periods.append('periodD')
	else:
		period.append(options.arg_period)
	debug(periods)

	## Check the selection/isolation 
	selections = []
	if ((options.arg_point!=None) and (options.arg_point!='all')) and not options.do_all:
		for p in options.arg_point.split(","):
			selections.append(p)	
	else:
		selections = ['Loose', 'Medium','Tight']

	## Should include isolation?
	if options.do_plot_iso or options.do_all:
		selections =	['Loose']#,  'Loose_IsoGradient',  'Loose_IsoLoose',  'Loose_IsoTight',
					#'Medium', 'Medium_IsoGradient', 'Medium_IsoLoose', 'Medium_IsoTight',
					#'Tight',  'Tight_IsoGradient',  'Tight_IsoLoose',  'Tight_IsoTight']
	debug(selections)

	## Check for which triggers to run
	triggers = []
	if (options.arg_trig!=None and options.arg_trig!='all') and not options.do_all:
		for t in options.arg_trig.split(","):
			triggers.append(t)
	else:
		triggers = 	['HLT_mu20_iloose_L1MU15']#, 
					#'HLT_mu20_iloose_L1MU15_OR_HLT_mu50',
					#'HLT_mu24_iloose_L1MU15',
					#'HLT_mu24_imedium', 
					#'HLT_mu24_iloose_L1MU15_OR_HLT_mu50',
					#'HLT_mu24_imedium_OR_HLT_mu50', 
					#'HLT_mu26_imedium', 
					#'HLT_mu26_imedium_OR_HLT_mu50',
					#'HLT_mu50']  #@todo add L1 trig
	debug(triggers)


	## Detector Regions
	regions = ['barrel','endcap']
	debug(regions)


	## Map is in eta-phi bins - coarse for Early Run II
	variables = []
	if options.do_fine_bin and not options.do_all :
		variables.append("eff_etaphi_fine")
	elif not options.do_fine_bin and not options.do_all:
		variables.append("eff_etaphi_coarse")
	else:
		variables = ["eff_etaphi_coarse"]

	debug(variables)

	## Some labels in case they are not set in the SF file histograms
	labels = {"eff_etaphi_fine":["Probe #eta", "Probe #phi"],
				"eff_etaphi_coarse":["Probe #eta", "Probe #phi"]}

	## The samples to use -- Uppercase/Lowercase matters... for the labels ;)
	samples = ['Data', 'MC']
	debug(samples)

	## Nominal, Stat and Syst variations (if do-sys) - Upper "N" for the labels ;)
	## @attention Nominal should always be first!!!
	variations = ['Nominal', 'stat_up', 'stat_down']
	if options.do_syst or options.do_all:
		variations.append('syst_up')
		variations.append('syst_down')
	debug(variations)

	if(options.tex_only == False):
		## open the file
		f_input = rt.TFile.Open(options.sf_file, 'read')

		## happy looping -- sorry python developpers :(
		for selection in selections:
			info("Working on %s selection..." % selection)
			for period in periods:
				for trigger in triggers:
					info("Trigger : %s" % trigger)
					f_input.cd()
					for variable in variables:
						for region in regions:
							## keep data and mc for data/mc ratio plot
							keep_data = rt.TH2F()
							rt.SetOwnership(keep_data, False)
							keep_mc   = rt.TH2F()
							rt.SetOwnership(keep_mc, False)

							for sample in samples:
								## keep the nominal data or mc for ratios 
								## @attention that's why nominal should be the first variation
								temp_nominal = rt.TH2F()
								rt.SetOwnership(temp_nominal, False)

								for variation in variations:
									## there is no syst for data
									if ( (sample=="Data") and ('syst' in variation) ): continue

									hname = selection+"/"+period+"/"+trigger+"/"+variable+"_"+region+"_"+sample.lower()+"_"+variation.lower()
									htemp = rt.gDirectory.Get(hname)
									rt.SetOwnership(htemp, False)
									## draw plot in any case
									drawHist(htemp, selection, trigger, region, sample, variable, variation, m_outdir, png=options.do_png)
									
									if(variation.lower() == "nominal"):
										temp_nominal = htemp.Clone(htemp.GetName()+"_temp")

										if(sample.lower() == "data"):
											keep_data = htemp.Clone(htemp.GetName()+"_temp_data")
										if(sample.lower() == "mc"):
											keep_mc = htemp.Clone(htemp.GetName()+"_temp_mc")
									
									else:
										## draw variation/nominal plot
										htemp.Divide(temp_nominal)
										variation = variation.lower()+"_over_Nominal"
										drawHist(htemp, selection, trigger, region, sample, variable, variation, m_outdir, png=options.do_png)

									del htemp

							## draw data/mc plot
							keep_data.Divide(keep_mc)
							drawHist(keep_data, selection, trigger, region, "Data/MC", variable, "Nominal", m_outdir, png=options.do_png)

		info('done... plots under : %s' % m_outdir)


		if(options.tex_file != None):
			info("Generating TeX file : %s" % options.tex_file)
			makeTex(options.tex_file, m_outdir, "Muon Trigger Summary Plots for 25ns data", selections, triggers, regions, png=options.do_png, compile=options.compile, clean=options.clean)


		info('All done. Bye!')

	else:
		if(options.tex_file != None):
			info("Generating TeX file : %s" % options.tex_file)
			makeTex(options.tex_file, m_outdir, "Muon Trigger Summary Plots for 25ns data", selections, triggers, regions, png=options.do_png, compile=options.compile, clean=options.clean)


		info('All done. Bye!')

#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*
#!! --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

if __name__ == '__main__':
	main()
