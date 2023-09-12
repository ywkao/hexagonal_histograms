#!/usr/bin/env python2
import argparse
import subprocess
import toolbox.polygon_manager as tp

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('--partial', help="enable produce of partial wafer", action='store_true')
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
args = parser.parse_args()

if args.partial:
    waferType, beginIdx, endIdx = "partial", 667, 778
else:
    waferType, beginIdx, endIdx = "full", 0, 223

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
    """ load geometry data & loop over all cells """
    polygon_manager = tp.PolygonManager(waferType)
    
    fin = open("./data/WaferCellMapTrg.txt", 'r')
    contents = fin.readlines()[beginIdx:endIdx]
    fin.close()

    print("[DEBUG] len(contents) = %d" % len(contents))
    
    for i, line in enumerate(contents):
        if 'Seq' in line: continue # omit heading
        if polygon_manager.counter==args.n : break # manually control how many cells to display
    
        density, _, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, t = retrieve_info(line)
        if(iu==-1 and iv==-1): continue # ignore non-connected channels
        if(density == "HD"): break # keep only first set of LD
    
        globalId = 78*roc + 39*halfroc + seq
        channelIds = (globalId, sicell, rocpin)
        polygon_manager.run(channelIds, (iu,iv))
        print("idx = {0}, {1}".format(i, polygon_manager))

    # Add additional cells for CM channels
    for idx, CM in enumerate(tp.tg.gcId[waferType]["CMIds"]):
        channelIds = (CM, 198+1+idx, -1) # globalId, artificial sicell, rocpin
        polygon_manager.run(channelIds, (-1,-1), "CM", idx, "hex_cm")
        print("idx = {0}, {1}".format(idx, polygon_manager))

    # Add additional cells for NC channels
    for idx, NC in enumerate(tp.tg.gcId[waferType]["NonConnIds"]):
        channelIds = (NC, 198+1+12+idx, -1) # globalId, artificial sicell, rocpin
        polygon_manager.run(channelIds, (-1,-1), "NC", idx, "hex_nc")
        print("idx = {0}, {1}".format(idx, polygon_manager))

        """ CAVEAT: need to fix RocPin for NC """
    
    polygon_manager.export_root_file() # geometry root file for DQM
    polygon_manager.export_coordinate_data() # store coordinates for auxiliary lines


if __name__ == "__main__":
    main()

    if args.drawLine:
        exe("./toolbox/coordinate_loader.py") # execute python script for coordinate queries

    exe("root -l -b -q th2poly.C'(\"./data/hexagons.root\", \"DQM_LD_wafer_map.pdf\", 26, %d)'" % (args.drawLine)) # execute root macro for TH2Poly

