import math

#--------------------------------------------------
# Define constants and types
#--------------------------------------------------
s2 = math.sqrt(2)
s3 = math.sqrt(3)
pi = math.pi
p3 = math.pi/3.

type_triangle = 3
type_square = 4
type_regular_pentagon = 5
type_hexagon = 6
type_hexagon_small = 7
type_circle = 12
type_pentagon_hollow = 19
type_hollow = 20

type_trapezoid_left = 41
type_trapezoid_extended_left = 42
type_trapezoid_right = 43
type_trapezoid_extended_right = 44
type_parallelogram = 45

type_pentagon_side1 = 501
type_pentagon_side2 = 502
type_pentagon_side3 = 503
type_pentagon_side4 = 504
type_pentagon_side5 = 505
type_pentagon_side6 = 506
type_pentagon_corner1 = 507
type_pentagon_corner2 = 508
type_pentagon_corner3 = 509
type_pentagon_corner4 = 510
type_pentagon_corner5 = 511
type_pentagon_corner6 = 512
type_partial_wafer_pentagon_corner6 = 513
type_partial_wafer_pentagon_corner3 = 514
type_partial_wafer_pentagon_merged_cell_corner2 = 515
type_partial_wafer_pentagon_merged_cell_corner4 = 516
type_hexagon_corner1 = 601
type_hexagon_corner2 = 602
type_hexagon_corner3 = 603
type_hexagon_corner4 = 604
type_hexagon_corner5 = 605
type_hexagon_corner6 = 606
type_partial_wafer_hexagon_corner6 = 607
type_partial_wafer_hexagon_corner3 = 608
type_partial_wafer_hexagon_corner2 = 609

type_pentagon_extended_side1 = 517
type_pentagon_truncated_side4 = 518
type_pentagon_extended_corner1 = 519
type_pentagon_extended_corner2 = 520

type_HD_quadrilaterals_corner3 = 407
type_HD_quadrilaterals_corner6 = 408
type_HD_quadrilaterals_left_side1 = 409
type_HD_quadrilaterals_right_side1 = 410
type_HD_quadrilaterals_extended_left_side1 = 411
type_HD_quadrilaterals_extended_right_side1 = 412

type_HD_hexagon_side1_corner1 = 621
type_HD_hexagon_side1_corner2 = 622
type_HD_hexagon_side3_corner3 = 623 # by rotation
type_HD_hexagon_side3_corner4 = 624 # by rotation
type_HD_hexagon_side5_corner5 = 625 # by rotation
type_HD_hexagon_side5_corner6 = 626 # by rotation
type_HD_trpezoid_corner1 = 401
type_HD_trpezoid_corner2 = 402
type_HD_trpezoid_corner3 = 403 # by rotation
type_HD_trpezoid_corner4 = 404 # by rotation
type_HD_trpezoid_corner5 = 405 # by rotation
type_HD_trpezoid_corner6 = 406 # by rotation
type_HD_hexagon_side6_corner1 = 650
type_HD_hexagon_side2_corner2 = 651
type_HD_hexagon_side2_corner3 = 652 # by rotation
type_HD_hexagon_side4_corner4 = 653 # by rotation
type_HD_hexagon_side4_corner5 = 654 # by rotation
type_HD_hexagon_side6_corner6 = 655 # by rotation

