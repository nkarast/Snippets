"""
    Available Functions:
    *   init_logger(logfile="",loglevel="debug"):
    *   replaceBranch(str_infile, str_intree, float_factor, str_outfile):
    *   get_remap_config(cfgfile):
    *   get_unrolled(infile, histname,tag):
    *   get_remappedBDT(remapList,h_unrolled, tag):
    *   normalize(histo)
    *   setStyle()
    *   setHSG3Style():
    *   setHistoStyle(histo):
    *   setHistoHSG3Style(histo):
    *   drawNorm(normtxt):
    *   drawOverflow(h):
    *   setPadStyle(pad):
    *   duplicates(lst)
    *   indices(lst, items= None)
    *   random_sample_func(func, nsamplings=1, seed=0)
    *   random_sample_hist(hist, nsamplings=1, seed=0)
    *   getRootToArray(filename, treename)
    *   getRootToRec(filename, treename)
    *   getTreeToArray(tree)
    *   getTreeToRec(tree)
    *   getArrayToRoot(rec_array, foutname, treename):
    *   fillHistFromNumpy(np_arr, histList=[], histname="")
    *   getListOfKeys(file, str_directory="")
    *   shell_command(cmd)
    *   addinquadrature(numbers, power=2)
    *   fixstring(s)
    *   drawLatex(str, x=0.22, y=0.86, size=0.06, font=42, color=1)
    *   getKS(hist1, hist2)
    *   getLegend(inDict=None, x1=0.65, y1=0.65, x2=0.90, y2=0.90, borderSize=0, font=42, fontSize=0.045, fillColor=0, nColumns=2)
 
"""



from logging import *

def init_logger(logfile="",loglevel="debug"):
    """
        Initialize the format and log level and even the file of the logger
        Inputs logfile (default=""), loglevel (default="debug")
    """
    m_level = ""
    if loglevel=="debug" : m_level = DEBUG
    elif loglevel=="info" : m_level = INFO
    elif loglevel=="warning" : m_level = WARNING
    elif loglevel=="error" : m_level = ERROR
    elif loglevel=="critical" : m_level = loggin.CRITICAL
    FORMAT = '%(asctime)s %(levelname)s : %(message)s'
    basicConfig(format=FORMAT, filename=logfile, level=m_level)
    info('(init_logger) logger initialized with format : %s , file = %s , at level %s ' % (FORMAT, logfile, loglevel) )

#def debug(str):
#    import logging
#    logging.debug(str)
#
#def info(str):
#    outstring='\033[132m [info] '+str+'\033[1m'
#    print outstring
#
#def warning(str):
#    outstring='\033[133m [warning] '+str+'\033[1m'
#    print outstring
#
#def error(str):
#    outstring='\033[135m [error] '+str+'\033[1m'
#    print outstring
#
#def fatal(str):
#    outstring='\033[141m [fatal] '+str+'\033[1m'
#    print outstring

#---***---***---***---***---***---***---***---***---***---***---***---

def replaceBranch(str_infile, str_intree, float_factor, str_outfile):
    """
        Replaces a branch in a tree by multiplying it
        It only works for .EventWeight . hardcoded
        Inputs : infilename , intreename, multiplicative factor, oufilename
    """
    from rootpy.tree import Tree, TreeModel, TreeChain
    from rootpy.io import root_open
    from rootpy import asrootpy
    
    chain = TreeChain(name=str_intree, files=str_infile)
    f_copy = root_open(str_outfile,'recreate')
    tree_copy = Tree(str_intree)

    tree_copy.set_buffer(chain._buffer, create_branches=True)

    for entry in chain:
        entry.EventWeight = entry.EventWeight *float_factor
        tree_copy.Fill()

    tree_copy.Write()
    f_copy.Close()

#---***---***---***---***---***---***---***---***---***---***---***---

