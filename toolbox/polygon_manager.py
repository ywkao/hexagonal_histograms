import toolbox.geometry as tg
import numpy as np
import json
import math
import ROOT
ROOT.gROOT.SetBatch(True)

class PolygonManager:
    def __init__(self, wafer_type, extra_angle, offset_x, offset_y):
        # configuration parameters & shared library
        mm2cm = 0.10
        arbUnit_to_cm = (6.9767/2.)*mm2cm if not wafer_type=="HD" else (4.65/2.)*mm2cm
        waferSize = 60 * arbUnit_to_cm
        nFine, nCoarse = 0, 10 #222
        typeFine, typeCoarse = 0, 1

        ROOT.gInterpreter.ProcessLine('#include "include/HGCalCell.h"')
        ROOT.gSystem.Load("./build/libHGCalCell.so")
        cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)

        # wafer information
        self.waferType = wafer_type
        self.special_cells = tg.special_cells
        self.cell_helper = cell_helper
        self.cell_fine_or_coarse = typeCoarse
        self.arbUnit_to_cm = arbUnit_to_cm
        self.cm2mm = 10.0

        # output geometry root file
        if self.waferType == "HD":
            self.output_geometry_root_file = "./data/geometry_HD_full_wafer.root"
        elif self.waferType == "LD3":
            self.output_geometry_root_file = "./data/geometry_LD3_partial_wafer.root"
        elif self.waferType == "LD4":
            self.output_geometry_root_file = "./data/geometry_LD4_partial_wafer.root"
        elif self.waferType == "full":
            self.output_geometry_root_file = "./data/geometry_LD_full_wafer.root"
        else:
            self.output_geometry_root_file = "./data/hexagons.root"

        self.extra_rotation_tb2024 = extra_angle
        self.global_theta = 5.*math.pi/6. # + self.extra_rotation_tb2024 # 150 + extra degree
        self.cos_global_theta = math.cos(self.global_theta)
        self.sin_global_theta = math.sin(self.global_theta)

        # global corrections on coordinates
        if self.waferType == "HD":
            self.global_correction_x = 0.805403625519528
            self.global_correction_y = -1.395
        else:
            self.global_correction_x = offset_x
            self.global_correction_y = offset_y

        # containers
        self.counter = 0
        self.idxNC = 0 # counting for non-connected channels
        self.collections = {} # a collection of cells in TGraph format, key = global channel Id, value = TGraph
        self.dict_my_chId_mapping = {} # key = globalId, value = [sicell, rocpin]
        self.dict_my_coordinate_data = {} # key = sicell, value = dict_polygon_coordinates

    def rotate_coordinate(self, x, y, theta):
        """ evaluate (r, phi) and apply rotation """
        r = math.sqrt(pow(x,2)+pow(y,2))
        cos_phi, sin_phi = x/r, y/r
        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)
        xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
        yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)
        return xprime, yprime

    def translate_coordinate(self, x, y, scale, shift):
        """ apply scale and translation """
        dx, dy = shift
        return x*scale+dx, y*scale+dy

    def get_polygon(self):
        """ derive coordinates for a polygon & create an instance of TGraph """
        polygon = {'x':[], 'y':[]}
        polygon_base, deltaPhi = self.get_base()

        resize_factor = 1.0
        if self.cellType == "CM": resize_factor = 0.6
        elif self.cellType == "NC": resize_factor = 0.4
        if(isinstance(self.rocpin, str)): resize_factor = 0.4 # "CALIB"

        # apply rotation and translation on a base polygon
        for idx in range(self.nCorner+1):
            x, y = polygon_base['x'][idx], polygon_base['y'][idx]
            x, y = self.rotate_coordinate(x, y, deltaPhi) if deltaPhi>0. else (x, y)
            x, y = self.translate_coordinate(x, y, self.arbUnit_to_cm*resize_factor, (self.center_x, self.center_y))
            polygon['x'].append(x)
            polygon['y'].append(y)

        # save info in dictionary for mapping
        self.dict_my_chId_mapping[self.globalId] = [self.sicell, self.rocpin]
        if not (self.cellType=="CM" or self.cellType=="NC"):
            if self.waferType == "full":
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
        elif self.type_polygon == tg.type_hollow:
            self.area = 1.2646 - 0.29239 # area of LD outer calib cell in cm^{2}
        elif self.cellType=="CM" or self.cellType=="NC":
            self.area = 0.

        self.counter += 1

        return graph

    def get_cell_center_coordinates(self):
        """ convert (u, v) to (x, y) coordinates with global coorections """

        # unconnected channels
        if self.cellType == "NC":
            x = tg.Coordinates_NC_channels[self.waferType]['x'][self.cellIdx%8]
            y = tg.Coordinates_NC_channels[self.waferType]['y'][self.cellIdx%8]
            if self.waferType == "full":
                theta = 2*math.pi/3. * (self.cellIdx//8) - math.pi/3.
            elif self.waferType == "LD3" or self.waferType == "LD4":
                theta = tg.Coordinates_NC_channels[self.waferType]['theta'][self.cellIdx]

            x, y = self.rotate_coordinate(x, y, theta + self.extra_rotation_tb2024)
            x, y = self.translate_coordinate(x, y, self.arbUnit_to_cm, (0., 0.))
            return x, y

        # CM channels
        elif self.cellType == "CM":
            if self.waferType == "HD":
                x = tg.Coordinates_CM_channels[self.waferType]['x'][self.cellIdx%8]
                y = tg.Coordinates_CM_channels[self.waferType]['y'][self.cellIdx%8]
                theta = 2*math.pi/3. * (self.cellIdx//8)
            elif self.waferType == "full":
                x = tg.Coordinates_CM_channels[self.waferType]['x'][self.cellIdx%4]
                y = tg.Coordinates_CM_channels[self.waferType]['y'][self.cellIdx%4]
                theta = 2*math.pi/3. * (self.cellIdx//4) - math.pi/3.
            elif self.waferType == "LD3" or self.waferType == "LD4":
                x = tg.Coordinates_CM_channels[self.waferType]['x'][self.cellIdx]
                y = tg.Coordinates_CM_channels[self.waferType]['y'][self.cellIdx]
                theta = tg.Coordinates_CM_channels[self.waferType]['theta'][self.cellIdx]

            x, y = self.rotate_coordinate(x, y, theta + self.extra_rotation_tb2024)
            x, y = self.translate_coordinate(x, y, self.arbUnit_to_cm, (0., 0.))
            return x, y

        # normal channels
        else:
            coor = self.cell_helper.cellUV2XY1(int(self.iu), int(self.iv), 0, self.cell_fine_or_coarse)
            x, y = self.rotate_coordinate(coor[0], coor[1], self.global_theta)
            x, y = self.translate_coordinate(x, y, 1., (-1*self.global_correction_x, -1*self.global_correction_y))
            x, y = self.rotate_coordinate(x, y, self.extra_rotation_tb2024)
            return x, y

    def get_polygon_information(self):
        """ return type of polygon & number of corners of it """
        # CM and NC
        if self.cellType=="CM":
            if self.cellIdx%2==0: # CM0
                return tg.type_regular_pentagon, 5
            else: # CM1
                return tg.type_square, 4
        elif self.cellType=="NC":
            return tg.type_circle, 12

        # other channels
        if self.waferType == "full":
            return self.get_polygon_info_LD_full()
        elif self.waferType == "LD3":
            return self.get_polygon_info_LD3_partial()
        elif self.waferType == "LD4":
            return self.get_polygon_info_LD4_partial()
        elif self.waferType == "HD":
            return self.get_polygon_info_HD_full()
        else:
            try:
                raise NameError("WaferType")
            except NameError:
                print("The specified wafer type is unexpected.")

    def get_polygon_info_HD_full(self):
        """ conditional statements for HD full wafer """
        cellDict = self.special_cells[self.waferType]
        if(isinstance(self.rocpin, str)): # "CALIB"
            return tg.type_circle, 12
        elif self.sicell in cellDict[tg.type_hollow]:
            return tg.type_hollow, 20
        elif self.sicell in cellDict[tg.type_pentagon_side1]:
            return tg.type_pentagon_side1, 5
        elif self.sicell in cellDict[tg.type_pentagon_side2]:
            return tg.type_pentagon_side2, 5
        elif self.sicell in cellDict[tg.type_pentagon_side3]:
            return tg.type_pentagon_side3, 5
        elif self.sicell in cellDict[tg.type_pentagon_side4]:
            return tg.type_pentagon_side4, 5
        elif self.sicell in cellDict[tg.type_pentagon_side5]:
            return tg.type_pentagon_side5, 5
        elif self.sicell in cellDict[tg.type_pentagon_side6]:
            return tg.type_pentagon_side6, 5
        elif self.sicell in cellDict[tg.type_HD_hexagon_side1_corner1]:
            return tg.type_HD_hexagon_side1_corner1, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side1_corner2]:
            return tg.type_HD_hexagon_side1_corner2, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side3_corner3]:
            return tg.type_HD_hexagon_side3_corner3, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side3_corner4]:
            return tg.type_HD_hexagon_side3_corner4, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side5_corner5]:
            return tg.type_HD_hexagon_side5_corner5, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side5_corner6]:
            return tg.type_HD_hexagon_side5_corner6, 6
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner1]:
            return tg.type_HD_trpezoid_corner1, 4
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner2]:
            return tg.type_HD_trpezoid_corner2, 4
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner3]:
            return tg.type_HD_trpezoid_corner3, 4
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner4]:
            return tg.type_HD_trpezoid_corner4, 4
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner5]:
            return tg.type_HD_trpezoid_corner5, 4
        elif self.sicell in cellDict[tg.type_HD_trpezoid_corner6]:
            return tg.type_HD_trpezoid_corner6, 4
        elif self.sicell in cellDict[tg.type_HD_hexagon_side6_corner1]:
            return tg.type_HD_hexagon_side6_corner1, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side2_corner2]:
            return tg.type_HD_hexagon_side2_corner2, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side2_corner3]:
            return tg.type_HD_hexagon_side2_corner3, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side4_corner4]:
            return tg.type_HD_hexagon_side4_corner4, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side4_corner5]:
            return tg.type_HD_hexagon_side4_corner5, 6
        elif self.sicell in cellDict[tg.type_HD_hexagon_side6_corner6]:
            return tg.type_HD_hexagon_side6_corner6, 6
        else:
            return tg.type_hexagon, 6

    def get_polygon_info_LD_full(self):
        """ conditional statements for LD full wafer """
        cellDict = self.special_cells[self.waferType]
        if self.sicell in cellDict[tg.type_hexagon_corner1]:
            return tg.type_hexagon_corner1, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner2]:
            return tg.type_hexagon_corner2, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner3]:
            return tg.type_hexagon_corner3, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner4]:
            return tg.type_hexagon_corner4, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner5]:
            return tg.type_hexagon_corner5, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner6]:
            return tg.type_hexagon_corner6, 6
        elif self.sicell in cellDict[tg.type_pentagon_side1]:
            return tg.type_pentagon_side1, 5
        elif self.sicell in cellDict[tg.type_pentagon_side2]:
            return tg.type_pentagon_side2, 5
        elif self.sicell in cellDict[tg.type_pentagon_side3]:
            return tg.type_pentagon_side3, 5
        elif self.sicell in cellDict[tg.type_pentagon_side4]:
            return tg.type_pentagon_side4, 5
        elif self.sicell in cellDict[tg.type_pentagon_side5]:
            return tg.type_pentagon_side5, 5
        elif self.sicell in cellDict[tg.type_pentagon_side6]:
            return tg.type_pentagon_side6, 5
        elif self.sicell in cellDict[tg.type_hollow]:
            return tg.type_hollow, 20
        elif(isinstance(self.rocpin, str)): # "CALIB"
            return tg.type_circle, 12
        elif self.sicell in cellDict[tg.type_pentagon_corner1]:
            return tg.type_pentagon_corner1, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner2]:
            return tg.type_pentagon_corner2, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner3]:
            return tg.type_pentagon_corner3, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner4]:
            return tg.type_pentagon_corner4, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner5]:
            return tg.type_pentagon_corner5, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner6]:
            return tg.type_pentagon_corner6, 5
        else:
            return tg.type_hexagon, 6

    def get_polygon_info_LD4_partial(self):
        """ conditional statements for LD4 partial wafer """
        cellDict = self.special_cells[self.waferType]
        if self.sicell in cellDict[tg.type_hollow]:
            return tg.type_hollow, 20
        elif(isinstance(self.rocpin, str)): # "CALIB"
            return tg.type_circle, 12
        elif self.sicell in cellDict[tg.type_pentagon_side1]:
            return tg.type_pentagon_side1, 5
        elif self.sicell in cellDict[tg.type_pentagon_side2]:
            return tg.type_pentagon_side2, 5
        elif self.sicell in cellDict[tg.type_pentagon_side3]:
            return tg.type_pentagon_side3, 5
        elif self.sicell in cellDict[tg.type_pentagon_side4]:
            return tg.type_pentagon_side4, 5
        elif self.sicell in cellDict[tg.type_trapezoid_right]:
            return tg.type_trapezoid_right, 4
        elif self.sicell in cellDict[tg.type_trapezoid_extended_right]:
            return tg.type_trapezoid_extended_right, 4
        elif self.sicell in cellDict[tg.type_trapezoid_left]:
            return tg.type_trapezoid_left, 4
        elif self.sicell in cellDict[tg.type_partial_wafer_pentagon_corner3]:
            return tg.type_partial_wafer_pentagon_corner3, 5
        elif self.sicell in cellDict[tg.type_partial_wafer_hexagon_corner3]:
            return tg.type_partial_wafer_hexagon_corner3, 6
        elif self.sicell in cellDict[tg.type_partial_wafer_hexagon_corner2]:
            return tg.type_partial_wafer_hexagon_corner2, 6
        elif self.sicell in cellDict[tg.type_partial_wafer_pentagon_merged_cell_corner2]:
            return tg.type_partial_wafer_pentagon_merged_cell_corner2, 5
        elif self.sicell in cellDict[tg.type_partial_wafer_pentagon_merged_cell_corner4]:
            return tg.type_partial_wafer_pentagon_merged_cell_corner4, 5
        elif self.sicell in cellDict[tg.type_hexagon_corner4]:
            return tg.type_hexagon_corner4, 6
        elif self.sicell in cellDict[tg.type_parallelogram]:
            return tg.type_parallelogram, 4
        else:
            return tg.type_hexagon, 6

    def get_polygon_info_LD3_partial(self):
        """ conditional statements for LD3 partial wafer """
        cellDict = self.special_cells[self.waferType]
        if(isinstance(self.rocpin, str)): # "CALIB"
            return tg.type_circle, 12
        elif self.sicell in cellDict[tg.type_hollow]:
            return tg.type_hollow, 20
        elif self.sicell in cellDict[tg.type_pentagon_hollow]:
            return tg.type_pentagon_hollow, 19
        elif self.sicell in cellDict[tg.type_trapezoid_left]:
            return tg.type_trapezoid_left, 4
        elif self.sicell in cellDict[tg.type_trapezoid_extended_left]:
            return tg.type_trapezoid_extended_left, 4
        elif self.sicell in cellDict[tg.type_pentagon_side1]:
            return tg.type_pentagon_side1, 5
        elif self.sicell in cellDict[tg.type_pentagon_side4]:
            return tg.type_pentagon_side4, 5
        elif self.sicell in cellDict[tg.type_pentagon_side5]:
            return tg.type_pentagon_side5, 5
        elif self.sicell in cellDict[tg.type_pentagon_side6]:
            return tg.type_pentagon_side6, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner1]:
            return tg.type_pentagon_corner1, 5
        elif self.sicell in cellDict[tg.type_pentagon_corner5]:
            return tg.type_pentagon_corner5, 5
        elif self.sicell in cellDict[tg.type_partial_wafer_pentagon_corner6]:
            return tg.type_partial_wafer_pentagon_corner6, 5
        elif self.sicell in cellDict[tg.type_hexagon_corner1]:
            return tg.type_hexagon_corner1, 6
        elif self.sicell in cellDict[tg.type_hexagon_corner5]:
            return tg.type_hexagon_corner5, 6
        elif self.sicell in cellDict[tg.type_partial_wafer_hexagon_corner6]:
            return tg.type_partial_wafer_hexagon_corner6, 6
        else:
            return tg.type_hexagon, 6

    def get_base(self):
        """
        Use local rotation for corner cells on HD full wafers
        CAVEAT: mind the internal indices of corner polygons when querying auxiliary lines
        """
        if self.type_polygon==tg.type_HD_hexagon_side3_corner3:
            return tg.base[tg.type_HD_hexagon_side1_corner1], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side3_corner4:
            return tg.base[tg.type_HD_hexagon_side1_corner2], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side5_corner5:
            return tg.base[tg.type_HD_hexagon_side1_corner1], 4*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side5_corner6:
            return tg.base[tg.type_HD_hexagon_side1_corner2], 4*tg.p3 + self.extra_rotation_tb2024

        elif self.type_polygon==tg.type_HD_trpezoid_corner3:
            return tg.base[tg.type_HD_trpezoid_corner1], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_trpezoid_corner4:
            return tg.base[tg.type_HD_trpezoid_corner2], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_trpezoid_corner5:
            return tg.base[tg.type_HD_trpezoid_corner1], 4*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_trpezoid_corner6:
            return tg.base[tg.type_HD_trpezoid_corner2], 4*tg.p3 + self.extra_rotation_tb2024

        elif self.type_polygon==tg.type_HD_hexagon_side2_corner3:
            return tg.base[tg.type_HD_hexagon_side6_corner1], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side4_corner4:
            return tg.base[tg.type_HD_hexagon_side2_corner2], 2*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side4_corner5:
            return tg.base[tg.type_HD_hexagon_side6_corner1], 4*tg.p3 + self.extra_rotation_tb2024
        elif self.type_polygon==tg.type_HD_hexagon_side6_corner6:
            return tg.base[tg.type_HD_hexagon_side2_corner2], 4*tg.p3 + self.extra_rotation_tb2024

        else:
            return tg.base[self.type_polygon], self.extra_rotation_tb2024 

    def export_cpp_id_mapping(self):
        """ export chId mapping for information wafer map """
        if self.waferType == "full":
            output_json = "data/output_my_chId_mapping.json"
        elif self.waferType == "LD3":
            output_json = "data/output_my_chId_mapping_LD3_wafer.json"
        elif self.waferType == "LD4":
            output_json = "data/output_my_chId_mapping_LD4_wafer.json"
        elif self.waferType == "HD":
            output_json = "data/output_my_chId_mapping_HD_wafer.json"
        with open(output_json, 'w') as f:
            json.dump(self.dict_my_chId_mapping, f, indent=4)

    def export_coordinate_data(self):
        """ export values for auxiliary boundary lines on the wafer map """
        if self.waferType == "full":
            output_json = "data/output_my_coordinate_data.json"
        elif self.waferType == "LD3":
            output_json = "data/output_my_coordinate_LD3_wafer.json"
        elif self.waferType == "LD4":
            output_json = "data/output_my_coordinate_LD4_wafer.json"
        elif self.waferType == "HD":
            output_json = "data/output_my_coordinate_HD_wafer.json"
        with open(output_json, 'w') as f:
            json.dump(self.dict_my_coordinate_data, f, indent=4)

    def export_root_file(self):
        """ generate geometry root file for DQM in raw data handling chain"""
        fout = ROOT.TFile(self.output_geometry_root_file, "RECREATE")
        for key, graph in self.collections.items():
            graph.Write()
        fout.Close()

    def __str__(self):
        # more info
        return "globalId = {0}, rocpin = {1}, sicell = {2}, {3}, area = {4} mm^{{2}}".format(self.globalId, self.rocpin, self.sicell, (self.iu,self.iv), "%.2f"%(self.area*pow(self.cm2mm,2)))

        # channel ID info
        return "{0} {1} {2} {3}".format(self.globalId, self.rocpin, self.sicell, (self.iu,self.iv))

        # globalId and area
        return "{0} {1}".format(self.globalId, "%.2f"%(self.area*pow(self.cm2mm,2)))

    def run(self, channelIds, coor_uv, cellType="", cellIdx=-1, cellName="hex"):
        """ main method for controling flow """

        # cell Id and (u, v) coordinates
        self.iu, self.iv = coor_uv
        self.globalId, self.sicell, self.rocpin = channelIds

        # cell info (ad hoc for CM and non-connected channels)
        self.cellType = cellType
        self.cellIdx = cellIdx
        self.cellName = cellName

        # evaluation + creation
        self.center_x, self.center_y = self.get_cell_center_coordinates()
        self.type_polygon, self.nCorner = self.get_polygon_information()
        self.graph = self.get_polygon() # need polygon type, number of corners, coordinates of cell center
        self.collections[self.globalId] = self.graph

        # if self.sicell==193:
        #     print(f"[DEBUG] globalId = {self.globalId}, rocpin = {self.rocpin}, sicell = {self.sicell}")
        #     print(f"[DEBUG] x, y = {self.center_x}, {self.center_y}")


