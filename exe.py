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
arbUnit_to_cm = 17./24.
waferSize = 60 * arbUnit_to_cm
nFine, nCoarse = 0, 10 #222
typeFine, typeCoarse = 0, 1
placementIndex = 0

# parameter and coordinate of a hexagonal cell
import toolbox.geometry as tg
s3 = tg.s3
base = tg.base

# LD wafer pentagons
LD_special_polygonal_cells = tg.LD_special_polygonal_cells
LD_special_polygonal_cells_all = tg.LD_special_polygonal_cells_all

# global translation & rotation
global_correction_x, global_correction_y = 2*s3, -5 
global_theta = 5.*math.pi/6. # 150 degree
cos_global_theta, sin_global_theta = math.cos(global_theta), math.sin(global_theta)

# for auxiliary boundary lines on the wafer map
import json
dict_my_coordinate_data = {} # key = sicell, value = dict_polygon_coordinates

def get_polygon(sicell, type_polygon, nCorner, x, y, isCM=False, isNC=False):
	polygon_base = base[type_polygon]
	polygon = {}

	resize_factor = 1.0
	if isCM:
		resize_factor = 0.6
	elif isNC:
		resize_factor = 0.4

	polygon['x'] = [ element*arbUnit_to_cm*resize_factor + x for element in polygon_base['x'] ]
	polygon['y'] = [ element*arbUnit_to_cm*resize_factor + y for element in polygon_base['y'] ]

	dict_my_coordinate_data[sicell] = polygon

	graph = ROOT.TGraph(nCorner+1, np.array(polygon['x']), np.array(polygon['y']))
	graph.SetTitle("")
	graph.GetXaxis().SetTitle("x (arb. unit)")
	graph.GetYaxis().SetTitle("y (arb. unit)")
	
	graph.SetMaximum(200)
	graph.SetMinimum(-200)
	graph.GetXaxis().SetLimits(-200, 200)
	return graph

# utility
counter = 0 # how many cells are drawn
collections = {} # key, value = SiCell, graph
cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)

# load geometry data
fin = open("./data/WaferCellMapTrg.txt", 'r')
#contents = fin.readlines()[:223] # full LD
contents = fin.readlines()[667:778] # partial LD3
fin.close()

def retrieve_info(line):
    info = line.strip().split()
    result = []
    for ele in info:
        if "LD" in ele or "CALIB" in ele:
            result.append(str(ele))
        elif "." in ele:
            result.append(float(ele))
        else:
            result.append(int(ele))
    return tuple(result)

# loop over all the cells
for i, line in enumerate(contents):
	if 'Seq' in line: continue # omit heading
	if counter==UNTIL_THIS_NUMBER : break # manually control

	density, _, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, t = retrieve_info(line)
	if(iu==-1 and iv==-1): continue # ignore (-1,-1)
	if(density == "HD"): break # keep only first set of LD

	globalId = 78*roc + 39*halfroc + seq

	# # print globalId vs HGCROC pin
	# print("{{{0},{1}}},").format(globalId, rocpin)

	# print globalId vs padId
	print("{{{0},{1}}},").format(globalId, sicell)
	
	coor = cell_helper.cellUV2XY1(int(iu), int(iv), 0, typeCoarse)
	x, y = coor[0], coor[1]

	# evaluate (r, phi) and apply rotation
	r = math.sqrt(pow(x,2)+pow(y,2))
	cos_phi, sin_phi = x/r, y/r
	xprime = r*(cos_phi*cos_global_theta + sin_phi*sin_global_theta) + global_correction_x
	yprime = r*(sin_phi*cos_global_theta - cos_phi*sin_global_theta) + global_correction_y
	x, y = xprime, yprime

	# create a hexagon
	type_polygon, nCorner = tg.type_hexagon, 6
	
	if sicell in LD_special_polygonal_cells[tg.type_hexagon_corner1]:
		type_polygon, nCorner = tg.type_hexagon_corner1, 6
	elif sicell in LD_special_polygonal_cells[tg.type_hexagon_corner2]:
		type_polygon, nCorner = tg.type_hexagon_corner2, 6
	elif sicell in LD_special_polygonal_cells[tg.type_hexagon_corner3]:
		type_polygon, nCorner = tg.type_hexagon_corner3, 6
	elif sicell in LD_special_polygonal_cells[tg.type_hexagon_corner4]:
		type_polygon, nCorner = tg.type_hexagon_corner4, 6
	elif sicell in LD_special_polygonal_cells[tg.type_hexagon_corner5]:
		type_polygon, nCorner = tg.type_hexagon_corner5, 6
	elif sicell in LD_special_polygonal_cells[tg.type_hexagon_corner6]:
		type_polygon, nCorner = tg.type_hexagon_corner6, 6

	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side1]:
		type_polygon, nCorner = tg.type_pentagon_side1, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side2]:
		type_polygon, nCorner = tg.type_pentagon_side2, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side3]:
		type_polygon, nCorner = tg.type_pentagon_side3, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side4]:
		type_polygon, nCorner = tg.type_pentagon_side4, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side5]:
		type_polygon, nCorner = tg.type_pentagon_side5, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_side6]:
		type_polygon, nCorner = tg.type_pentagon_side6, 5

	elif sicell in tg.hollow_cells:
		type_polygon, nCorner = tg.type_hollow, 14 
	elif(isinstance(rocpin, str)): # "CALIB"
		type_polygon, nCorner = tg.type_hexagon_small, 6 
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner1]:
		type_polygon, nCorner = tg.type_pentagon_corner1, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner2]:
		type_polygon, nCorner = tg.type_pentagon_corner2, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner3]:
		type_polygon, nCorner = tg.type_pentagon_corner3, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner4]:
		type_polygon, nCorner = tg.type_pentagon_corner4, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner5]:
		type_polygon, nCorner = tg.type_pentagon_corner5, 5
	elif sicell in LD_special_polygonal_cells[tg.type_pentagon_corner6]:
		type_polygon, nCorner = tg.type_pentagon_corner6, 5

	graph = get_polygon(sicell, type_polygon, nCorner, x, y)	
	graph.SetName("hex_%d" % sicell)
	#collections[sicell] = graph
	collections[globalId] = graph
	counter+=1

	#print "counter=%d, i=%d, (iu,iv) = (%d,%d), (x,y) = (%.2f, %.2f)" % (counter, i, int(iu), int(iv), x, y)