def get_remap_config(cfgfile):

    """
        #   Get a list with the remap bins (1st column of cfg file)
        #       - cfg file : a string to the cfg file
        #   Returns : a list object
    """
    
    incfgfile = open(cfgfile,'r')
    remapList = []
    for line in incfgfile.readlines():
        line.split()
        if "#" in line[0] or line[0]=="" or ":" in line[0]: continue
        else: remapList.append(int(line[0]))
    incfgfile.close()
    info('(get_remap_config) reading config file [ %s ] ... DONE' % incfgfile)
    return remapList

#---***---***---***---***---***---***---***---***---***---***---***---

def get_unrolled(infile, histname,tag):
    import ROOT as rt
    """
        #   Get the unrolled 2D histogram:
        #       - infile : string to the input ROOT file that contains the 2D hist
        #       - histname : name of the histogram in the file
        #       - tag : tag to put in the name of the unrolled (amcatnlo or powheg)
        #   Returns : a TH1F object with 50 bins from -1 to 1
        """
    
    ifile = rt.TFile.Open(infile,"read")
    h2_bdt = ifile.Get(histname)
    name = tag+"_unrolled"
    h1_unrolled = rt.TH1F(name,name,50,-1   ,1)
    binI=0
    for x_bin in range(1,11):
        for y_bin in range(1,6):
            binI=binI+1
            bin_sig0 = h2_bdt.GetBinContent(x_bin,y_bin)
            bin_sig0_err = h2_bdt.GetBinError(x_bin,y_bin)
            h1_unrolled.SetBinContent(binI,bin_sig0)
            h1_unrolled.SetBinError(binI, bin_sig0_err)
    info('(get_unrolled) unrolling %s... DONE' % tag)
    return h1_unrolled

#---***---***---***---***---***---***---***---***---***---***---***---

def get_remappedBDT(remapList,h_unrolled, tag):
    import ROOT as rt
    """
        #   Get the remapped distribution, named "remapped_"+tag:
        #       - remapList : a list containing the remapped bins (use get_remap_config function)
        #       - h_unrolled : a histogram with the unrolled distribution (use get_unrolled)
        #       - tag : tag to put in the name of the unrolled (amcatnlo or powheg)
        #   Returns : a TH1F object with len(remapList) bins from -1 to 1
        """
    
    name = "remapped_"+tag
    h1_remapped = rt.TH1F(name,name,len(remapList),-1,1)
    
    bin_in =  1
    for i in range(len(remapList)):
        bin_out = i+1
        content = 0.
        sumerror2 = 0
        for j in range(remapList[i]):
            content = content+h_unrolled.GetBinContent(bin_in)
            error = h_unrolled.GetBinError(bin_in)
            error2 = error*error
            sumerror2 = sumerror2+error2
            bin_in = bin_in+1
        h1_remapped.SetBinContent(bin_out,content)
        h1_remapped.SetBinError(bin_out,math.sqrt(sumerror2))
    info('(get_remappedBDT) remapping %s... DONE' % tag)
    return h1_remapped

#---***---***---***---***---***---***---***---***---***---***---***---

def normalize(histo):
    import ROOT as rt
    waring('(normalize) normalising histogram %s' % histo.GetName())
    histo.Scale(1/histo.Integral())
    return histo

#---***---***---***---***---***---***---***---***---***---***---***---

