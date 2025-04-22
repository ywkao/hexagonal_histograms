#!/usr/bin/env python3
import os, math, subprocess
from utils.data_loader import WaferDataLoader
from utils.polygon_manager import PolygonManager
from utils.config_handler import setup_parser, setup_logging
from utils.config_handler import get_macro_arguments, get_exported_file_names, get_type_config
from utils.auxiliary_line_producer import AuxiliaryLineProducer
from utils.special_channels import gcId

def main(args, logger):
    #----------------------------------------------------------------------
    # Initialize data loader
    #----------------------------------------------------------------------
    data_loader = WaferDataLoader()

    # List available types if requested
    if args.listTypes:
        print("Available type codes:")
        for code in data_loader.get_all_type_codes():
            print(f"  {code}")
        return

    #----------------------------------------------------------------------
    # Initialize polygon manager & Get data for specified type
    #----------------------------------------------------------------------
    type_config = get_type_config(args.waferType)
    offset_x = type_config.get('offset_x', 0.0)
    offset_y = type_config.get('offset_y', 0.0)
    extra_angle = math.pi/6 if args.rotation == '30' else 5*math.pi/6 if args.rotation == '150' else 0

    # Initialize polygon manager
    polygon_manager = PolygonManager(args.waferType, extra_angle, offset_x, offset_y)

    # skip NC and CM if they are not registered
    nc_channels_are_registered = (args.waferType in gcId and "NonConnIds" in gcId[args.waferType])
    cm_channels_are_registered = (args.waferType in gcId and "CMIds" in gcId[args.waferType])
    if not nc_channels_are_registered: logger.warning(f"No NC channel information found for wafer type {args.waferType}")
    if not cm_channels_are_registered: logger.warning(f"No CM channel information found for wafer type {args.waferType}")

    # Get data for specified type
    contents = data_loader.get_data_as_lines(args.waferType)
    logger.info(f"Processing {args.waferType}, len(contents) = {len(contents)}")

    #----------------------------------------------------------------------
    # Loop over normal channels & non-connected channels
    #----------------------------------------------------------------------
    for i, line in enumerate(contents):
        density, roc, halfroc, seq, rocpin, sicell, _, _, iu, iv, _, t = data_loader.retrieve_info(line)

        # identify non-connected channels using (iu,iv) == (-1,-1)
        if(iu==-1 and iv==-1):
            cellType, cellIdx, cellName = "NC", polygon_manager.idxNC, "hex_nc"
            polygon_manager.idxNC += 1
            # if not nc_channels_are_registered: continue
        else: 
            cellType, cellIdx, cellName = "", -1, "hex"

        # evaluate channel Ids & create a polygon
        globalId = 78*roc + 39*halfroc + seq
        channelIds = (globalId, sicell, rocpin)
        polygon_manager.create_and_register_polygon(channelIds, (iu,iv), cellType, cellIdx, cellName)
        logger.debug(polygon_manager)
        if polygon_manager.counter==args.n : break # manually control how many cells to display

    logger.debug(f"Number of unconnected channels: {polygon_manager.idxNC}")
    logger.debug(f"Number of registered channels: {polygon_manager.counter}")
    logger.debug(f"Number of expected CM groups: {int(polygon_manager.counter/37)}")

    # Add additional cells for CM channels
    if cm_channels_are_registered:
        for idx, CM in enumerate(gcId[args.waferType]["CMIds"]):
            channelIds = (CM, -1, -1) # globalId, artificial sicell, rocpin
            polygon_manager.create_and_register_polygon(channelIds, (-1,-1), "CM", idx, "hex_cm")
            logger.debug(polygon_manager)

    else:
        cm_groups = int(polygon_manager.counter/37)
        for idx in range(cm_groups):
            channelIds = (37+idx*39, -1, -1) # globalId, artificial sicell, rocpin
            polygon_manager.create_and_register_polygon(channelIds, (-1,-1), "CM", idx, "hex_cm")
            logger.debug(polygon_manager)

            channelIds = (38+idx*39, -1, -1) # globalId, artificial sicell, rocpin
            polygon_manager.create_and_register_polygon(channelIds, (-1,-1), "CM", idx, "hex_cm")
            logger.debug(polygon_manager)

    # Export geometry data
    geometry_rootfile, coordinate_json, mapping_json = get_exported_file_names(args.waferType)
    polygon_manager.export_root_file(geometry_rootfile) # geometry root file for DQM
    polygon_manager.export_coordinate_data(coordinate_json) # store coordinates for auxiliary lines
    polygon_manager.export_channel_id_mapping(mapping_json) # store chIds for information wafer map


if __name__ == "__main__":
    #----------------------------------------------------------------------
    # Initialize parser and looger & Create output directories
    #----------------------------------------------------------------------
    parser = setup_parser()
    args = parser.parse_args()
    logger = setup_logging(verbose=args.verbose, log_file=f"log_{args.waferType}.txt")

    os.makedirs("output/coordinates", exist_ok=True)
    os.makedirs("output/mapping", exist_ok=True)
    os.makedirs("output/mapping_csv", exist_ok=True)
    os.makedirs("output/geometry", exist_ok=True)
    os.makedirs("output/waferMaps", exist_ok=True)

    #----------------------------------------------------------------------
    # Generate wafermap geometry root files
    #----------------------------------------------------------------------
    main(args, logger)
    if args.listTypes: exit()

    #----------------------------------------------------------------------
    # Create a c++ header file for auxiliary lines
    #----------------------------------------------------------------------
    geometry_rootfile, coordinate_json, _ = get_exported_file_names(args.waferType)
    if args.drawLine:
        producer = AuxiliaryLineProducer(args.waferType, coordinate_json)
        producer.create_cpp_headers()

    #----------------------------------------------------------------------
    # Execute root macro for visualization
    #----------------------------------------------------------------------
    scope, tag, outputName, markerSize = get_macro_arguments(args.waferType)
    rotationTag = "" if args.rotation == '0' else f"_rotation{args.rotation}"
    command = f"root -l -b -q ./scripts/generate_wafer_maps.C'(\"{geometry_rootfile}\", \"{outputName}\", {scope}, {int(args.drawLine)}, \"{tag}\", {markerSize}, \"{rotationTag}\")'"
    logger.info(command)
    subprocess.call(command, shell=True)
