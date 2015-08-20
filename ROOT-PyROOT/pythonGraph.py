#
#   @author : Nikos Karastathis
#   @date   : 09.02.2015
#
#   @description: Average current vs y measurement plot
#
#
import ROOT as rt
#import numpy as np
from collections import Counter, defaultdict, OrderedDict
from array import array
import sys

####################### functions to use later #####################

#
#   this is to read a 3 column file and save the data as floats
#   returning the 3 lists
#
def read_from_file(filename):
    x = [];y = []; q = []
    file = open(filename, 'read')
    for line in file.readlines():
        x.append(float(line.split()[0]))
        y.append(float(line.split()[1]))
        q.append(float(line.split()[2]))

    return x, y, q


#
#   returns the duplicates
#
def duplicates(lst):
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

#
#   gets the indices of the duplicates
#
def indices(lst, items= None):
    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind


def graph(newDict, infilename, addname, xlabel, ylabel):
    canvas = rt.TCanvas("Scan", "Scan",800,600)
    canvas.cd()
    canvas.SetFillColor(42)
    canvas.SetGrid()
    graph = rt.TGraph(len(newDict.keys()), array('d',newDict.keys()), array('d',newDict.values())) #array() to convert list to arrays
    graph.SetLineColor(2)
    graph.SetLineWidth(4)
    graph.SetMarkerColor(4)
    graph.SetMarkerStyle(21)
    graph.SetTitle("L1")
    graph.GetXaxis().SetTitle(xlabel)
    graph.GetYaxis().SetTitle(ylabel)
    graph.Draw("APC")
    canvas.Update()
    canvas.Modified()
    nfilename = infilename+"\b\b\b\b"+addname+".pdf"
    canvas.SaveAs(nfilename)

def graph_dictList(dict_list, addname, xlabel, ylabel):
    canvas = rt.TCanvas("ScanAll", "ScanAll",1200,1200)
    canvas.Divide(2,2)
    canvas.cd(0)
#    canvas.SetFillColor(42)
    canvas.SetGrid()
    graph1 = rt.TGraph(len(dict_list[0].keys()), array('d',dict_list[0].keys()), array('d',dict_list[0].values())) #array() to convert list to arrays
    graph1.SetLineColor(rt.kBlack)
    graph1.SetLineWidth(4)
    graph1.SetMarkerColor(rt.kBlue)
    graph1.SetMarkerStyle(21)
    graph1.SetTitle("L1")
    graph1.GetXaxis().SetTitle(xlabel)
    graph1.GetYaxis().SetTitle(ylabel)
    graph1.Draw("APC")

    canvas.cd(1)
    canvas.SetGrid()
    graph2 = rt.TGraph(len(dict_list[1].keys()), array('d',dict_list[1].keys()), array('d',dict_list[1].values())) #array() to convert list to arrays
    graph2.SetLineColor(rt.kBlack)
    graph2.SetLineWidth(4)
    graph2.SetMarkerColor(rt.kBlue)
    graph2.SetMarkerStyle(21)
    graph2.SetTitle("L2")
    graph2.GetXaxis().SetTitle(xlabel)
    graph2.GetYaxis().SetTitle(ylabel)
    graph2.Draw("APC")
    canvas.cd(2)
    canvas.SetGrid()
    graph3 = rt.TGraph(len(dict_list[2].keys()), array('d',dict_list[2].keys()), array('d',dict_list[2].values())) #array() to convert list to arrays
    graph3.SetLineColor(rt.kBlack)
    graph3.SetLineWidth(4)
    graph3.SetMarkerColor(rt.kBlue)
    graph3.SetMarkerStyle(21)
    graph3.SetTitle("L3")
    graph3.GetXaxis().SetTitle(xlabel)
    graph3.GetYaxis().SetTitle(ylabel)
    graph3.Draw("APC")
    canvas.cd(3)
    canvas.SetGrid()
    graph4 = rt.TGraph(len(dict_list[3].keys()), array('d',dict_list[3].keys()), array('d',dict_list[3].values())) #array() to convert list to arrays
    graph4.SetLineColor(rt.kBlack)
    graph4.SetLineWidth(4)
    graph4.SetMarkerColor(rt.kBlue)
    graph4.SetMarkerStyle(21)
    graph4.SetTitle("L4")
    graph4.GetXaxis().SetTitle(xlabel)
    graph4.GetYaxis().SetTitle(ylabel)
    graph4.Draw("APC")

    canvas.Update()
    canvas.Modified()
    nfilename = infilename+"\b\b\b\b"+addname+".pdf"
    canvas.SaveAs(nfilename)


#def graph_combined(newDict1, newDict2):
#    canvas = rt.TCanvas("Scan", "Scan",800,600)
#    canvas.cd()
#    canvas.SetFillColor(42)
#    canvas.SetGrid()
#    graph = rt.TGraph(len(newDict.keys()), array('d',newDict.keys()), array('d',newDict.values())) #array() to convert list to arrays
#    graph.SetLineColor(2)
#    graph.SetLineWidth(4)
#    graph.SetMarkerColor(4)
#    graph.SetMarkerStyle(21)
#    graph.SetTitle("L1")
#    graph.GetXaxis().SetTitle(xlabel)
#    graph.GetYaxis().SetTitle(ylabel)
#    graph.Draw("APC")
#    canvas.Update()
#    canvas.Modified()
#    nfilename = infilename+"\b\b\b\b"+addname+".pdf"
#    canvas.SaveAs(nfilename)


######################################
######################################
##
##          MAIN PROGRAM :
##
######################################
######################################


if len(sys.argv) > 1:
    for i in range(len(sys.argv)-1):
        filenames_lst.append(sys.argv[i+1])
#    filenames = sys.argv[1]
else:
    filenames_lst = ["L1_xray_scan.dat", "L2_xray_scan.dat" , "L3_xray_scan.dat" , "L4_xray_scan.dat"]

dict_list = []

for filename in filenames_lst:
    x_val, y_val, q_val = read_from_file(filename)
    dic =  indices(y_val, duplicates(y_val))
    average_q = []

    print y_val
    print '---'
    print dic
    for key in dic.keys():
        sum = 0;
        for i in range(len(dic[key])):
            sum = sum + q_val[dic[key][i]]
        average_q.append(sum/len(dic[key]))


    newDict = OrderedDict(sorted(dict(zip(dic.keys(), average_q)).items()))

    graph(newDict, filename, "_y", "y [mm]", "<Q> [uA]")

    dict_list.append(newDict)

## i now have a list of 4 dictionaries
graph_dictList(dict_list, filenames_lst[0],"_all", "y [mm]", "<Q> [uA]")
