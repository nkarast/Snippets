#!/usr/bin/python
 
import sys
import re
 
class Compatibility:
  pass
args = Compatibility
 
if sys.version_info < (2,7):
  if len(sys.argv)<4:
    print("splitLHE.py requires 3 command line arguments, inputFile ouFileNameBase and nFiles" )
    sys.exit(1)
  args.inputFile = sys.argv[1]
  args.outFileNameBase = sys.argv[2]
  args.nFiles = int(sys.argv[3])
else:
  import argparse
  parser = argparse.ArgumentParser(description="Splits LHE events from input file into N output files")
  parser.add_argument("inputFile",help="Input LHE file name")
  parser.add_argument("outFileNameBase",help="Output LHE file name Base (a number and .lhe will be added to it)")
  parser.add_argument("nFiles",help="Number of files to split the events between",type=int)
 
  args = parser.parse_args()
 
if args.nFiles < 2:
  print("Error: nFiles must be > 1")
  sys.exit(1)
 
fin = ""
try:
  fin = open(args.inputFile)
except:
  print("Error: Input file: %s could not be opened, exiting." % args.inputFile)
  sys.exit(1)
 
eventNum = 0
init = False
inFooter = False
footLines = []
for line in fin:
  if re.match(r"[^#]*</LesHouchesEvents>",line):
    inFooter = True
    footLines.append(line)
  elif inFooter:
    footLines.append(line)
  elif init:  
    if re.match(r"[^#]*</event>",line):
      eventNum += 1
  elif re.match(r"[^#]*</init>",line):
    init = True
 
eventsTotal = eventNum
print "N Events Total: %i" % eventsTotal
 
files = []
maxEventsFile = []
for i in range(args.nFiles):
  s=i+1
  number = "%05d"%s
  tmp = open(args.outFileNameBase+number+".events",'w')
  files.append(tmp)
  maxEventsFile.append(eventsTotal/args.nFiles)
maxEventsFile[len(maxEventsFile)-1] += eventsTotal % args.nFiles
 
eventNum = 0
eventNumThisFile = 0
init = False
headLines = []
iFile = 0
fin.seek(0)
for line in fin:
  if init:  
    files[iFile].write(line)
    if re.match(r"[^#]*</event>",line):
      eventNum += 1
      eventNumThisFile += 1
      if eventNumThisFile >= maxEventsFile[iFile]:
        files[iFile].writelines(footLines)
        iFile += 1
        eventNumThisFile = 0
        if iFile == args.nFiles:
          break
        files[iFile].writelines(headLines)
  elif re.match(r"[^#]*</init>",line):
    init = True
    headLines.append(line)
    files[iFile].writelines(headLines)
  else:
    headLines.append(line)
 
for f in files:
  f.close()
