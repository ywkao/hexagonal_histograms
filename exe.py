#!/usr/bin/env python2
import argparse
import subprocess
import toolbox.polygon_manager as tp

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('-w', '--waferType', help="set wafer type (partial, full, HD)", type=str, default="full")
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
args = parser.parse_args()

"""
Reminder: range of indices (line numbers) is decided from the text file, ./data/WaferCellMapTrg.txt
"""
if args.waferType == "HD":
    waferType, beginIdx, endIdx = "HD", 223, 667
elif args.waferType == "full": # LD full
    waferType, beginIdx, endIdx = "full", 1, 223
elif args.waferType == "partial": # LD3
    waferType, beginIdx, endIdx = "partial", 667, 778

def exe(command):
    print "\n>>> executing command, ", command
    subprocess.call(command, shell=True)

def retrieve_info(line):
    info = line.strip().split()
    result = []
    for ele in info:
        if "LD" in ele or "HD" in ele or "CALIB" in ele:
            result.append(str(ele))
        elif "." in ele:
            result.append(float(ele))
        else:
            result.append(int(ele))
    return tuple(result)

def get_macro_arguments():
    # Reminder: outputName is not used for the moment
    if args.waferType == "partial":
        scope = 14
        markerSize = 0.7
        tag = "LD3_partial_wafer"
        outputName = "waferMaps/DQM_LD_partial_wafer_map.png"
    elif args.waferType == "full":
        scope = 14
        markerSize = 0.7
        tag = "LD_wafer"
        outputName = "waferMaps/DQM_LD_wafer_map.png"
    elif args.waferType == "HD":
        scope = 12
        markerSize = 0.5
        tag = "HD_wafer"
        outputName = "waferMaps/DQM_HD_wafer_map.png"

    return scope, tag, outputName, markerSize

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
        if args.verbose: print(polygon_manager)
        if polygon_manager.counter==args.n : break # manually control how many cells to display

    # Add additional cells for CM channels
    for idx, CM in enumerate(tp.tg.gcId[waferType]["CMIds"]):
        channelIds = (CM, -1, -1) # globalId, artificial sicell, rocpin
        polygon_manager.run(channelIds, (-1,-1), "CM", idx, "hex_cm")
        if args.verbose: print(polygon_manager)

    # Export geometry root file
    polygon_manager.export_root_file() # geometry root file for DQM
    polygon_manager.export_coordinate_data() # store coordinates for auxiliary lines
    polygon_manager.export_cpp_id_mapping() # store chIds for information wafer map


if __name__ == "__main__":
    main()

    if args.drawLine:
        exe("./toolbox/coordinate_loader.py -w %s" % args.waferType)

    scope, tag, outputName, markerSize = get_macro_arguments()
    exe("root -l -b -q th2poly.C'(\"./data/hexagons.root\", \"%s\", %d, %d, \"%s\", %f)'" % (outputName, scope, args.drawLine, tag, markerSize)) # execute root macro for TH2Poly