def setStyle():
    import ROOT as rt
    info('(setHSG3Style) setting HSG3 style')
    info('(setStyle) setting style')
    rt.gStyle.SetOptStat(0)
    rt.gStyle.SetCanvasBorderMode(0)
    rt.gStyle.SetCanvasColor(0)
    rt.gStyle.SetStatBorderSize(0) #frame style of stat-box 1
    
    rt.gStyle.SetTitleBorderSize(0)
    rt.gStyle.SetTitleFillColor(0)
    rt.gStyle.SetPadColor(0)
    rt.gStyle.SetPadBorderMode(0)
                                    
    rt.gStyle.SetLineWidth(3)
    rt.gStyle.SetPadTickX(0) #1:ticks on upper,2: ticks+labels on upper xaxis
    rt.gStyle.SetPadTickY(0)
                                                
    rt.gStyle.SetPadLeftMargin(0.12) # 0.18
    rt.gStyle.SetPadRightMargin(0.08)
    rt.gStyle.SetPadTopMargin(0.07)
    rt.gStyle.SetPadBottomMargin(0.17)
    rt.gStyle.SetFrameLineWidth(2)
    rt.gStyle.SetFrameFillColor(0)
    rt.gStyle.SetPaintTextFormat(".2f")

    rt.gStyle.SetTitleOffset(1.1,"X")
    rt.gStyle.SetTitleOffset(1.1,"Y")
    rt.gStyle.SetTextFont(42)

#---***---***---***---***---***---***---***---***---***---***---***---

def setHSG3Style():
    import ROOT as rt
    info('(setHSG3Style) setting HSG3 style')
    
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
    rt.gStyle.SetPadLeftMargin(0.16)
    rt.gStyle.SetPadRightMargin(0.05)
                                                                                
    rt.gStyle.SetPadTickX(1)
    rt.gStyle.SetPadTickY(1)
        
    rt.gStyle.SetFrameLineWidth(1)
    rt.gStyle.SetLineWidth(1) # width of ticks

#---***---***---***---***---***---***---***---***---***---***---***---

def setHistoStyle(histo): #th1
    import ROOT as rt

    info('(setHistoStyle) setting histo style for hist %s', hist.GetName())
    histo.SetTitle("")
    histo.SetLineWidth(3)
    histo.SetTitleSize(0.07,"x")
    histo.SetTitleSize(0.07,"y")
    histo.SetNdivisions(505,"x")
    histo.SetNdivisions(505,"y")
    histo.SetLabelSize(0.07,"x")
    histo.SetLabelSize(0.07,"y")
    histo.SetTitleOffset(1.,"x")
    histo.SetTitleOffset(1.,"y")

#---***---***---***---***---***---***---***---***---***---***---***---

def setHistoHSG3Style(histo): #TH1F
    import ROOT as rt

    info('(setHistoHSG3Style) setting HSG3 histo style for hist %s', hist.GetName())
    histo.SetTitle("")
    histo.SetLineWidth(0)
    #histo.SetLineWidth(3)
    histo.SetTitleSize(0.07,"x")
    histo.SetTitleSize(0.07,"y")
    histo.SetNdivisions(510,"x")
    histo.SetNdivisions(510,"y")
    histo.SetLabelSize(0.05,"x")
    histo.SetLabelSize(0.05,"y")
    histo.SetTitleOffset(1.1,"x")
    histo.SetTitleOffset(1.1,"y")

#---***---***---***---***---***---***---***---***---***---***---***---

def drawNorm(normtxt): #TString
    import ROOT as rt
    normbox = rt.TLatex()
    normbox.SetNDC()
    normbox.SetTextSize(0.04)
    normbox.SetTextAngle(90)
    normbox.DrawLatex(0.975,0.18,normtxt)
    normbox.Draw()

#---***---***---***---***---***---***---***---***---***---***---***---

def drawOverflow(h): # th1f
    import ROOT as rt
    info('(drawOverflow) adding overflow bin in histo %s' % histo.GetName())
    nx1  = int(h.GetNbinsX()+1)
    nx  = int(h.GetNbinsX())
    x = float(h.GetBinContent(nx))
    x1 = float(h.GetBinContent(nx1))
    h.SetBinContent(nx,x+x1)
    h.SetBinContent(nx1,0)
    ex = float(h.GetBinError(nx))
    ex1 = float(h.GetBinError(nx1))
    h.SetBinError(nx,ex+ex1)
    h.SetBinError(nx1,0)

#---***---***---***---***---***---***---***---***---***---***---***---

