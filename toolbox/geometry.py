#!/usr/bin/env python2
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
type_pentagon_hollow = 13
type_hollow = 14

type_trapezoid_left = 41
type_trapezoid_extended_left = 42

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
type_hexagon_corner1 = 601
type_hexagon_corner2 = 602
type_hexagon_corner3 = 603
type_hexagon_corner4 = 604
type_hexagon_corner5 = 605
type_hexagon_corner6 = 606
type_partial_wafer_hexagon_corner6 = 607

type_HD_hexagon_side1_corner1 = 608
type_HD_hexagon_side6_corner1 = 609
type_HD_trpezoid_corner1 = 401

# information of CM and NC in global Id (readout sequence)
global_channel_Id_special_channels = {
    "partial" : {
        "CMIds" : [37, 38, 76, 77, 115, 116],
        "NonConnIds" : [8, 17, 47, 56, 58, 67, 86, 95]
    },
    "full" : {
        "CMIds" : [37, 38, 76, 77, 115, 116, 154, 155, 193, 194, 232, 233],
        "NonConnIds" : [8, 17, 19, 28, 47, 56, 58, 67, 86, 95, 97, 106, 125, 134, 136, 145, 164, 173, 175, 184, 203, 212, 214, 223]
    },
    "HD" : {
        "CMIds" : [37, 38, 76, 77, 115, 116, 154, 155, 193, 194, 232, 233, 271, 272, 310, 311, 349, 350, 388, 389, 427, 428, 466, 467],
        "NonConnIds" : [8, 17, 19, 28, 47, 56, 58, 67, 86, 95, 97, 106, 125, 134, 136, 145, 164, 173, 175, 184, 203, 212, 214, 223]
    },
}

gcId = global_channel_Id_special_channels

#--------------------------------------------------
# Coordinates of calib and CM channels
#--------------------------------------------------

# Coordinates of calibration channels
calib_distance_factor = 14.
Coordinates_calib_channels = {
	14  : (0, 2),
	62  : (s3, 1),
	154 : (s3, -1),
	163 : (0, -2),
	143 : (-1*s3, -1),
	70  : (-1*s3, 1),
}

# Coordinates of CM and NC channels
Coordinates_CM_channels = {
    "partial": {
	    'x' : [-8.75, -3.75, 3.75, 8.75, 8.75, 3.75],
	    'y' : [29, 29, 29, 29, 29, 29],
        'theta' : [-p3, -p3, -p3, -p3, p3*3, p3*3]
    },
    "full": {
	    'x' : [8.75, 3.75, -3.75, -8.75],
	    'y' : [29, 29, 29, 29],
    },
    "HD": {
	    'x' : [14., 10.5, 7.0, 3.5, -3.5, -7.0, -10.5, -14.],
	    'y' : [45, 45, 45, 45, 45, 45, 45, 45],
    },
}

Coordinates_NC_channels = {
    "partial": {
	    'x' : [-7.5, -5.0, 2.5, 5.0, 7.5, 10., 7.5, 5.0],
	    'y' : [32, 32, 32, 32, 32, 32, 32, 32],
        'theta' : [-p3, -p3, -p3, -p3, -p3, -p3, p3*3, p3*3]
    },
    "full": {
	    'x' : [10., 7.5, 5.0, 2.5, -2.5, -5.0, -7.5, -10.],
	    'y' : [32, 32, 32, 32, 32, 32, 32, 32],
    },
    "HD": {
	    'x' : [10., 7.5, 5.0, 2.5, -2.5, -5.0, -7.5, -10.],
	    'y' : [32, 32, 32, 32, 32, 32, 32, 32],
    },
}

