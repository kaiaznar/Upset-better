from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import sys
import os

Z='kai'
E1='Aznar'
wDir=os.getcwd()
fileTxt=wDir + '\' + 'txtTeste.txt'
open(105,file=fileTxt,position='append')
WRITE(105,*)Z,E1
close(105)