#!/usr/bin/env python2
import ROOT
ROOT.gROOT.SetBatch(True)

def pad2ElecID(pad):
	padmap = pandas.read_csv('./data/ld_pad_to_channel_mapping.csv')
	padmap = padmap [ padmap['PAD']==pad ]
	chip=padmap['ASIC'].max()
	rocchannel = padmap['Channel'].max()
	channeltype = padmap['Channeltype'].max()
	half, channel = -1, -1
	if padmap['Channeltype'].max()==0:
		if padmap['Channel'].max()>=36:
			half = 1
			channel = padmap['Channel'].max()-36
		else:
			half = 0
			channel = padmap['Channel'].max()
	elif padmap['Channeltype'].max()==1:
		half = padmap['Channel'].max()
		channel = 36

	globalchannelId = chip*78 + half*39+ channel
	return globalchannelId,chip,half,channel,rocchannel,channeltype

def pad2ElecID2(pad):
	padmap = table[pad]
	chip = int(padmap[0])
	rocchannel = int(padmap[1])
	channeltype = int(padmap[2])
	half, channel = -1, -1
	if channeltype==0:
		if rocchannel>=36:
			half = 1
			channel = rocchannel-36
		else:
			half = 0
			channel = rocchannel
	elif channeltype==1:
		half = rocchannel
		channel = 18

	globalchannelId = chip*78 + half*39+ channel
	return globalchannelId,chip,half,channel,rocchannel,channeltype

def test_and_validate_global_channel_id():
	''' conclusion of cross-check:
	globalId shows that 8, 17, 18, 27, 37, 38 are not in the list.
	They are very likely corresponding to CM and non-connected channels.
	'''
	global_channelId_dict = {} # key = global channel Id, value = padId
	global_channelId_list = []
	message = "padId globalChId chip half channel rocchannel channeltype"
	#print(message)
	for pad in range(1,199):
		output = pad2ElecID2(pad)
		#print("{0} {1}".format(pad,output))

		globalchannelId, _, _, _, _, _ = pad2ElecID2(pad)
		#print("{0} {1}".format(pad, globalchannelId))
		global_channelId_list.append(globalchannelId)
		global_channelId_dict[globalchannelId] = pad

	print("# global_channel_Id, padId")
	global_channelId_list.sort()
	for idx in global_channelId_list:
		print("{0},{1}".format(idx, global_channelId_dict[idx]))

if __name__ == "__main__":
	#--------------------------------------------------
	# load data/WaferCellMapTrg.txt
	#--------------------------------------------------
	with open('./data/WaferCellMapTrg.txt', 'r') as fin: contents = fin.readlines()

	#print "# globalchannelId roc halfroc seq sicell t"
	print "# globalchannelId, padId"
	for line in contents[1:223]:
		_, _, roc, halfroc, seq, _, sicell, _, _, _, _, t = tuple([str(ele) if "LD" in ele or "CALIB" in ele else int(ele) for ele in line.strip().split()])
		if sicell==-1: continue
		globalchannelId = 78*roc + 39*halfroc + seq
		print "%d,%d" % (globalchannelId, sicell)
		#print "%3d %d %d %2d %2d %2d" % (globalchannelId, roc, halfroc, seq, sicell, t)

	exit()

	#--------------------------------------------------
	# load ld_pad_to_channel_mapping.csv
	#--------------------------------------------------
	table = {}
	with open('./data/ld_pad_to_channel_mapping.csv', 'r') as fin: contents = fin.readlines()
	for line in contents:
		if 'PAD' in line: continue
		LoI = line.strip().split(',') # list of items
		#pad, chip, rocchannel, channelType = int(LoI[0]), LoI[1], LoI[2], LoI[3]
		pad = int(LoI[0])
		table[pad] = LoI[1:]

	test_and_validate_global_channel_id()

	exit()

	#--------------------------------------------------
	# th2poly
	#--------------------------------------------------
	c1 = ROOT.TCanvas("c1", "", 900, 900)
	c1.SetRightMargin(0.15)
	ROOT.gStyle.SetPaintTextFormat(".0f")
	fin = ROOT.TFile.Open("./data/hexagons.root", "R")

	scope = 24
	p = ROOT.TH2Poly("hexagonal histograms", "Low density wafer map with global channel id", -1*scope, scope, -1*scope-2, scope-2)
	p.SetStats(0)
	p.GetXaxis().SetTitle("x (cm)")
	p.GetYaxis().SetTitle("y (cm)")
	p.GetYaxis().SetTitleOffset(1.1)

	counter = 0
	for key in ROOT.gDirectory.GetListOfKeys():
		obj = key.ReadObj()
		if obj.InheritsFrom("TGraph"):
			gr = obj
			p.AddBin(gr)
			counter+=1

	print(">>> counter = {0}".format(counter))
	for pad in range(1, 199):
 		globalchannelId, _, _, _, _, _ = pad2ElecID2(pad)
		if globalchannelId==0:
			p.SetBinContent(pad, 0.000001)
		else:
			p.SetBinContent(pad, globalchannelId)

	CMIds = [37, 38, 76, 77, 115, 116, 154, 155, 193, 194, 232, 233]
	for pad in range(199, 211):
		p.SetBinContent(pad, CMIds[pad-199])

	p.SetMarkerSize(0.7)
	p.Draw("colztext")

	outputfile = "output_wafer_map_with_global_channelId.png"
	c1.SaveAs(outputfile)
