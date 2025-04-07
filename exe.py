#!/usr/bin/env python3
import math
import argparse
import subprocess
from utils.geometry import gcId
from utils.polygon_manager import PolygonManager
from utils.config_handler import load_wafer_contents, get_macro_arguments, get_exported_file_names
from utils.auxiliary_line_producer import AuxiliaryLineProducer

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('-w', '--waferType', help="set wafer type (full, LD3, LD4, HD)", type=str, default="full")
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
args = parser.parse_args()

"""
Reminder: range of indices (line numbers) is decided from the text file, ./data/input/WaferCellMapTrg.txt
"""
def exe(command):
    print("\n>>> executing command, ", command)
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

def main(extra_angle, offset_x, offset_y):
    global args
    polygon_manager = PolygonManager(args.waferType, extra_angle, offset_x, offset_y)
    
    # Load geometry text file
    contents = load_wafer_contents(args.waferType)
    print("[DEBUG] len(contents) = %d" % len(contents))
    
    # Loop over normal channels & non-connected channels
    for i, line in enumerate(contents):
        density, _, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, t = retrieve_info(line)
        if(iu==-1 and iv==-1): # treatment for non-connected channels
            cellType, cellIdx, cellName = "NC", polygon_manager.idxNC, "hex_nc"
            polygon_manager.idxNC += 1
        else: # default values for normal channels
            cellType, cellIdx, cellName = "", -1, "hex"
        globalId = 78*roc + 39*halfroc + seq
        channelIds = (globalId, sicell, rocpin)
        polygon_manager.create_and_register_polygon(channelIds, (iu,iv), cellType, cellIdx, cellName)
        if args.verbose: print(polygon_manager)
        if polygon_manager.counter==args.n : break # manually control how many cells to display

    # Add additional cells for CM channels
    for idx, CM in enumerate(gcId[args.waferType]["CMIds"]):
        channelIds = (CM, -1, -1) # globalId, artificial sicell, rocpin
        polygon_manager.create_and_register_polygon(channelIds, (-1,-1), "CM", idx, "hex_cm")
        if args.verbose: print(polygon_manager)

    # Export geometry data
    geometry_rootfile, coordinate_json, mapping_json = get_exported_file_names(args.waferType)
    polygon_manager.export_root_file(geometry_rootfile) # geometry root file for DQM
    polygon_manager.export_coordinate_data(coordinate_json) # store coordinates for auxiliary lines
    polygon_manager.export_channel_id_mapping(mapping_json) # store chIds for information wafer map


if __name__ == "__main__":
    #----------------------------------------------------------------------------------------------------
    # generate wafermap geometry root files
    #----------------------------------------------------------------------------------------------------
    extra_rotation_tb2024 = 0.
    main(extra_rotation_tb2024, -1.20840 , 2.09301)

    #----------------------------------------------------------------------------------------------------
    # create plots using C++ root macro (validation for CMSSW DQMEDAnalyzer and DQM GUI rendering plugins)
    #----------------------------------------------------------------------------------------------------
    rotationTag = ""
    if(extra_rotation_tb2024==5*math.pi/6.):
        rotationTag = "_rotation150"
    if(extra_rotation_tb2024==math.pi/6.):
        rotationTag = "_rotation30"

    geometry_rootfile, coordinate_json, _ = get_exported_file_names(args.waferType)
    if args.drawLine:
        producer = AuxiliaryLineProducer(args.waferType, coordinate_json)
        producer.create_cpp_headers()

    scope, tag, outputName, markerSize = get_macro_arguments(args.waferType)
    exe(f"root -l -b -q th2poly.C'(\"{geometry_rootfile}\", \"{outputName}\", {scope}, {int(args.drawLine)}, \"{tag}\", {markerSize}, \"{rotationTag}\")'") # execute root macro for TH2Poly

