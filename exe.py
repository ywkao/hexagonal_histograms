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

# define type id
type_pentagon_corner1 = 41
type_pentagon_corner2 = 42
type_pentagon_corner3 = 43
type_pentagon_corner4 = 44
type_pentagon_corner5 = 45
type_pentagon_corner6 = 46
type_pentagon_side1 = 51
type_pentagon_side2 = 52
type_pentagon_side3 = 53
type_pentagon_side4 = 54
type_pentagon_side5 = 55
type_pentagon_side6 = 56
type_hexagon = 6
type_circle = 12 

# coordinate of a hexagonal cell
s3 = math.sqrt(3)

base = {
	type_pentagon_side1 : {
		'x': [1*s3, 1*s3, 0, -1*s3, -1*s3, 1*s3],
	 	'y': [1, -1, -2, -1, 1, 1]
	},
	type_pentagon_side2 : {
		'x': [0, 1*s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2, -1, -2, -1, 1, 2]
	},
	type_pentagon_side3 : {
		'x': [0, 1*s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -2, -1, 1, 2]
	},
	type_pentagon_side4 : {
		'x': [0, 1*s3, 1*s3, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -1, -1, 1, 2]
	},
	type_pentagon_side5 : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, 0],
	 	'y': [2, 1, -1, -2, 1, 2]
	},
	type_pentagon_side6 : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, 0],
	 	'y': [2, 1, -1, -2, -1, 2]
	},
	type_pentagon_corner1 : {
		'x': [-1/s3, 1*s3, 1*s3, 0, -1*s3, -1/s3],
	 	'y': [1, 1, -1, -2, -1, 1]
	},
	type_pentagon_corner2 : {
		'x': [1/s3,1*s3, 0, -1*s3, -1*s3, 1/s3],
	 	'y': [1, -1, -2, -1, 1, 1]
	},
	type_pentagon_corner3 : {
		'x': [0, 2/s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2, 0, -2, -1, 1, 2]
	},
	type_pentagon_corner4 : {
		'x': [0, 1*s3, 1/s3, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -1, -1, 1, 2]
	},
	type_pentagon_corner5 : {
		'x': [0, 1*s3, 1*s3, -1/s3, -1*s3, 0],
	 	'y': [2, 1, -1, -1, 1, 2]
	},
	type_pentagon_corner6 : {
		'x': [0, 1*s3, 1*s3, 0, -2/s3, 0],
	 	'y': [2, 1, -1, -2, 0, 2]
	},
	type_hexagon : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -1, -2, -1, 1, 2]
	},
	type_circle : {
		'x': [0, 1, 1*s3, 2, 1*s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0],
	 	'y': [2, s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0, 1, s3, 2]
	},
}

# LD wafer pentagons
LD_pentapon_cells = {
	type_pentagon_side1 : [2, 3, 4, 5, 6, 7],
	type_pentagon_side2 : [18, 28, 39, 51, 65, 80, 95],
	type_pentagon_side3 : [126, 140, 155, 168, 179, 189],
	type_pentagon_side4 : [191, 192, 193, 194, 195, 196, 197],
	type_pentagon_side5 : [112, 127, 141, 156, 169, 180],
 	type_pentagon_side6 : [9, 19, 29, 40, 52, 66, 81],
	type_pentagon_corner1 : [1],
	type_pentagon_corner2 : [8],
	type_pentagon_corner3 : [111],
	type_pentagon_corner4 : [198],
	type_pentagon_corner5 : [190],
	type_pentagon_corner6 : [96],
}

LD_pentapon_cells_all = []
for i in range(type_pentagon_side1, type_pentagon_side6+1):
	LD_pentapon_cells_all += LD_pentapon_cells[i] 

# translation & rotation
global_correction_x, global_correction_y = 2*s3, -5 
global_theta = 5.*math.pi/6. # 150 degree
cos_theta, sin_theta = math.cos(global_theta), math.sin(global_theta)

# load geometry data
fin = open("./data/WaferCellMapTrg.txt", 'r')
contents = fin.readlines()[:223]
fin.close()