def setPadStyle(pad): #TPad

    pad.SetTopMargin(0.07)
    pad.SetBottomMargin(0.05)
    pad.SetFrameLineWidth(2)
    pad.SetLeftMargin(0.16)

#---***---***---***---***---***---***---***---***---***---***---***---

def setsubPadStyle(pad): #TPad

    pad.SetBottomMargin(0.4)
    pad.SetFrameLineWidth(2)
    pad.SetLeftMargin(0.16)

#---***---***---***---***---***---***---***---***---***---***---***---

def duplicates(lst):
    from collections import Counter
    """
       returns the duplicates
    """
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

#---***---***---***---***---***---***---***---***---***---***---***---

def indices(lst, items= None):
    from collections import defaultdict
    """
       gets the indices of the duplicates
    """
    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind

#---***---***---***---***---***---***---***---***---***---***---***---

def random_sample_func(func, nsamplings=1, seed=0):
    """
        return a numpy array with random samples (samplings)
        which are taken randomly from a function.
        The sampling sequence starts with a random seed if seed == 0
        Inputs : function (TF1, TF2, TF3) , # of samplings, seed (default=0)
    """
    from ROOT import TF1, TF2, TF3
    from root_numpy import random_sample
    info('(random_sample_hist) getting random sample of %f with seed %f from function ' % (nsamplings, seed))
    return random_sample(func, nsamplings, seed)

#---***---***---***---***---***---***---***---***---***---***---***---

def random_sample_hist(hist, nsamples=1, seed=0):
    """
    return a numpy array with random samples (samplings)
    which are taken randomly from a histogram.
    The sampling sequence starts with a random seed if seed == 0
    Inputs : histogram (TH1, TH2, TH3) , # of samplings, seed (default=0)
    """
    from ROOT import TH1, TH2, TH3
    from root_numpy import random_sample
    info('(random_sample_hist) getting random sample of %f with seed %f from histogram ' %(nsamples, seed))
    return random_sample(hist, nsamples, seed)

#---***---***---***---***---***---***---***---***---***---***---***---

def getRootToArray(filename, treename):
    """
        Convert and return a tree into a numpy array
        Inputs: filename and treename
        Return: np array
    """
    from root_numpy import root2array, root2rec
    return root2array(filename, treename)

#---***---***---***---***---***---***---***---***---***---***---***---

def getRootToRec(filename, treename):
    """
        Convert and return a tree into a record numpy array
        Inputs: filename and treename
        Return: rec array
    """
    from root_numpy import root2array, root2rec
    info('(getRootToRec) building rec array from tree %s in file %s' % (treename, filename))
    return root2rec(filename, treename)

#---***---***---***---***---***---***---***---***---***---***---***---

def getTreeToArray(tree):
    """
        Convert and return a tree into a numpy array
        Inputs: TTree object
        Return: np array
    """
    from root_numpy import tree2array
    return tree2array(tree)

#---***---***---***---***---***---***---***---***---***---***---***---

def getTreeToRec(tree):
    """
        Convert and return a tree into a record numpy array
        Inputs: TTree object
        Return: rec array
    """
    from root_numpy import tree2rec
    return tree2rec(treename)

#---***---***---***---***---***---***---***---***---***---***---***---

def getArrayToRoot(rec_array, foutname, treename):
    """
        Convert and return a tree into a numpy array
        Inputs: TTree object
    """
    from root_numpy import array2root
    info('(getArrayToRoot) building tree %s in file %s' % (treename, foutname))
    array2root(rec_array, foutname, treename)

#---***---***---***---***---***---***---***---***---***---***---***---

