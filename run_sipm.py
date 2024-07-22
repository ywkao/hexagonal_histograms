#!/usr/bin/env python2
import argparse
import subprocess
import toolbox.polygon_manager_sipm as tp

parser = argparse.ArgumentParser()
parser.add_argument('-n', help="number of cells", type=int, default=9999)
parser.add_argument('-w', '--waferType', help="set wafer type (full, LD3, LD4, HD)", type=str, default="full")
parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
args = parser.parse_args()

"""
Reminder: range of indices (line numbers) is decided from the text file, ./data/WaferCellMapTrg.txt
"""
if args.waferType == "user": # cassette level
    waferType, beginIdx, endIdx = "user", 0, 0
elif args.waferType == "sipm": # cassette level
    #waferType, beginIdx, endIdx = "sipm", 190, 477
    waferType, beginIdx, endIdx = "sipm", 1, 188 # 188 # 96 
elif args.waferType == "HD":
    waferType, beginIdx, endIdx = "HD", 223, 667
elif args.waferType == "full": # LD full
    waferType, beginIdx, endIdx = "full", 1, 223
elif args.waferType == "LD3":
    waferType, beginIdx, endIdx = "LD3", 667, 778
elif args.waferType == "LD4":
    waferType, beginIdx, endIdx = "LD4", 778, 889

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

def retrieve_info_sipm(line):
    info = line.strip().split()
    result = []
    for i, ele in enumerate(info):
        if i==24: break # NOTE: consider the first 24 element for the moment
        if i==3 or i==4:
            result.append(str(ele))
        elif "." in ele:
            result.append(float(ele))
        else:
            result.append(int(ele))
    return tuple(result)

        # plane u v itype typecode x0 y0 irot nvertices vx_0 vy_0 vx_1 vy_1 vx_2 vy_2 vx_3 vy_3 vx_4 vy_4 vx_5 vy_5 vx_6 vy_6 icassette # trigRate trigLinks dataRate_ld dataLinks_ld dataRate_hd dataLinks_hd MB wagon isSiPM isEngine nROCs power mrot phi HDorLD hash hash_hdld engine_trig_fibres engine_data_fibres engine_ctrl_fibres dataPp0 trigPp0 dataPp0_type trigPp0_type dataPp1 trigPp1 dataPp1_type trigPp1_type dataPp2 DAQ

def get_macro_arguments():
    # Reminder: outputName is not used for the moment
    if args.waferType == "user":
        scope = 50 
        markerSize = 0.7
        tag = "user"
        outputName = "waferMaps/DQM_user_map.png"
    elif args.waferType == "sipm":
        scope = 2000 
        markerSize = 0.7
        tag = "sipm"
        outputName = "waferMaps/DQM_sipm_map.png"
    elif args.waferType == "LD3":
        scope = 14
        markerSize = 0.7
        tag = "LD3_partial_wafer"
        outputName = "waferMaps/DQM_LD3_partial_wafer_map.png"
    elif args.waferType == "LD4":
        scope = 14
        markerSize = 0.7
        tag = "LD4_partial_wafer"
        outputName = "waferMaps/DQM_LD4_partial_wafer_map.png"
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

def transform_base_shape(pm, polygon_base, deltaPhi, shift, resize_factor):
    """apply rotation and translation on a base polygon"""
    shift = [10.*element for element in shift]
    polygon = {'x':[], 'y':[]}
    for idx in range(len(polygon_base['x'])):
        x, y = polygon_base['x'][idx], polygon_base['y'][idx]
        x, y = pm.rotate_coordinate(x, y, deltaPhi) if deltaPhi>0. else (x, y)
        x, y = pm.translate_coordinate(x, y, resize_factor, tuple(shift))
        polygon['x'].append(x)
        polygon['y'].append(y)
    return polygon

def main():
    polygon_manager = tp.PolygonManager(waferType)
    polygon_manager.globalId = 0
    scope, _, _, _ = get_macro_arguments()

    #----------------------------------------------------------------------------------------------------
    # 2024 user deinfed polygons
    #----------------------------------------------------------------------------------------------------
    if args.waferType=="user":
        nvertices = 6
        resize_factor = 10 # arbitrary scale
        shifts = [[0.,2.], [-1.*tp.tg.s3, -1.], [tp.tg.s3, -1.]]
        for idx in range(3):
            hexagon = tp.tg.base[tp.tg.type_hexagon]
            polygon = transform_base_shape(polygon_manager, hexagon, 0., shifts[idx], resize_factor)
            polygon_manager.run_sipm(nvertices, polygon, scope, "module_%d"%idx)

    #----------------------------------------------------------------------------------------------------
    # 2024 sipm on tiles, cassette level
    #----------------------------------------------------------------------------------------------------
    elif args.waferType=="sipm":
        # Load geometry text file
        with open("./data/geometry_sipmontile.hgcal.txt", 'r') as fin: contents = fin.readlines()[beginIdx:endIdx]
        print("[DEBUG] len(contents) = %d" % len(contents))

        for i, line in enumerate(contents):
            plane, u, v, itype, typecode, x0, y0, irot, nvertices, vx_0, vy_0, vx_1, vy_1, vx_2, vy_2, vx_3, vy_3, vx_4, vy_4, vx_5, vy_5, vx_6, vy_6, icassette = retrieve_info_sipm(line)
            print(plane, u, v, itype, typecode, x0, y0, irot, nvertices, vx_0, vy_0, vx_1, vy_1, vx_2, vy_2, vx_3, vy_3, vx_4, vy_4, vx_5, vy_5, vx_6, vy_6, icassette)

            polygon = {'x':[], 'y':[]}
            for i in range(nvertices):
                polygon['x'].append(vx[i])
                polygon['y'].append(vy[i])
                if (i+1)==nvertices: # make the polygon "closed"
                    polygon['x'].append(vx[0])
                    polygon['y'].append(vy[0])
                    
            polygon_manager.run_sipm(nvertices, polygon, scope)

    #----------------------------------------------------------------------------------------------------
    # 2023 recipe for wafer maps: load from WaferCellMapTrg.txt
    #----------------------------------------------------------------------------------------------------
    else:
        # Load geometry text file
        with open("./data/WaferCellMapTrg.txt", 'r') as fin: contents = fin.readlines()[beginIdx:endIdx]
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

    return polygon_manager.output_geometry_root_file


if __name__ == "__main__":
    geometry_rootfile = main()

    # if args.drawLine:
    #     exe("./toolbox/coordinate_loader.py -w %s" % args.waferType)
    macro = "th2poly_sipm.C" if (args.waferType=="sipm" or args.waferType=="user") else "th2poly.C"
    scope, tag, outputName, markerSize = get_macro_arguments()
    exe("root -l -b -q %s'(\"%s\", \"%s\", %d, %d, \"%s\", %f)'" % (macro, geometry_rootfile, outputName, scope, args.drawLine, tag, markerSize)) # execute root macro for TH2Poly