def get_polygon(type_polygon, nCorner, x, y):
	polygon_base = base[type_polygon]
	polygon = {}
	factor = 1. if type_polygon != type_circle else 0.6
	polygon['x'] = [ element*factor + x for element in polygon_base['x'] ]
	polygon['y'] = [ element*factor + y for element in polygon_base['y'] ]

	graph = ROOT.TGraph(nCorner+1, np.array(polygon['x']), np.array(polygon['y']))
	graph.SetTitle("")
	graph.GetXaxis().SetTitle("x (arb. unit)")
	graph.GetYaxis().SetTitle("y (arb. unit)")
	
	graph.SetMaximum(200)
	graph.SetMinimum(-200)
	graph.GetXaxis().SetLimits(-200, 200)
	return graph

# loop over all the cells
counter = 0 # how many cells are drawn
collections = {} # key, value = SiCell, graph
cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)
for i, line in enumerate(contents):
	if i==0: continue # omit heading
	if counter==UNTIL_THIS_NUMBER : break # manually control

	density, _, roc, half, seq, rocpin, str_sicell, _, _, iu, iv = tuple(line.split()[:11])
	if(iu=="-1" and iv=="-1"): continue # ignore (-1,-1)
	if(density == "HD"): break # keep only first set of LD
	sicell = int(str_sicell)

	coor = cell_helper.cellUV2XY1(int(iu), int(iv), 0, typeCoarse)
	x, y = coor[0], coor[1]

	# evaluate (r, phi) and apply rotation
	r = math.sqrt(pow(x,2)+pow(y,2))
	cos_phi, sin_phi = x/r, y/r
	xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta) + global_correction_x
	yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta) + global_correction_y
	x, y = xprime, yprime

	# create a hexagon
	type_polygon, nCorner = type_hexagon, 6
	
	if sicell in LD_pentapon_cells[type_pentagon_side1]:
		type_polygon, nCorner = type_pentagon_side1, 5
	elif sicell in LD_pentapon_cells[type_pentagon_side2]:
		type_polygon, nCorner = type_pentagon_side2, 5
	elif sicell in LD_pentapon_cells[type_pentagon_side3]:
		type_polygon, nCorner = type_pentagon_side3, 5
	elif sicell in LD_pentapon_cells[type_pentagon_side4]:
		type_polygon, nCorner = type_pentagon_side4, 5
	elif sicell in LD_pentapon_cells[type_pentagon_side5]:
		type_polygon, nCorner = type_pentagon_side5, 5
	elif sicell in LD_pentapon_cells[type_pentagon_side6]:
		type_polygon, nCorner = type_pentagon_side6, 5
	elif("CALIB" in rocpin):
		type_polygon, nCorner = type_circle, 12
	elif sicell in LD_pentapon_cells[type_pentagon_corner1]:
		type_polygon, nCorner = type_pentagon_corner1, 5
	elif sicell in LD_pentapon_cells[type_pentagon_corner2]:
		type_polygon, nCorner = type_pentagon_corner2, 5
	elif sicell in LD_pentapon_cells[type_pentagon_corner3]:
		type_polygon, nCorner = type_pentagon_corner3, 5
	elif sicell in LD_pentapon_cells[type_pentagon_corner4]:
		type_polygon, nCorner = type_pentagon_corner4, 5
	elif sicell in LD_pentapon_cells[type_pentagon_corner5]:
		type_polygon, nCorner = type_pentagon_corner5, 5
	elif sicell in LD_pentapon_cells[type_pentagon_corner6]:
		type_polygon, nCorner = type_pentagon_corner6, 5

	graph = get_polygon(type_polygon, nCorner, x, y)	
	graph.SetName("hex_%d" % sicell)
	collections[sicell] = graph
	counter+=1

	#print "counter=%d, i=%d, (iu,iv) = (%d,%d), (x,y) = (%.2f, %.2f)" % (counter, i, int(iu), int(iv), x, y)

# store graphs in order of sicell
fout = ROOT.TFile("./data/hexagons.root", "RECREATE")
for sicell, graph in collections.items():
	#print "sicell = %d" % sicell
	graph.Write()
fout.Close()

# execute root macro for TH2Poly
import subprocess
subprocess.call("root -l -b -q th2poly.C", shell=True)
