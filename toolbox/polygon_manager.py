import toolbox.geometry as tg
import numpy as np
import json
import math
import ROOT
ROOT.gROOT.SetBatch(True)

class PolygonManager:
    def __init__(self, wafer_type):
        # configuration parameters & shared library
        arbUnit_to_cm = 17./24.
        waferSize = 60 * arbUnit_to_cm
        nFine, nCoarse = 0, 10 #222
        typeFine, typeCoarse = 0, 1
        
        ROOT.gInterpreter.ProcessLine('#include "include/HGCalCell.h"')
        ROOT.gSystem.Load("./build/libHGCalCell.so")
        cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)

        # wafer information
        self.type = wafer_type
        self.LD_cells = tg.LD_cells
        self.cell_helper = cell_helper
        self.cell_fine_or_coarse = typeCoarse
        self.arbUnit_to_cm = arbUnit_to_cm

        # global corrections on coordinates
        self.global_correction_x = 2*tg.s3
        self.global_correction_y = -5 
        self.global_theta = 5.*math.pi/6. # 150 degree
        self.cos_global_theta = math.cos(self.global_theta)
        self.sin_global_theta = math.sin(self.global_theta)

        # default cell info (unused for normal channels except for cellName)
        self.cellType = ""
        self.cellIdx = -1
        self.cellName = "hex"

        # containers
        self.counter = 0
        self.collections = {} # a collection of cells in TGraph format, key = global channel Id, value = TGraph
        self.dict_my_coordinate_data = {} # key = sicell, value = dict_polygon_coordinates

    def set_special_cell_info(self, cellType, cellIdx, cellName):
        "ad hoc for CM and non-connected channels"
        self.cellType = cellType
        self.cellIdx = cellIdx
        self.cellName = cellName

    def get_polygon(self, sicell, type_polygon, nCorner, x, y):
        """ return an instance of TGraph """
        polygon_base = tg.base[type_polygon]
        polygon = {}
    
        resize_factor = 1.0
        if self.cellType == "CM":
            resize_factor = 0.6
        elif self.cellType == "NC":
            resize_factor = 0.4
    
        polygon['x'] = [ element*self.arbUnit_to_cm*resize_factor + x for element in polygon_base['x'] ]
        polygon['y'] = [ element*self.arbUnit_to_cm*resize_factor + y for element in polygon_base['y'] ]
    
        self.dict_my_coordinate_data[sicell] = polygon
    
        graph = ROOT.TGraph(nCorner+1, np.array(polygon['x']), np.array(polygon['y']))
        graph.SetTitle("")
        graph.GetXaxis().SetTitle("x (arb. unit)")
        graph.GetYaxis().SetTitle("y (arb. unit)")
        
        graph.SetMaximum(200)
        graph.SetMinimum(-200)
        graph.GetXaxis().SetLimits(-200, 200)
        graph.SetName(self.cellName + "_%d" % sicell)

        self.counter += 1

        return graph
    
    def get_cell_center_coordinates(self, iu, iv):
        """ convert (u, v) to (x, y) coordinates with global coorections """

        if self.cellType == "NC":
            x = tg.Coordinates_NC_channels['x'][self.cellIdx%8]*self.arbUnit_to_cm
            y = tg.Coordinates_NC_channels['y'][self.cellIdx%8]*self.arbUnit_to_cm
            theta = 2*math.pi/3. * (self.cellIdx//8) - math.pi/3.
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)

            # evaluate (r, phi) and apply rotation
            r = math.sqrt(pow(x,2)+pow(y,2))
            cos_phi, sin_phi = x/r, y/r
            xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
            yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)
            x, y = xprime, yprime

            return xprime, yprime

        elif self.cellType == "CM":
            # assign coordinates
            correction_fine_tune_y_coordinate = 2. if self.cellIdx//4 == 0 else 0.
            x = tg.Coordinates_CM_channels['x'][self.cellIdx%4]*self.arbUnit_to_cm
            y = tg.Coordinates_CM_channels['y'][self.cellIdx%4]*self.arbUnit_to_cm - correction_fine_tune_y_coordinate*self.arbUnit_to_cm
            theta = 2*math.pi/3. * (self.cellIdx//4) - math.pi/3.
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
    
            # evaluate (r, phi) and apply rotation
            r = math.sqrt(pow(x,2)+pow(y,2))
            cos_phi, sin_phi = x/r, y/r
            xprime = r*(cos_phi*cos_theta + sin_phi*sin_theta)
            yprime = r*(sin_phi*cos_theta - cos_phi*sin_theta)

            return xprime, yprime

        else:
            coor = self.cell_helper.cellUV2XY1(int(iu), int(iv), 0, self.cell_fine_or_coarse)
            x, y = coor[0], coor[1]
    
            # evaluate (r, phi) and apply rotation
            r = math.sqrt(pow(x,2)+pow(y,2))
            cos_phi, sin_phi = x/r, y/r
            xprime = r*(cos_phi*self.cos_global_theta + sin_phi*self.sin_global_theta) + self.global_correction_x
            yprime = r*(sin_phi*self.cos_global_theta - cos_phi*self.sin_global_theta) + self.global_correction_y

            return xprime, yprime

    def get_polygon_information(self, sicell, rocpin):
        """ return type of polygon & nCorner of it """
        if self.type == "full":
            return self.get_polygon_info_LD_full(sicell, rocpin)
        elif self.type == "partial":
            return self.get_polygon_info_LD_partial(sicell, rocpin)
        else:
            try:
                raise NameError("WaferType")
            except NameError:
                print("The specified wafer type is unexpected.")
        
    def get_polygon_info_LD_partial(self, sicell, rocpin):
        """ conditional statements for LD partial wafer """
        type_polygon, nCorner = tg.type_hexagon, 6
        return type_polygon, nCorner

    def get_polygon_info_LD_full(self, sicell, rocpin):
        """ conditional statements for LD full wafer """
        type_polygon, nCorner = tg.type_hexagon, 6

        if self.cellType=="CM":
            if self.cellIdx%2==0: # CM0
                type_polygon, nCorner = tg.type_regular_pentagon, 5
            else: # CM1
                type_polygon, nCorner = tg.type_square, 4
            return type_polygon, nCorner
        
        elif self.cellType=="NC":
            return tg.type_circle, 12 

        else:
            if sicell in self.LD_cells[tg.type_hexagon_corner1]:
                type_polygon, nCorner = tg.type_hexagon_corner1, 6
            elif sicell in self.LD_cells[tg.type_hexagon_corner2]:
                type_polygon, nCorner = tg.type_hexagon_corner2, 6
            elif sicell in self.LD_cells[tg.type_hexagon_corner3]:
                type_polygon, nCorner = tg.type_hexagon_corner3, 6
            elif sicell in self.LD_cells[tg.type_hexagon_corner4]:
                type_polygon, nCorner = tg.type_hexagon_corner4, 6
            elif sicell in self.LD_cells[tg.type_hexagon_corner5]:
                type_polygon, nCorner = tg.type_hexagon_corner5, 6
            elif sicell in self.LD_cells[tg.type_hexagon_corner6]:
                type_polygon, nCorner = tg.type_hexagon_corner6, 6
    
            elif sicell in self.LD_cells[tg.type_pentagon_side1]:
                type_polygon, nCorner = tg.type_pentagon_side1, 5
            elif sicell in self.LD_cells[tg.type_pentagon_side2]:
                type_polygon, nCorner = tg.type_pentagon_side2, 5
            elif sicell in self.LD_cells[tg.type_pentagon_side3]:
                type_polygon, nCorner = tg.type_pentagon_side3, 5
            elif sicell in self.LD_cells[tg.type_pentagon_side4]:
                type_polygon, nCorner = tg.type_pentagon_side4, 5
            elif sicell in self.LD_cells[tg.type_pentagon_side5]:
                type_polygon, nCorner = tg.type_pentagon_side5, 5
            elif sicell in self.LD_cells[tg.type_pentagon_side6]:
                type_polygon, nCorner = tg.type_pentagon_side6, 5
    
            elif sicell in tg.hollow_cells:
                type_polygon, nCorner = tg.type_hollow, 14 
            elif(isinstance(rocpin, str)): # "CALIB"
                type_polygon, nCorner = tg.type_hexagon_small, 6 
            elif sicell in self.LD_cells[tg.type_pentagon_corner1]:
                type_polygon, nCorner = tg.type_pentagon_corner1, 5
            elif sicell in self.LD_cells[tg.type_pentagon_corner2]:
                type_polygon, nCorner = tg.type_pentagon_corner2, 5
            elif sicell in self.LD_cells[tg.type_pentagon_corner3]:
                type_polygon, nCorner = tg.type_pentagon_corner3, 5
            elif sicell in self.LD_cells[tg.type_pentagon_corner4]:
                type_polygon, nCorner = tg.type_pentagon_corner4, 5
            elif sicell in self.LD_cells[tg.type_pentagon_corner5]:
                type_polygon, nCorner = tg.type_pentagon_corner5, 5
            elif sicell in self.LD_cells[tg.type_pentagon_corner6]:
                type_polygon, nCorner = tg.type_pentagon_corner6, 5

            return type_polygon, nCorner

    def export_coordinate_data(self):
        """ export values for auxiliary boundary lines on the wafer map """
        with open("data/output_my_coordinate_data.json", 'w') as f:
            json.dump(self.dict_my_coordinate_data, f, indent=4)

    def export_root_file(self):
        """ generate geometry root file for DQM in raw data handling chain"""
        fout = ROOT.TFile("./data/hexagons.root", "RECREATE")
        for key, graph in self.collections.items():
            graph.Write()
        fout.Close()