#--------------------------------------------------
# Define base polygons
#--------------------------------------------------
base = {
	type_hexagon : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0],
		'y': [2, 1, -1, -2, -1, 1, 2]
	},
	type_trapezoid_left : {
		'x': [0, 0, -1*s3, -1*s3, 0],
	    'y': [2, -2, -1, 1, 2]
	},
	type_trapezoid_extended_left : {
		'x': [0, 0, -1*s3, -1*s3, 0],
	    'y': [2, -2, -2, 1, 2]
	},
	type_HD_hexagon_side1_corner1 : {
		'x': [1*s3, 1*s3, 0, -1*s3, -1*s3, -0.5*s3, 1*s3],
        'y': [1, -1, -2, -1, 0.5, 1, 1]
	},
	type_HD_trpezoid_corner1 : {
		'x': [1*s3, 1*s3, 0, -0.75*s3, s3],
        'y': [0.5, -1, -2, -1.25, 0.5]
	},
	type_HD_hexagon_side6_corner1 : {
		'x': [0.25*s3, 1*s3, 1*s3, 0, -1.5*s3, -1.25*s3, 0.25*s3],
        'y': [1.75, 1, -1, -2, -0.5, 0.25, 1.75]
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
		'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0, 0, -0.6*s3, -0.6*s3, 0, 0.6*s3, 0.6*s3, 0, 0],
	 	'y': [2, 1, -1, -2, -1, 1, 2, 1.2, 0.6, -0.6, -1.2, -0.6, 0.6, 1.2, 2]
	},
	type_pentagon_hollow : {
		'x': [0, 1*s3, 1*s3, -1*s3, -1*s3, 0, 0, -0.6*s3, -0.6*s3, 0, 0.6*s3, 0.6*s3, 0, 0],
	 	'y': [2, 1, -2, -2, 1, 2, 1.2, 0.6, -0.6, -1.2, -0.6, 0.6, 1.2, 2]
	},
	type_circle : {
		'x': [0, 1, 1*s3, 2, 1*s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0],
	 	'y': [2, s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0, 1, s3, 2]
	},
}

special_cells = { # dictionary for special cells using sicell padID
    "full": {
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
        type_hexagon_small : [14, 62, 70, 143, 154, 163], # calibration_cells
    },
    "partial" : {
        #--------------------------------------------------
        # Next to-do tuning:
        # 89 has to be a hollow pentagon
        # 85 is a pentagon
        # 14, 35, 61, 93, 126, 157, 185, 207 have to be cut half
        #--------------------------------------------------
        type_hollow : [12, 168], # cells around a calib channel
        type_pentagon_hollow : [89], # cells around a calib channel
        type_hexagon_small : [13, 90, 169], # calibration_cells
        type_trapezoid_left : [14, 35, 61, 126, 157, 185],
        type_trapezoid_extended_left : [93, 207],
	    type_pentagon_side1 : [2, 3, 4, 104, 105, 106, 107, 108, 109, 110],
	    type_pentagon_side4 : [86, 87, 88, 91, 92, 93, 205, 206, 207],
	    type_pentagon_side5 : [119, 136, 151, 167, 180, 193],
	    type_pentagon_side6 : [20, 30, 43, 55, 71],
	    type_pentagon_corner1 : [1],
	    type_pentagon_corner5 : [203],
	    type_partial_wafer_pentagon_corner6 : [103],
	    type_hexagon_corner1 : [9],
	    type_hexagon_corner5 : [204],
	    type_partial_wafer_hexagon_corner6 : [85],
    },
    "HD" : {
        type_hollow : [29, 150, 157, 36, 387, 411, 297, 267, 261, 87, 207, 381], # cells around a calib channel
	    type_pentagon_side1 : [3, 4, 5, 6, 7, 8, 9, 10],
	    type_pentagon_side2 : [41, 56, 72, 90, 108, 127, 147, 170, 192],
	    type_pentagon_side3 : [287, 309, 329, 348, 366, 384, 401, 417],
	    type_pentagon_side4 : [434, 435, 436, 437, 438, 439, 440, 441, 442],
	    type_pentagon_side5 : [265, 288, 310, 330, 349, 367, 385, 402],
	    type_pentagon_side6 : [26, 42, 57, 73, 91, 109, 128, 148, 171],
	    type_hexagon_corner2 : [25],
	    type_hexagon_corner3 : [216],
	    type_hexagon_corner4 : [443],
	    type_hexagon_corner5 : [433],
	    type_hexagon_corner6 : [193],
        type_HD_hexagon_side1_corner1 : [2],
        type_HD_hexagon_side6_corner1 : [13],
        type_HD_trpezoid_corner1 : [1],
    },
}
