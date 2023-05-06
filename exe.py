#!/usr/bin/env python2
import numpy as np
import math
import ROOT
ROOT.gROOT.SetBatch(True)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
args = parser.parse_args()

UNTIL_THIS_NUMBER = args.n 

# load shared library
ROOT.gInterpreter.ProcessLine('#include "include/HGCalCell.h"')
ROOT.gSystem.Load("./build/libHGCalCell.so")

# input parameters
waferSize = 60
nFine, nCoarse = 0, 10 #222
typeFine, typeCoarse = 0, 1
placementIndex = 0

# coordinate of a hexagonal cell
s3 = math.sqrt(3)
nCorner = 7 # one corner is repeated
hexagon_base = {
	'x': [2, 1, -1, -2, -1, 1, 2],
	'y': [0, -1*s3, -1*s3, 0, s3, s3, 0]
}

# load geometry data
fin = open("./data/WaferCellMapTrg.txt", 'r')
contents = fin.readlines()[:223]
fin.close()

# loop over all the cells
counter = 0 # how many cells are drawn
fout = ROOT.TFile("./data/hexagons.root", "RECREATE")
cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)
for i, line in enumerate(contents):
	if i==0: continue # omit heading
	if counter==UNTIL_THIS_NUMBER : break # manually control

	density, _, roc, half, seq, rocpin, _, _, _, iu, iv = tuple(line.split()[:11])
	if(iu=="-1" and iv=="-1"): continue # ignore (-1,-1)
	if("CALIB" in rocpin): continue # ignore calibration bins
	if(density == "HD"): break # keep only first set of LD

	coor = cell_helper.cellUV2XY1(int(iu), int(iv), 0, typeCoarse)
	x, y = coor[0], coor[1]

	hexagon = {}
	hexagon['x'] = [ element + x for element in hexagon_base['x'] ]
	hexagon['y'] = [ element + y for element in hexagon_base['y'] ]

	graph = ROOT.TGraph(nCorner, np.array(hexagon['x']), np.array(hexagon['y']))
	graph.SetTitle("")
	graph.GetXaxis().SetTitle("x (cm)")
	graph.GetYaxis().SetTitle("y (cm)")
	
	graph.SetMaximum(200)
	graph.SetMinimum(-200)
	graph.GetXaxis().SetLimits(-200, 200)
	
	graph.SetName("hex_%d"%i)
	graph.Write()

	counter+=1

	print "counter=%d, i=%d, (iu,iv) = (%d,%d), (x,y) = (%.2f, %.2f)" % (counter, i, int(iu), int(iv), x, y)

fout.Close()

# execute root macro for TH2Poly
import subprocess
subprocess.call("root -l -b -q th2poly.C", shell=True)