# Add additional cells for CM channels
CMIds = [37, 38, 76, 77, 115, 116, 154, 155, 193, 194, 232, 233]
for idxCM in range(12):
	if idxCM%2==0: # CM0
		type_polygon, nCorner = tg.type_regular_pentagon, 5
	else: # CM1
		type_polygon, nCorner = tg.type_square, 4

	# assign coordinates
	correction_fine_tune_y_coordinate = 2. if idxCM//4 == 0 else 0.
	x = tg.Coordinates_CM_channels['x'][idxCM%4]*arbUnit_to_cm
	y = tg.Coordinates_CM_channels['y'][idxCM%4]*arbUnit_to_cm - correction_fine_tune_y_coordinate*arbUnit_to_cm
	theta = 2*math.pi/3. * (idxCM//4) - math.pi/3.
	cos_theta = math.cos(theta)
	sin_theta = math.sin(theta)

	# evaluate (r, phi) and apply rotation
	r = math.sqrt(pow(x,2)+pow(y,2))
	cos_phi, sin_phi = x/r, y/r
	xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
	yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)
	x, y = xprime, yprime

	sicell = 198+1+idxCM # artificial sicell for CM channels
	globalId = CMIds[idxCM]

	graph = get_polygon(sicell, type_polygon, nCorner, x, y, True)	
	graph.SetName("hex_cm_%d" % idxCM)
	#collections[sicell] = graph
	collections[globalId] = graph
	counter+=1

# Add additional cells for NC channels
NonConnIds = [8, 17, 19, 28, 47, 56, 58, 67, 86, 95, 97, 106, 125, 134, 136, 145, 164, 173, 175, 184, 203, 212, 214, 223]
for idxNC in range(24):
	#type_polygon, nCorner = tg.type_triangle, 3
	type_polygon, nCorner = tg.type_circle, 12 
	x = tg.Coordinates_NC_channels['x'][idxNC%8]*arbUnit_to_cm
	y = tg.Coordinates_NC_channels['y'][idxNC%8]*arbUnit_to_cm
	theta = 2*math.pi/3. * (idxNC//8) - math.pi/3.
	cos_theta = math.cos(theta)
	sin_theta = math.sin(theta)

	# evaluate (r, phi) and apply rotation
	r = math.sqrt(pow(x,2)+pow(y,2))
	cos_phi, sin_phi = x/r, y/r
	xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
	yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)
	x, y = xprime, yprime

	sicell = 198+1+12+idxNC # artificial sicell for NC channels
	globalId = NonConnIds[idxNC]

	graph = get_polygon(sicell, type_polygon, nCorner, x, y, False, True)	
	graph.SetName("hex_nc_%d" % idxNC)
	collections[globalId] = graph
	counter+=1

# store graphs in order of key (sicell or globalId)
fout = ROOT.TFile("./data/hexagons.root", "RECREATE")
for key, graph in collections.items():
	graph.Write()
	#if key>=78: break
fout.Close()

# store coordinates
with open("data/output_my_coordinate_data.json", 'w') as f:
	json.dump(dict_my_coordinate_data, f, indent=4)

#--------------------------------------------------
# external execute
#--------------------------------------------------
import subprocess

def exe(command):
	print "\n>>> executing command, ", command
	subprocess.call(command, shell=True)

# # execute python script for coordinate queries
# exe("./toolbox/coordinate_loader.py")

# execute root macro for TH2Poly
#exe("root -l -b -q th2poly.C'(\"./data/hexagons.root\", \"DQM_LD_wafer_map.pdf\", 26, 1)'")
exe("root -l -b -q th2poly.C'(\"./data/hexagons.root\", \"DQM_partial_LD3_wafer_map.pdf\", 26, 1)'")