def fillHistFromNumpy(np_arr, histList=[], histname=""):
    """
        Fill a 1D or 2D hist from a np array
        Inputs: The numpy array and a list with [nbins, min, max] for 1D or 
                [nbinsX, minX, maxX, nbinsY, minY, maxY]
        Return: The hist
    """
    from ROOT import TH1F, TH2F
    from root_numpy import fill_hist
    hist = 0
    if histname =="" : histname="hist"
    if len(histList) == 0 : pass
    elif len(hist)==3 : hist = ROOT.TH1F(histname, histname, int(histList[0]),histList[1],histList[2])
    elif len(hist)==6 : hist = ROOT.TH2F(histname, histname, int(histList[0]),histList[1],histList[2], int(histList[3]),histList[4],histList[5])
    info('(fillHistFromNumpy) filling hist with name %s' % histname)
    fill_hist(hist, np_arr)
    return hist

#---***---***---***---***---***---***---***---***---***---***---***---

def getListOfKeys(file, str_directory=""):
    """
        Return a list with the key names of the file under a certain directory
        Inputs : the TFile and (if needed) a directory to cd and then get the keys
        Returns : a list with keynames
    """
    import ROOT as rt

    info('(getListOfKeys) Opening file %s and going into directory %s .' % (file.GetName(), str_directory))
    if str_directory != "" :
        rt.gDirectory.cd(str_directory)
    return [key.GetName() for key in rt.gDirectory.GetListOfKeys()]

#---***---***---***---***---***---***---***---***---***---***---***---

def shell_command(cmd):
    import os
    """
        shell_command(cmd):
        -------------------
        Run the `cmd` string as system command.
    """
    
    os.system(cmd)

#---***---***---***---***---***---***---***---***---***---***---***---

def addinquadrature(numbers, power=2):
    """
        Add numbers in quadrature and return the sqrt(numbers[0]**2 + .... )
        """
    import math
    if p <= 0:
        return 0.
    f = lambda x: math.pow(x, p)
    s = sum(map(f, numbers))
    return math.pow(s, 1.0 / p)

#---***---***---***---***---***---***---***---***---***---***---***---

def fixstring(s):
    """
        Remove special characters from the input string s
    """
    
    special =  '~!@#$%^&*()+={}\\|\'";:?><,/-. '
    for char in special:
        s = s.replace(char,'')
    return s

#---***---***---***---***---***---***---***---***---***---***---***---

def drawLatex(str, x=0.22, y=0.86, size=0.06, font=42, color=1):
    """
        Draws a latex str of size 0.06 at 0.22, 0.86
        Inputs : str, x,y,size
        Output : None
    """

    import ROOT as rt
    tex = rt.TLatex()
    tex.SetNDC()
    tex.SetTextFont(font)
    tex.SetTextColor(color)
    tex.SetTextSize(size)
    tex.DrawLatex(x, y, str)

#---***---***---***---***---***---***---***---***---***---***---***---

def getKS(hist1, hist2):
    """
        Computes and returns the Kolmogorov-Smirnoff Test of
        hist1 and hist2
        Inputs : hist1, hist2
        Returns : KS(hist1, hist2)
    """
    import ROOT as rt
    return hist1.KolmogorovTest(hist2)

#---***---***---***---***---***---***---***---***---***---***---***---

def getLegend(inDict=None, x1=0.65, y1=0.65, x2=0.90, y2=0.90, borderSize=0, font=42, fontSize=0.045, fillColor=0, nColumns=2):
    """
        Creates a legend at 0.65, 0.65, 0.90 0.90
        hist1 and hist2
        Inputs : inDict, x1, y1, x2, y2, borderSize, font, fontSize, fillColor, nColumns
                -> inDict is a dictionary with key = TH1F histo and value a list of 2 str
                    dict(hist1:["Data","lf"], hist2:["Bkg","lep"])
        Returns : None
        """


    import ROOT as rt
    leg = rt.TLegend(x1,y1,x2,y2)
    leg.SetBorderSize(borderSize)
    leg.SetTextFont(font)
    leg.SetTextSize(fontSize)
    leg.SetFillColor(fillColor)
    leg.SetNColumns(nColumns)
    if inDict != None:
        for key in inDict.keys():
            len.AddEntry(key, inDict[key][0], inDict[key][1])