#----------------------------------------------------------------------------------------------------
# Define base polygons
#----------------------------------------------------------------------------------------------------
base = {
    type_hexagon : {
        'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0],
        'y': [2, 1, -1, -2, -1, 1, 2]
    },
    type_parallelogram : {
        'x': [0, 0, -1*s3, -1*s3, 0],
        'y': [2, -13./29., -40./29., 1, 2]
    },
    type_trapezoid_left : {
        'x': [0, 0, -1*s3, -1*s3, 0],
        'y': [2, -2, -1, 1, 2]
    },
    type_trapezoid_extended_left : {
        'x': [0, 0, -1*s3, -1*s3, 0],
        'y': [2, -2, -2, 1, 2]
    },
    type_trapezoid_right : {
        'x': [0, 1*s3, 1*s3, 0, 0],
        'y': [2, 1, -1, -2, 2]
    },
    type_trapezoid_extended_right : {
        'x': [0, 1*s3, 1*s3, 0, 0],
        'y': [2, 1, -2, -2, 2]
    },
    type_HD_hexagon_side1_corner1 : {
        'x': [1*s3, 1*s3, 0, -1*s3, -1*s3, -0.5*s3, 1*s3],
        'y': [1, -1, -2, -1, 0.5, 1, 1]
    },
    type_HD_hexagon_side1_corner2 : {
        'x': [-1*s3, 0.5*s3, s3, s3, 0, -1*s3, -1*s3],
        'y': [1, 1, 0.5, -1, -2, -1, 1]
    },
    type_HD_trpezoid_corner1 : {
        'x': [1*s3, 1*s3, 0, -0.75*s3, s3],
        'y': [0.5, -1, -2, -1.25, 0.5]
    },
    type_HD_trpezoid_corner2 : {
        'x': [-1*s3, 0.75*s3, 0, -1*s3, -1*s3],
        'y': [0.5, -1.25, -2, -1, 0.5]
    },
    type_HD_hexagon_side6_corner1 : {
        'x': [0.25*s3, 1*s3, 1*s3, 0, -1.5*s3, -1.25*s3, 0.25*s3],
        'y': [1.75, 1, -1, -2, -0.5, 0.25, 1.75]
    },
    type_HD_hexagon_side2_corner2 : {
        'x': [-0.25*s3, 1.25*s3, 1.5*s3, 0, -1*s3, -1*s3, -0.25*s3],
        'y': [1.75, 0.25, -0.5, -2, -1, 1, 1.75]
    },
    type_pentagon_side1 : {
        'x': [1*s3, 1*s3, 0, -1*s3, -1*s3, 1*s3],
        'y': [1, -1, -2, -1, 1, 1]
    },
    type_pentagon_side2 : {
        'x': [0.5*s3, 1.5*s3, 0, -1*s3, -1*s3, 0.5*s3],
        'y': [2.5, -0.5, -2, -1, 1, 2.5]
    },
    type_pentagon_side3 : {
        'x': [0, 1*s3, 0, -1*s3, -1*s3, 0],
        'y': [2, 1, -2, -1, 1, 2]
    },
    type_pentagon_side4 : {
        'x': [0, 1*s3, 1*s3, -1*s3, -1*s3, 0],
        'y': [2, 1, -2, -2, 1, 2]
    },
    type_pentagon_side5 : {
        'x': [0, 1*s3, 1*s3, 0, -1*s3, 0],
        'y': [2, 1, -1, -2, 1, 2]
    },
    type_pentagon_side6 : {
        'x': [-0.5*s3, 1*s3, 1*s3, 0, -1.5*s3, -0.5*s3],
        'y': [2.5, 1, -1, -2, -0.5, 2.5]
    },
    type_pentagon_extended_side1 : {
        'x': [1*s3, 1*s3, 0, -1*s3, -1*s3, 1*s3],
        'y': [2, -1, -2, -1, 2, 2]
    },
    type_pentagon_truncated_side4 : {
        'x': [0, 1*s3, 1*s3, -1*s3, -1*s3, 0],
        'y': [2, 1, -1, -1, 1, 2]
    },
    type_HD_quadrilaterals_extended_left_side1 : {
        'x': [0, 0, -1*s3, -1*s3, 0],
        'y': [2, -2, -1, 2, 2]
    },
    type_HD_quadrilaterals_extended_right_side1 : {
        'x': [1*s3, 1*s3, 0, 0, 1*s3],
        'y': [2, -1, -2, 2, 2]
    },
    type_HD_quadrilaterals_left_side1 : {
        'x': [0, 0, -1*s3, -1*s3, 0],
        'y': [1, -2, -1, 1, 1]
    },
    type_HD_quadrilaterals_right_side1 : {
        'x': [1*s3, 1*s3, 0, 0, 1*s3],
        'y': [1, -1, -2, 1, 1]
    },
    type_pentagon_extended_corner1 : {
        'x': [1*s3, 1*s3, 0, -1.5*s3, -2./s3, 1*s3],
        'y': [2, -1, -2, -0.5, 2, 2]
    },
    type_pentagon_extended_corner2 : {
        'x': [2./s3, 1.5*s3, 0, -1*s3, -1*s3, 2./s3],
        'y': [2, -0.5, -2, -1, 2, 2]
    },
    type_HD_quadrilaterals_corner3 : {
        'x': [0.5*s3, 5./s3, -1*s3, -1*s3, 0.5*s3],
        'y': [2.5, -1, -1, 1, 2.5]
    },
    type_HD_quadrilaterals_corner6 : {
        'x': [-0.5*s3, 1*s3, 1*s3, -5./s3, -0.5*s3],
        'y': [2.5, 1, -1, -1, 2.5]
    },
    type_hexagon_corner1 : {
        'x': [-11.*s3/58., 1*s3, 1*s3, 0, -1.5*s3, -5.*s3/6., -11.*s3/58.],
        'y': [127./58., 1, -1, -2, -0.5, 1.5, 127./58.]
    },
    type_hexagon_corner2 : {
        'x': [11.*s3/58., 5.*s3/6., 1.5*s3, 0, -1*s3, -1*s3, 11.*s3/58.],
        'y': [127./58., 1.5, -0.5, -2, -1, 1, 127./58.]
    },
    type_hexagon_corner3 : {
        'x': [0.5*s3, 7.*s3/6., 69.*s3/58., 0, -1*s3, -1*s3, 0.5*s3],
        'y': [2.5, 0.5, -47./58., -2, -1, 1, 2.5]
    },
    type_hexagon_corner4 : {
        'x': [0, 1*s3, 1*s3, s3/3., -1*s3, -1*s3, 0],
        'y': [2, 1, -40./29., -2, -2, 1, 2]
    },
    type_hexagon_corner5 : {
        'x': [0, 1*s3, 1*s3, -s3/3., -1*s3, -1*s3, 0],
        'y': [2, 1, -2, -2, -40./29., 1, 2]
    },
    type_hexagon_corner6 : {
        'x': [-0.5*s3, 1*s3, 1*s3, 0, -69.*s3/58., -7.*s3/6., -0.5*s3],
        'y': [2.5, 1, -1, -2, -47./58., 0.5, 2.5]
    },
    type_partial_wafer_hexagon_corner6 : {
        'x': [-0.5*s3, 1*s3, 1*s3, -23.*493.*s3/(58.*163.), -69.*s3/58., -7.*s3/6., -0.5*s3],
        'y': [2.5, 1, -2, -2, -47./58., 0.5, 2.5]
    },
    type_partial_wafer_hexagon_corner3 : {
        'x': [ 0.5*s3, 7.*s3/6., 69.*s3/58., 23.*493.*s3/(58.*163.), -1*s3, -1*s3, 0.5*s3 ],
        'y': [ 2.5, 0.5, -47./58., -2, -2, 1, 2.5 ]
    },
    type_partial_wafer_hexagon_corner2 : {
        'x': [-s3/2., s3, s3, 0, -1*s3, -1*s3, -s3/2.],
        'y': [1., -17./28., -1, -2, -1, 1, 1.]
    },
    type_pentagon_corner1 : {
        'x': [s3/2., 1*s3, 1*s3, 0, -69.*s3/58., s3/2.],
        'y': [1, 1, -1, -2, -47./58., 1]
    },
    type_pentagon_corner2 : {
        'x': [-s3/2., 69.*s3/58., 0, -1*s3, -1*s3, -s3/2.],
        'y': [1., -47./58., -2, -1, 1, 1.]
    },
    type_pentagon_corner3 : {
        'x': [11.*s3/58., s3/4., 0, -1*s3, -1*s3, 11.*s3/58.],
        'y': [127./58., -1.25, -2, -1, 1, 127./58.]
    },
    type_pentagon_corner4 : {
        'x': [0, 1*s3, 3.*s3/4., -s3, -1*s3, 0],
        'y': [2, 1, 0.25, -40./29., 1, 2]
    },
    type_pentagon_corner5 : {
        'x': [0, 1*s3, 1*s3, -3*s3/4, -1*s3, 0],
        'y': [2, 1, -40./29., 0.25, 1, 2]
    },
    type_pentagon_corner6 : {
        'x': [-11.*s3/58., 1*s3, 1*s3, 0, -s3/4., -11.*s3/58.],
        'y': [127./58., 1, -1, -2, -1.25, 127./58.]
    },
    type_partial_wafer_pentagon_corner6: {
        'x': [-1885*s3/(58.*163.), 1*s3, 1*s3, 0, -s3/4., -1885*s3/(58.*163.)],
        'y': [1, 1, -1, -2, -1.25, 1]
    },
    type_partial_wafer_pentagon_corner3: {
        'x': [ -1*s3, 1885*s3/(58.*163.), s3/4., 0, -1*s3, -1*s3 ],
        'y': [ 1, 1, -1.25, -2, -1, 1 ]
    },
    type_partial_wafer_pentagon_merged_cell_corner2 : {
        'x': [-s3, -s3/6., 1.5*s3, 0, -1*s3, -s3],
        'y': [151./28., 4.5, -0.5, -2, -1, 151./28.]
    },
    type_partial_wafer_pentagon_merged_cell_corner4 : {
        'x': [0, 1*s3, -0.25*s3, -1*s3, -1*s3, 0],
        'y': [2, 1, -11./4., -100./29., 1, 2]
    },
    type_triangle : {
        'x': [0, 1*s3, -1*s3, 0],
        'y': [2, -1, -1, 2]
    },
    type_square : {
        'x' : [s2, s2, -s2, -s2, s2],
        'y' : [s2, -s2, -s2, s2, s2]
    },
    type_regular_pentagon : {
        'x' : [0, 2*math.cos(pi/10.), 2*math.cos(17.*pi/10.), 2*math.cos(13.*pi/10.), 2*math.cos(9.*pi/10.), 0],
        'y' : [2, 2*math.sin(pi/10.), 2*math.sin(17.*pi/10.), 2*math.sin(13.*pi/10.), 2*math.sin(9.*pi/10.), 2],
    },
    type_hexagon_small : {
        'x': [0, 0.45*s3, 0.45*s3, 0, -0.45*s3, -0.45*s3, 0],
        'y': [0.9, 0.45, -0.45, -0.9, -0.45, 0.45, 0.9]
    },
    type_hollow : {
        'x': [ 0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0, 0, 0.6*-1, 0.6*-1*s3, 0.6*-2, 0.6*-1*s3, 0.6*-1, 0.6*0, 0.6*1, 0.6*1*s3, 0.6*2, 0.6*1*s3, 0.6*1, 0, 0 ],
        'y': [ 2, 1, -1, -2, -1, 1, 2, 0.6*2, 0.6*s3, 0.6*1, 0.6*0, 0.6*-1, 0.6*-1*s3, 0.6*-2, 0.6*-1*s3, 0.6*-1, 0.6*0, 0.6*1, 0.6*s3, 0.6*2, 2 ]
    },
    type_pentagon_hollow : {
        'x': [0, 1*s3, 1*s3, -1*s3, -1*s3, 0, 0, 0.6*-1, 0.6*-1*s3, 0.6*-2, 0.6*-1*s3, 0.6*-1, 0.6*0, 0.6*1, 0.6*1*s3, 0.6*2, 0.6*1*s3, 0.6*1, 0, 0],
        'y': [2, 1, -2, -2, 1, 2, 1.2, 0.6*s3, 0.6*1, 0.6*0, 0.6*-1, 0.6*-1*s3, 0.6*-2, 0.6*-1*s3, 0.6*-1, 0.6*0, 0.6*1, 0.6*s3, 1.2, 2]
    },
    type_circle : {
        'x': [0, 1, 1*s3, 2, 1*s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0],
        'y': [2, s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0, 1, s3, 2]
    },
}

