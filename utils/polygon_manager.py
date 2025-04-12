import utils.geometry as ug
from utils.special_channels import Coordinates_CM_channels, Coordinates_NC_channels
import numpy as np
import json
import math
import ROOT
ROOT.gROOT.SetBatch(True)

class PolygonManager:
    def __init__(self, wafer_type, extra_angle, offset_x, offset_y):
        # configuration parameters & shared library
        mm2cm = 0.10
        arbUnit_to_cm = (6.9767/2.)*mm2cm if "ML" in wafer_type else (4.65/2.)*mm2cm
        waferSize = 60 * arbUnit_to_cm
        nFine, nCoarse = 0, 10 #222
        typeFine, typeCoarse = 0, 1

        ROOT.gInterpreter.ProcessLine('#include "scripts/include/HGCalCell.h"')
        ROOT.gSystem.Load("./build/libHGCalCell.so")
        cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)

        # wafer information
        self.waferType = wafer_type
        self.irregular_polygonal_cells = ug.irregular_polygonal_cells
        self.cell_helper = cell_helper
        self.cell_fine_or_coarse = typeCoarse
        self.arbUnit_to_cm = arbUnit_to_cm
        self.cm2mm = 10.0

        self.extra_rotation_tb2024 = extra_angle
        self.global_theta = 5.*math.pi/6. # + self.extra_rotation_tb2024 # 150 + extra degree
        self.cos_global_theta = math.cos(self.global_theta)
        self.sin_global_theta = math.sin(self.global_theta)

        # global corrections on coordinates
        self.global_correction_x = offset_x
        self.global_correction_y = offset_y

        # containers
        self.counter = 0
        self.idxNC = 0 # counting for non-connected channels
        self.collections = {} # a collection of cells in TGraph format, key = global channel Id, value = TGraph
        self.dict_my_chId_mapping = {} # key = globalId, value = [sicell, rocpin]
        self.dict_my_coordinate_data = {} # key = sicell, value = dict_polygon_coordinates

        self._build_polygon_lookup_tables()

    def create_and_register_polygon(self, channelIds, coor_uv, cellType="", cellIdx=-1, cellName="hex"):
        """
        Create and register a polygon for a cell based on its coordinates and IDs.

        This is the main method controlling the flow of polygon creation. It:
        1. Sets cell properties based on input parameters
        2. Calculates the cell's center coordinates
        3. Determines the polygon type and number of corners
        4. Generates the polygon graph
        5. Stores the graph in the collections dictionary

        Parameters
        ----------
        channelIds : tuple
            Tuple containing (globalId, sicell, rocpin) identifiers
        coor_uv : tuple
            Tuple containing (u, v) coordinates of the cell
        cellType : str, optional
            Type of cell ("", "CM", or "NC"), default is ""
        cellIdx : int, optional
            Index of the cell for CM and NC channels, default is -1
        cellName : str, optional
            Name of the cell for graph naming, default is "hex"

        Side Effects
        ------------
        Adds a new polygon to self.collections using globalId as the key
        Updates instance attributes with cell properties
        """

        # cell (u, v) coordinates and cell IDs
        self.iu, self.iv = coor_uv
        self.globalId, self.sicell, self.rocpin = channelIds

        # cell info (ad hoc for CM and non-connected channels)
        self.cellType = cellType
        self.cellIdx = cellIdx
        self.cellName = cellName

        # generate a polygon graph using cell center coordinates, polygon type, and the number of corners
        self.center_x, self.center_y = self._get_cell_center_coordinates()
        self.type_polygon, self.nCorner = self._get_polygon_information()
        self.graph = self._generate_polygon_graph() # need polygon type, number of corners, coordinates of cell center
        self.collections[self.globalId] = self.graph

    def export_root_file(self, output_geometry_root):
        """ generate geometry root file for DQM in raw data handling chain"""
        fout = ROOT.TFile(output_geometry_root, "RECREATE")
        for key, graph in sorted(self.collections.items()):
            graph.Write()
        fout.Close()

    def export_coordinate_data(self, output_json):
        """ export values for auxiliary boundary lines on the wafer map """
        with open(output_json, 'w') as f:
            json.dump(self.dict_my_coordinate_data, f, indent=4)

    def export_channel_id_mapping(self, output_json):
        """ export chId mapping for information wafer map """
        with open(output_json, 'w') as f:
            json.dump(self.dict_my_chId_mapping, f, indent=4)

    def _build_polygon_lookup_tables(self):
        """Build lookup tables for quick polygon type and corner count determination"""
        self._polygon_info_cache = {}

        for wafer_type, type_dict in self.irregular_polygonal_cells.items():
            self._polygon_info_cache[wafer_type] = {}
            for polygon_type, cell_list in type_dict.items():
                corner_count = len(ug.base[polygon_type]['x']) - 1
                for sicell in cell_list:
                    self._polygon_info_cache[wafer_type][sicell] = (polygon_type, corner_count)

    def _rotate_coordinate(self, x, y, theta):
        """ evaluate (r, phi) and apply rotation """
        r = math.sqrt(pow(x,2)+pow(y,2))
        cos_phi, sin_phi = x/r, y/r
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
        yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)
        return xprime, yprime

    def _translate_coordinate(self, x, y, scale, shift):
        """ apply scale and translation """
        dx, dy = shift
        return x*scale+dx, y*scale+dy

    def _get_cell_center_coordinates(self):
        """ convert (u, v) to (x, y) coordinates with global coorections """

        # non-connected channels
        if self.cellType == "NC":
            x = Coordinates_NC_channels[self.waferType]['x'][self.cellIdx%8]
            y = Coordinates_NC_channels[self.waferType]['y'][self.cellIdx%8]
            if self.waferType == "ML-F":
                theta = 2*math.pi/3. * (self.cellIdx//8) - math.pi/3.
            elif self.waferType == "ML-L" or self.waferType == "ML-R":
                theta = Coordinates_NC_channels[self.waferType]['theta'][self.cellIdx]

            x, y = self._rotate_coordinate(x, y, theta + self.extra_rotation_tb2024)
            x, y = self._translate_coordinate(x, y, self.arbUnit_to_cm, (0., 0.))
            return x, y

        # CM channels
        elif self.cellType == "CM":
            if self.waferType == "MH-F":
                x = Coordinates_CM_channels[self.waferType]['x'][self.cellIdx%8]
                y = Coordinates_CM_channels[self.waferType]['y'][self.cellIdx%8]
                theta = 2*math.pi/3. * (self.cellIdx//8)
            elif self.waferType == "ML-F":
                x = Coordinates_CM_channels[self.waferType]['x'][self.cellIdx%4]
                y = Coordinates_CM_channels[self.waferType]['y'][self.cellIdx%4]
                theta = 2*math.pi/3. * (self.cellIdx//4) - math.pi/3.
            elif self.waferType == "ML-L" or self.waferType == "ML-R":
                x = Coordinates_CM_channels[self.waferType]['x'][self.cellIdx]
                y = Coordinates_CM_channels[self.waferType]['y'][self.cellIdx]
                theta = Coordinates_CM_channels[self.waferType]['theta'][self.cellIdx]

            x, y = self._rotate_coordinate(x, y, theta + self.extra_rotation_tb2024)
            x, y = self._translate_coordinate(x, y, self.arbUnit_to_cm, (0., 0.))
            return x, y

        # normal channels
        else:
            coor = self.cell_helper.cellUV2XY1(int(self.iu), int(self.iv), 0, self.cell_fine_or_coarse)
            x, y = self._rotate_coordinate(coor[0], coor[1], self.global_theta)
            x, y = self._translate_coordinate(x, y, 1., (-1*self.global_correction_x, -1*self.global_correction_y))
            x, y = self._rotate_coordinate(x, y, self.extra_rotation_tb2024)
            return x, y

    def _get_polygon_information(self):
        """Unified method to determine polygon type and corner count for any wafer type"""
        # Handle CM and NC channels
        if self.cellType == "CM":
            if self.cellIdx % 2 == 0:  # CM0
                return ug.type_regular_pentagon, 5
            else:  # CM1
                return ug.type_square, 4
        elif self.cellType == "NC":
            return ug.type_circle, 12

        # Handle calibration cells
        if isinstance(self.rocpin, str):  # "CALIB"
            return ug.type_circle, 12

        # Look up sicell in the cache
        polygon_info = self._polygon_info_cache.get(self.waferType, {}).get(self.sicell)
        if polygon_info:
            return polygon_info

        # Default for regular cells
        return ug.type_hexagon, 6

    def _get_polygon_base_and_rotation(self):
        """
        Use local rotation for corner cells on HD full wafers
        CAVEAT: mind the internal indices of corner polygons when querying auxiliary lines
        """
        # Define rotation mapping: maps derived polygon types to (base_type, rotation_angle) tuples
        rotation_mapping = {
            # Rotations by 2*pi/3 (120 degrees)
            ug.type_HD_hexagon_side3_corner3: (ug.type_HD_hexagon_side1_corner1, 2*ug.p3),
            ug.type_HD_hexagon_side3_corner4: (ug.type_HD_hexagon_side1_corner2, 2*ug.p3),
            ug.type_HD_trpezoid_corner3: (ug.type_HD_trpezoid_corner1, 2*ug.p3),
            ug.type_HD_trpezoid_corner4: (ug.type_HD_trpezoid_corner2, 2*ug.p3),
            ug.type_HD_hexagon_side2_corner3: (ug.type_HD_hexagon_side6_corner1, 2*ug.p3),
            ug.type_HD_hexagon_side4_corner4: (ug.type_HD_hexagon_side2_corner2, 2*ug.p3),

            # Rotations by 4*pi/3 (240 degrees)
            ug.type_HD_hexagon_side5_corner5: (ug.type_HD_hexagon_side1_corner1, 4*ug.p3),
            ug.type_HD_hexagon_side5_corner6: (ug.type_HD_hexagon_side1_corner2, 4*ug.p3),
            ug.type_HD_trpezoid_corner5: (ug.type_HD_trpezoid_corner1, 4*ug.p3),
            ug.type_HD_trpezoid_corner6: (ug.type_HD_trpezoid_corner2, 4*ug.p3),
            ug.type_HD_hexagon_side4_corner5: (ug.type_HD_hexagon_side6_corner1, 4*ug.p3),
            ug.type_HD_hexagon_side6_corner6: (ug.type_HD_hexagon_side2_corner2, 4*ug.p3)
        }

        # Look up base type and rotation angle
        if self.type_polygon in rotation_mapping:
            base_type, rotation = rotation_mapping[self.type_polygon]
            return ug.base[base_type], rotation + self.extra_rotation_tb2024

        # Default case - no rotation mapping found
        return ug.base[self.type_polygon], self.extra_rotation_tb2024

    def _generate_polygon_graph(self):
        """ derive coordinates for a polygon & create an instance of TGraph """
        polygon = {'x':[], 'y':[]}
        polygon_base, deltaPhi = self._get_polygon_base_and_rotation()

        resize_factor = 1.0
        if self.cellType == "CM": resize_factor = 0.6
        elif self.cellType == "NC": resize_factor = 0.4
        if(isinstance(self.rocpin, str)): resize_factor = 0.4 # "CALIB"

        # apply rotation and translation on a base polygon
        for idx in range(self.nCorner+1):
            x, y = polygon_base['x'][idx], polygon_base['y'][idx]
            x, y = self._rotate_coordinate(x, y, deltaPhi) if deltaPhi>0. else (x, y)
            x, y = self._translate_coordinate(x, y, self.arbUnit_to_cm*resize_factor, (self.center_x, self.center_y))
            polygon['x'].append(x)
            polygon['y'].append(y)

        # save info in dictionary for mapping
        self.dict_my_chId_mapping[self.globalId] = [self.sicell, self.rocpin]
        if not (self.cellType=="CM" or self.cellType=="NC"):
            if self.waferType == "ML-F":
                self.dict_my_coordinate_data[self.sicell] = polygon
            else:
                self.dict_my_coordinate_data[self.globalId] = polygon

        # create a graph
        graph = ROOT.TGraph(self.nCorner+1, np.array(polygon['x']), np.array(polygon['y']))
        graph.SetTitle("")
        graph.GetXaxis().SetTitle("x (arb. unit)")
        graph.GetYaxis().SetTitle("y (arb. unit)")

        graph.SetMaximum(200)
        graph.SetMinimum(-200)
        graph.GetXaxis().SetLimits(-200, 200)
        graph.SetName(self.cellName + "_%d" % self.globalId)

        # evaluation of area (valid for LD only)
        self.area = graph.Integral()
        if isinstance(self.rocpin, str):
            self.area = 0.29239 # area of LD calibration cell in cm^{2}
        elif self.type_polygon == ug.type_hollow:
            self.area = 1.2646 - 0.29239 # area of LD outer calib cell in cm^{2}
        elif self.cellType=="CM" or self.cellType=="NC":
            self.area = 0.

        self.counter += 1

        return graph

    def __str__(self):
        return "globalId = {0}, rocpin = {1}, sicell = {2}, u-v coordinates = {3}, area = {4} mm^{{2}}".format(self.globalId, self.rocpin, self.sicell, (self.iu,self.iv), "%.2f"%(self.area*pow(self.cm2mm,2)))
