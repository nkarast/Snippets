#
#  -- My Python Utils -- 
#  A set of function useful for my everyday research life...
#   
#  Author: Nikos Karastathis < nkarast .at. cern .dot. ch >
#   
#   List of available functions:
#
#   - initLogger()
#   - setLoggerLevel()
#   - duplicates()
#   - duplicateIndices()
#   - checkDir()
#   - shell()
#   - addInQuadrature()
#   - fixString()










from logging import *

def initLogger(logfile="",loglevel="debug"):
    """
        Initialize the format and log level and even the file of the logger
        Inputs logfile (default=""), loglevel (default="debug")
    """
    m_level = ""
    if loglevel.lower()=="debug" : m_level = DEBUG
    elif loglevel.lower()=="info" : m_level = INFO
    elif loglevel.lower()=="warning" : m_level = WARNING
    elif loglevel.lower()=="error" : m_level = ERROR
    elif (loglevel.lower()=="critical") or (loglevel.lower()=="fatal") : m_level = loggin.CRITICAL
    FORMAT = '%(asctime)-15s : %(levelname)-8s : %(message)s'
    basicConfig(format=FORMAT, filename=logfile, level=m_level, datefmt='%d/%m/%Y %H:%M:%S')
    info('(init_logger) logger initialized with format : %s , file = %s , at level %s ' % (FORMAT, logfile, loglevel) )

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def setLoggerLevel(loglevel):
    """
        Change the logger level to loglevel (from debug (default))
        Inputs : String with loglevel
        Returns : None
    """

    m_level = ""    
    if loglevel.lower()=="debug" : m_level = DEBUG
    elif loglevel.lower()=="info" : m_level = INFO
    elif loglevel.lower()=="warning" : m_level = WARNING
    elif loglevel.lower()=="error" : m_level = ERROR
    elif (loglevel.lower()=="critical") or (loglevel.lower()=="fatal") : m_level = loggin.CRITICAL
    setLevel(m_level)

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def duplicates(lst):
    """
       returns the duplicates
    """
    from collections import Counter
    cnt= Counter(lst)
    return [key for key in cnt.keys() if cnt[key]> 1]

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def duplicateIndices(lst, items= None):
    """
       gets the indices of the duplicates
    """
    from collections import defaultdict

    items, ind= set(lst) if items is None else items, defaultdict(list)
    for i, v in enumerate(lst):
        if v in items: ind[v].append(i)
    return ind

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def checkDir(directory):
    """
    Check if a directory exists. If not creates it
    """
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def shell(cmd):
    """
        shell_command(cmd):
        -------------------
        Run the `cmd` string as system command.
    """
    import os
    os.system(cmd)

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def addInQuadrature(numbers, power=2):
    """
        Add numbers in quadrature and return the sqrt(numbers[0]**2 + .... )
    """
    import math
    if p <= 0:
        return 0.
    f = lambda x: math.pow(x, p)
    s = sum(map(f, numbers))
    return math.pow(s, 1.0 / p)

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def fixString(s):
    """
        Remove special characters from the input string s
    """
    
    special =  '~!@#$%^&*()+={}\\|\'";:?><,/-. '
    for char in special:
        s = s.replace(char,'')
    return s

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def makePairCombinations(lst_a, lst_b):
    """
    Makes all combination pairs from elements of lst_a and lst_b
    Returns a list of tuples with the pairs
    """
    from itertools import product
    return list(product(lst_a, lst_b))

# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def makePairCombinationsString(lst_a, lst_b, delimeter="_"):
    """
    Makes all combination pairs from elements of lst_a and lst_b and creates a string for each pair made from 
    the element of list_a, the separation delimeter and the element of list_b.
    Returns a list of the strings
    """
    from itertools import product
    pairs = list(product(lst_a, lst_b))
    return [str(x[0])+delimeter+str(x[1]) for x in pairs]
    
# --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * --- * 

def makeRatioPlot(data1, data2, nbins=None, xmin=None,xmax=None, normed=1):
    """
    Makes a figure with top having two histograms and below the ratio of the two
    Input: data1, data2 are the data to be plotted in each histogram
    Returns: a plot...
    """
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    if(nbins is None) and (xmin is None) and (xmax is None):
        h1, bins1, patches1 = ax.hist(data1, normed=1)
        h2, bins2, patches2 = ax.hist(data2, normed=1)
    else:
        h1, bins1, patches1 = ax.hist(data1, bins=nbins, range=(xmin,xmax), normed=1)
        h2, bins2, patches2 = ax.hist(data2, bins=nbins, range=(xmin,xmax), normed=1)

    h_ratio = h1/h2




