#!/bin/bash
#takes one argument: spin


#JHU exe
#change this to your JHU install dir
#JHU=/project/atlas/users/dhohn/JHUGenerator
JHU=/project/atlas/users/dhohn/JHUGenerator.v2.2.6/JHUGenerator


#spin arg
SPIN=$1
PARITY=p

DIR=$(pwd)


cd $JHU

#generate events in lhe file

for i in 0 1 2 3 4 5 6 7 8 9
do
  FILE=qqH${SPIN}${PARITY}_$i
  ./JHUGen Collider=1 Process=$SPIN VegasNc1=1000000 PChannel=1 OffXVV=011 DecayMode1=4 DecayMode2=4 DataFile=$FILE
  #Collider 1 is LHC
  #Process is spin
#Pchannel 0 is ggF, 1 is qqH
  #DecayMode=4 is W->lnu
done

rm -f *.dat
mv *.lhe $DIR



cd $PWD