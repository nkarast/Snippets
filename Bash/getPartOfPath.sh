#!/bin/bash

#
#
#	Assume a directory in the form of 
#	/afs/cern.ch/user/n/nkarast/work/sixdesk/track/hl12_sample_tunescan/17/simul/62.31_60.32/6-14/e5/.1
#	and I need the n-3 part of the path in a variable called myname.
#

dir=/afs/cern.ch/user/n/nkarast/work/sixdesk/track/hl12_sample_tunescan/17/simul/62.31_60.32/6-14/e5/.1
myname = `echo $dir | awk -F/ '{print $(NF-3)}'