# Define derived polygon types that use rotation in PolygonManager
base_derived_types = {
    type_HD_hexagon_side3_corner3: base[type_HD_hexagon_side1_corner1],
    type_HD_hexagon_side3_corner4: base[type_HD_hexagon_side1_corner2],
    type_HD_hexagon_side5_corner5: base[type_HD_hexagon_side1_corner1],
    type_HD_hexagon_side5_corner6: base[type_HD_hexagon_side1_corner2],
    type_HD_trpezoid_corner3: base[type_HD_trpezoid_corner1],
    type_HD_trpezoid_corner4: base[type_HD_trpezoid_corner2],
    type_HD_trpezoid_corner5: base[type_HD_trpezoid_corner1],
    type_HD_trpezoid_corner6: base[type_HD_trpezoid_corner2],
    type_HD_hexagon_side2_corner3: base[type_HD_hexagon_side6_corner1],
    type_HD_hexagon_side4_corner4: base[type_HD_hexagon_side2_corner2],
    type_HD_hexagon_side4_corner5: base[type_HD_hexagon_side6_corner1],
    type_HD_hexagon_side6_corner6: base[type_HD_hexagon_side2_corner2],
}

base.update(base_derived_types)

#----------------------------------------------------------------------------------------------------
# Irregular polygons mapping using SiCell padID 
#----------------------------------------------------------------------------------------------------
irregular_polygonal_cells = {
    "ML-F": {
        type_pentagon_side1 : [2, 3, 4, 5, 6, 7],
        type_pentagon_side2 : [18, 28, 39, 51, 65, 80, 95],
        type_pentagon_side3 : [126, 140, 155, 168, 179, 189],
        type_pentagon_side4 : [191, 192, 193, 194, 195, 196, 197],
        type_pentagon_side5 : [112, 127, 141, 156, 169, 180],
        type_pentagon_side6 : [9, 19, 29, 40, 52, 66, 81],
        type_pentagon_corner1 : [1],
        type_pentagon_corner2 : [8],
        type_pentagon_corner3 : [111],
        type_pentagon_corner4 : [198],
        type_pentagon_corner5 : [190],
        type_pentagon_corner6 : [96],
        type_hexagon_corner1 : [9],
        type_hexagon_corner2 : [18],
        type_hexagon_corner3 : [95],
        type_hexagon_corner4 : [197],
        type_hexagon_corner5 : [191],
        type_hexagon_corner6 : [81],
        type_hollow : [13, 61, 69, 142, 153, 162], # cells around a calib channel
        # type_hexagon_small : [14, 62, 70, 143, 154, 163], # calibration_cells
    },
    "ML-L" : {
        type_hollow : [12, 168], # cells around a calib channel
        type_pentagon_hollow : [89], # cells around a calib channel
        # type_hexagon_small : [13, 90, 169], # calibration_cells
        type_trapezoid_left : [14, 35, 61, 126, 157, 185],
        type_trapezoid_extended_left : [93, 207],
        type_pentagon_side1 : [2, 3, 4, 104, 105, 106, 107, 108, 109, 110],
        type_pentagon_side4 : [86, 87, 88, 91, 92, 205, 206],
        type_pentagon_side5 : [119, 136, 151, 167, 180, 193],
        type_pentagon_side6 : [20, 30, 43, 55, 71],
        type_pentagon_corner1 : [1],
        type_pentagon_corner5 : [203],
        type_partial_wafer_pentagon_corner6 : [103],
        type_hexagon_corner1 : [9],
        type_hexagon_corner5 : [204],
        type_partial_wafer_hexagon_corner6 : [85],
    },
    "ML-5" : {
        type_hollow : [12, 64, 159, 168], # cells around a calib channel
        type_pentagon_hollow : [89], # cells around a calib channel
        type_hexagon_small : [13, 65, 90, 160, 169], # calibration_cells
        type_trapezoid_left : [19, 40, 67, 131, 163, 190],
        type_trapezoid_extended_left : [98, 212],
        type_pentagon_side1 : [2, 3, 4, 5, 6, 7, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114],
        type_pentagon_side4 : [86, 87, 88, 91, 92, 93, 95, 96, 97, 205, 206, 207, 209, 210, 211],
        type_pentagon_side5 : [119, 136, 151, 167, 180, 193],
        type_pentagon_side6 : [20, 30, 43, 55, 71],
        type_pentagon_corner1 : [1],
        type_pentagon_corner5 : [203],
        type_partial_wafer_pentagon_corner6 : [103],
        type_hexagon_corner1 : [9],
        type_hexagon_corner4 : [211],
        type_hexagon_corner5 : [204],
        type_parallelogram : [212],
        type_partial_wafer_hexagon_corner2 : [8],
        type_partial_wafer_hexagon_corner6 : [85],
    },
    "ML-T" : {
        type_hollow : [12, 64], # cells around a calib channel
        type_pentagon_hollow : [89], # cells around a calib channel
        type_hexagon_small : [13, 65, 90], # calibration_cells
        type_trapezoid_left : [19],
        type_pentagon_side1 : [2, 3, 4, 5, 6, 7],
        type_pentagon_side2 : [42, 54, 70, 84],
        type_pentagon_side4 : [86, 87, 88, 91, 92, 93, 95, 96, 97, 98, 100, 101],
        type_pentagon_side6 : [20, 30, 43, 55, 71],
        type_pentagon_corner1 : [1],
        type_hexagon_corner1 : [9],
        type_partial_wafer_hexagon_corner2 : [8],
        type_partial_wafer_hexagon_corner3 : [102],
        type_partial_wafer_hexagon_corner6 : [85],
        type_partial_wafer_pentagon_merged_cell_corner2 : [29],
    },
    "ML-B" : {
        type_hollow : [148, 159, 168], # cells around a calib channel
        type_hexagon_small : [149, 160, 169], # calibration_cells
        type_pentagon_side1 : [104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117],
        type_pentagon_side3 : [135, 150, 166, 179, 192],
        type_pentagon_side4 : [205, 206, 207, 209, 210, 211],
        type_pentagon_side5 : [119, 136, 151, 167, 180, 193],
        type_pentagon_corner5 : [203],
        type_hexagon_corner4 : [211],
        type_hexagon_corner5 : [204],
        type_parallelogram : [212],
        type_partial_wafer_pentagon_corner3 : [118],
        type_partial_wafer_pentagon_corner6 : [103],
        type_partial_wafer_pentagon_merged_cell_corner4 : [202],
    },
    "ML-R" : {
        type_hollow : [64, 148, 159],
        # type_hexagon_small : [65, 149, 160],
        type_trapezoid_right : [15, 36, 62, 127, 158, 186], # 41, 68, 132, 164, 191],
        type_trapezoid_extended_right : [94, 208, 99],
        type_trapezoid_left : [19], # 40, 67, 131, 163, 190],
        type_parallelogram : [212],
        type_pentagon_side1 : [5, 6, 7, 111, 112, 113, 114, 115, 116, 117],
        type_pentagon_side2 : [42, 54, 70, 84],
        type_pentagon_side3 : [135, 150, 166, 179, 192],
        type_pentagon_side4 : [209, 210, 95, 96, 97, 98, 99, 100, 101],
        type_partial_wafer_pentagon_corner3 : [118],
        type_partial_wafer_pentagon_merged_cell_corner2 : [29],
        type_partial_wafer_pentagon_merged_cell_corner4 : [202],
        type_partial_wafer_hexagon_corner3 : [102],
        type_partial_wafer_hexagon_corner2 : [8],
        type_hexagon_corner4 : [211],
    },
    "MH-F" : {
        type_hollow : [29, 150, 157, 36, 387, 411, 297, 267, 261, 87, 207, 381], # cells around a calib channel
        type_pentagon_side1 : [3, 4, 5, 6, 7, 8, 9, 10],
        type_pentagon_side2 : [41, 56, 72, 90, 108, 127, 147, 170, 192],
        type_pentagon_side3 : [287, 309, 329, 348, 366, 384, 401, 417],
        type_pentagon_side4 : [434, 435, 436, 437, 438, 439, 440, 441, 442],
        type_pentagon_side5 : [265, 288, 310, 330, 349, 367, 385, 402],
        type_pentagon_side6 : [26, 42, 57, 73, 91, 109, 128, 148, 171],
        type_HD_hexagon_side1_corner1 : [2],
        type_HD_hexagon_side1_corner2 : [11],
        type_HD_trpezoid_corner1 : [1],
        type_HD_trpezoid_corner2 : [12],
        type_HD_hexagon_side6_corner1 : [13],
        type_HD_hexagon_side2_corner2 : [25],

        type_HD_hexagon_side3_corner3 : [264], # by rotation
        type_HD_trpezoid_corner3 : [240], # by rotation
        type_HD_hexagon_side2_corner3 : [216], # by rotation

        type_HD_hexagon_side3_corner4 : [431], # by rotation
        type_HD_trpezoid_corner4 : [444], # by rotation
        type_HD_hexagon_side4_corner4 : [443], # by rotation

        type_HD_hexagon_side5_corner5 : [418], # by rotation
        type_HD_trpezoid_corner5 : [432], # by rotation
        type_HD_hexagon_side4_corner5 : [433], # by rotation

        type_HD_hexagon_side5_corner6 : [241], # by rotation
        type_HD_trpezoid_corner6 : [217], # by rotation
        type_HD_hexagon_side6_corner6 : [193], # by rotation
    },
    "MH-T" : {
        type_hollow : [30, 38, 113, 138, 145], # cells around a calib channel
        type_hexagon_small : [31, 39, 114, 139, 146], # calibration_cells
        type_pentagon_side1 : [3, 5, 6, 7, 8, 9, 10, 11],
        type_pentagon_side2 : [45, 60, 78, 95, 116, 135, 159],
        type_pentagon_side6 : [28, 46, 61, 79, 96, 117, 136],

        type_HD_quadrilaterals_corner3 : [180],
        type_HD_quadrilaterals_corner6 : [160],
        type_pentagon_truncated_side4 : [161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179],

        type_HD_trpezoid_corner1 : [1],
        type_HD_trpezoid_corner2 : [14],
        type_HD_hexagon_side1_corner1 : [2],
        type_HD_hexagon_side1_corner2 : [13],
        type_HD_hexagon_side6_corner1 : [15],
        type_HD_hexagon_side2_corner2 : [27],
    },
    "MH-B" : {
        type_hollow : [220, 252, 305, 334, 384, 425, 432], # cells around a calib channel
        type_hexagon_small : [221, 253, 306, 335, 385, 426, 433], # calibration_cells

        type_pentagon_extended_side1 : [182, 183, 184, 185, 186, 187, 188, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202, 203],
        type_pentagon_extended_corner1 : [181],
        type_pentagon_extended_corner2 : [204],
        type_pentagon_side3 : [278, 302, 324, 347, 366, 387, 404, 422, 439],
        type_pentagon_side4 : [466, 465, 464, 463, 462, 461, 460, 459, 458],
        type_pentagon_side5 : [279, 303, 325, 348, 367, 388, 405, 423],

        type_HD_hexagon_side3_corner3 : [278], # by rotation
        type_HD_trpezoid_corner3 : [255], # by rotation
        type_HD_hexagon_side2_corner3 : [228], # by rotation

        type_HD_hexagon_side3_corner4 : [455], # by rotation
        type_HD_trpezoid_corner4 : [468], # by rotation
        type_HD_hexagon_side4_corner4 : [467], # by rotation

        type_HD_hexagon_side5_corner5 : [440], # by rotation
        type_HD_trpezoid_corner5 : [456], # by rotation
        type_HD_hexagon_side4_corner5 : [457], # by rotation

        type_HD_hexagon_side5_corner6 : [256], # by rotation
        type_HD_trpezoid_corner6 : [229], # by rotation
        type_HD_hexagon_side6_corner6 : [205], # by rotation
    },
    "MH-L" : {
        type_hollow : [30, 138, 305, 425], # cells around a calib channel
        type_hexagon_small : [31, 139, 306, 426], # calibration_cells

        type_pentagon_side6 : [28, 46, 61, 79, 96, 117, 136],
        type_pentagon_extended_side1 : [182, 183, 184, 185, 186, 187],
        type_pentagon_side4 : [458],
        type_pentagon_side5 : [279, 303, 325, 348, 367, 388, 405, 423],

        type_trapezoid_left : [32, 65, 101, 143, 237, 286, 331, 372, 409, 443],
        type_HD_quadrilaterals_left_side1 : [3],
        type_HD_quadrilaterals_extended_left_side1 : [188],

        type_HD_quadrilaterals_corner6 : [160],
        type_pentagon_truncated_side4 : [161, 162, 163, 164, 165, 166],

        type_HD_trpezoid_corner1 : [1],
        type_HD_hexagon_side1_corner1 : [2],
        type_HD_hexagon_side6_corner1 : [15],
        type_pentagon_extended_corner1 : [181],

        type_HD_hexagon_side5_corner5 : [440], # by rotation
        type_HD_trpezoid_corner5 : [456], # by rotation
        type_HD_hexagon_side4_corner5 : [457], # by rotation

        type_HD_hexagon_side5_corner6 : [256], # by rotation
        type_HD_trpezoid_corner6 : [229], # by rotation
        type_HD_hexagon_side6_corner6 : [205], # by rotation
    },
    "MH-R" : {
        type_hollow : [113, 220, 252, 384], # cells around a calib channel
        type_hexagon_small : [114, 221, 253, 385], # calibration_cells

        # left edge
        type_HD_quadrilaterals_right_side1 : [12],
        type_HD_quadrilaterals_extended_right_side1 : [197],
        type_trapezoid_right : [42, 74, 110, 153, 246, 295, 341, 381, 418, 452],

        # upper edges
        type_pentagon_side2 : [45, 60, 78, 95, 116, 135, 159],
        type_HD_quadrilaterals_corner3 : [180],
        type_pentagon_truncated_side4 : [174, 175, 176, 177, 178, 179],

        # top corner
        type_HD_trpezoid_corner2 : [14],
        type_HD_hexagon_side1_corner2 : [13],
        type_HD_hexagon_side2_corner2 : [27],

        # lower edges
        type_pentagon_extended_side1 : [198, 199, 200, 201, 202, 203],
        type_pentagon_extended_corner2 : [204],
        type_pentagon_side3 : [278, 302, 324, 347, 366, 387, 404, 422, 439],
        type_pentagon_side4 : [466],

        type_HD_hexagon_side3_corner3 : [278], # by rotation
        type_HD_trpezoid_corner3 : [255], # by rotation
        type_HD_hexagon_side2_corner3 : [228], # by rotation

        type_HD_hexagon_side3_corner4 : [455], # by rotation
        type_HD_trpezoid_corner4 : [468], # by rotation
        type_HD_hexagon_side4_corner4 : [467], # by rotation
    },
}
