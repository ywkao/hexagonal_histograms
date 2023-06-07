#!/usr/bin/env python2
import numpy as np
import json
import ROOT
ROOT.gROOT.SetBatch(True)

fin = open("data/ldv3_geometry.json")
dict_features = json.load(fin)
list_cells = dict_features["features"]

counter = 0
collections = {} # key, value = SiCell, graph
for i, element in enumerate(list_cells):
	# load data
	rocId, channelId, _ = tuple(map(int, element["properties"]["chan_id"][1:-1].split(", ")))
	list_points = element["geometry"]["coordinates"][0]

	# extract info
	globalChannelId = 100*rocId + channelId
	nPoints = len(list_points)

	polygon = {}
	polygon['x'] = [coor[0] for coor in list_points]
	polygon['y'] = [coor[1] for coor in list_points]

	# create graph
	graph = ROOT.TGraph(nPoints, np.array(polygon['x']), np.array(polygon['y']))

	graph.SetTitle("")
	graph.GetXaxis().SetTitle("x (arb. unit)")
	graph.GetYaxis().SetTitle("y (arb. unit)")
	
	graph.SetMaximum(200)
	graph.SetMinimum(-200)
	graph.GetXaxis().SetLimits(-200, 200)

	graph.SetName("hex_%d" % globalChannelId)
	collections[globalChannelId] = graph
	counter+=1

	#print counter, globalChannelId

# store graphs in order of sicell
fout = ROOT.TFile("./data/hexagons_from_testbeam_json.root", "RECREATE")
for sicell, graph in collections.items():
	#print "sicell = %d" % sicell
	graph.Write()
fout.Close()

# execute root macro for TH2Poly
import subprocess
subprocess.call("root -l -b -q th2poly.C'(\"./data/hexagons_from_testbeam_json.root\", \"output_from_testbeam_json.png\", 10)'", shell=True)
