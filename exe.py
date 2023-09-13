#!/usr/bin/env python2
import argparse
import subprocess
import toolbox.polygon_manager as tp

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('-p', '--partial', help="enable produce of partial wafer", action='store_true')
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
args = parser.parse_args()

"""
Reminder: range of indices (line numbers) is decided from the text file, ./data/WaferCellMapTrg.txt
"""
if args.partial:
    waferType, beginIdx, endIdx = "partial", 667, 778
else:
    waferType, beginIdx, endIdx = "full", 1, 223

def exe(command):
    print "\n>>> executing command, ", command
    subprocess.call(command, shell=True)

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

def main():
    polygon_manager = tp.PolygonManager(waferType)
    
    # Load geometry text file
    with open("./data/WaferCellMapTrg.txt", 'r') as fin: contents = fin.readlines()[beginIdx:endIdx]
    print("[DEBUG] len(contents) = %d" % len(contents))
    
    # Inerate normal channels & non-connected channels
    for i, line in enumerate(contents):
        density, _, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, t = retrieve_info(line)
        if(iu==-1 and iv==-1): # treatment for non-connected channels
            cellType, cellIdx, cellName = "NC", polygon_manager.idxNC, "hex_nc"
            polygon_manager.idxNC += 1
        else: # default values for normal channels
            cellType, cellIdx, cellName = "", -1, "hex"
        globalId = 78*roc + 39*halfroc + seq
        channelIds = (globalId, sicell, rocpin)
        polygon_manager.run(channelIds, (iu,iv), cellType, cellIdx, cellName)
        if args.verbose: print("idx = {0}, {1}".format(i, polygon_manager))
        if polygon_manager.counter==args.n : break # manually control how many cells to display

    # Add additional cells for CM channels
    for idx, CM in enumerate(tp.tg.gcId[waferType]["CMIds"]):
        channelIds = (CM, -1, -1) # globalId, artificial sicell, rocpin
        polygon_manager.run(channelIds, (-1,-1), "CM", idx, "hex_cm")
        if args.verbose: print("idx = {0}, {1}".format(idx, polygon_manager))

    # Export geometry root file
    polygon_manager.export_root_file() # geometry root file for DQM
    polygon_manager.export_coordinate_data() # store coordinates for auxiliary lines


if __name__ == "__main__":
    main()

    if args.drawLine:
        exe("./toolbox/coordinate_loader.py") # execute python script for coordinate queries

    if args.partial:
        tag = "LD_partial_wafer"
        outputName = "DQM_LD_partial_wafer_map.png"
    else:
        tag = "LD_wafer"
        outputName = "DQM_LD_wafer_map.png"

    exe("root -l -b -q th2poly.C'(\"./data/hexagons.root\", \"%s\", 26, %d, \"%s\")'" % (outputName, args.drawLine, tag)) # execute root macro for TH2Poly

