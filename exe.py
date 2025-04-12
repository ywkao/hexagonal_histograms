#!/usr/bin/env python3
import os, math
import argparse
import subprocess
from utils.data_loader import WaferDataLoader
from utils.polygon_manager import PolygonManager
from utils.config_handler import get_macro_arguments, get_exported_file_names, get_type_config
from utils.auxiliary_line_producer import AuxiliaryLineProducer
from utils.special_channels import gcId

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('-t', '--waferType', help="wafer type code (ML-F, MH-F, etc.)", type=str, default="ML-F")
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
parser.add_argument('--listTypes', help="list available type codes", action='store_true')
parser.add_argument('--rotation', choices=['0', '30', '150'], default='0', help="Rotation angle in degrees (0, 30, or 150)")
args = parser.parse_args()

def main(extra_angle):
    global args

    # Initialize data loader
    data_loader = WaferDataLoader()

    # List available types if requested
    if args.listTypes:
        print("Available type codes:")
        for code in data_loader.get_all_type_codes():
            print(f"  {code}")
        return

    # Get type-specific configuration
    type_config = get_type_config(args.waferType)
    offset_x = type_config.get('offset_x', 0.0)
    offset_y = type_config.get('offset_y', 0.0)

    # Initialize polygon manager
    polygon_manager = PolygonManager(args.waferType, extra_angle, offset_x, offset_y)

    # Get data for specified type
    contents = data_loader.get_data_as_lines(args.waferType)
    print(f"[DEBUG] Processing {args.waferType}, len(contents) = {len(contents)}")

    # Loop over normal channels & non-connected channels
    for i, line in enumerate(contents):
        density, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, _, t = data_loader.retrieve_info(line)
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
    # create output directories & decide rotation angle
    # (non-default angles of 30° and 150° are for testing alternative orientations)
    #----------------------------------------------------------------------------------------------------
    os.makedirs("output/coordinates", exist_ok=True)
    os.makedirs("output/mapping", exist_ok=True)
    os.makedirs("output/geometry", exist_ok=True)
    os.makedirs("output/waferMaps", exist_ok=True)

    if args.rotation == '0':
        extra_rotation_tb2024, rotationTag = 0., ""
    elif args.rotation == '30':
        extra_rotation_tb2024, rotationTag = math.pi/6., "_rotation30"
    elif args.rotation == '150':
        extra_rotation_tb2024, rotationTag = 5*math.pi/6., "_rotation150"

    #--------------------------------------------------
    # generate wafermap geometry root files
    #--------------------------------------------------
    main(extra_rotation_tb2024)
    if args.listTypes: exit()

    #--------------------------------------------------
    # create a c++ header file for auxiliary lines
    #--------------------------------------------------
    geometry_rootfile, coordinate_json, _ = get_exported_file_names(args.waferType)
    if args.drawLine:
        producer = AuxiliaryLineProducer(args.waferType, coordinate_json)
        producer.create_cpp_headers()

    #--------------------------------------------------
    # execute root macro for TH2Poly
    #--------------------------------------------------
    scope, tag, outputName, markerSize = get_macro_arguments(args.waferType)
    command = f"root -l -b -q ./scripts/generate_wafer_maps.C'(\"{geometry_rootfile}\", \"{outputName}\", {scope}, {int(args.drawLine)}, \"{tag}\", {markerSize}, \"{rotationTag}\")'"
    print(f"running command: {command}")
    subprocess.call(command, shell=True)
