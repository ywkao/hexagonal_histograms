#!/usr/bin/env python2
import math

#--------------------------------------------------
# Define constants and types
#--------------------------------------------------
s2 = math.sqrt(2)
s3 = math.sqrt(3)
pi = math.pi

type_square = 4
type_regular_pentagon = 5
type_hexagon = 6
type_hexagon_small = 7
type_hollow = 8
type_circle = 12 

type_pentagon_corner1 = 41
type_pentagon_corner2 = 42
type_pentagon_corner3 = 43
type_pentagon_corner4 = 44
type_pentagon_corner5 = 45
type_pentagon_corner6 = 46
type_pentagon_side1 = 51
type_pentagon_side2 = 52
type_pentagon_side3 = 53
type_pentagon_side4 = 54
type_pentagon_side5 = 55
type_pentagon_side6 = 56

#--------------------------------------------------
# Coordinates of calib and CM channels
#--------------------------------------------------
# calibration channels and hollow channels
calibration_cells = [14, 62, 70, 143, 154, 163]
hollow_cells = [13, 61, 69, 142, 153, 162]

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

# Coordinates of CM channels
Coordinates_CM_channels = {
	'x' : [-10, -5, 5, 10],
	'y' : [30, 30, 30, 30],
}

#--------------------------------------------------
# Define base polygons
#--------------------------------------------------
base = {
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
	type_pentagon_corner1 : {
		'x': [-1/s3, 1*s3, 1*s3, 0, -1.5*s3, -1/s3],
	 	'y': [1, 1, -1, -2, -0.5, 1]
	},
	type_pentagon_corner2 : {
		'x': [1/s3,1.5*s3, 0, -1*s3, -1*s3, 1/s3],
	 	'y': [1, -0.5, -2, -1, 1, 1]
	},
	type_pentagon_corner3 : {
		'x': [0.5*s3, 2/s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2.5, 0, -2, -1, 1, 2]
	},
	type_pentagon_corner4 : {
		'x': [0, 1*s3, 1/s3, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -1, -2, 1, 2]
	},
	type_pentagon_corner5 : {
		'x': [0, 1*s3, 1*s3, -1/s3, -1*s3, 0],
	 	'y': [2, 1, -2, -1, 1, 2]
	},
	type_pentagon_corner6 : {
		'x': [-0.5*s3, 1*s3, 1*s3, 0, -2/s3, -0.5*s3],
	 	'y': [2.5, 1, -1, -2, 0, 2.5]
	},
	type_square : {
		'x' : [s2, s2, -s2, -s2, s2],
		'y' : [s2, -s2, -s2, s2, s2]
	},
	type_regular_pentagon : {
		'x' : [0, 2*math.cos(pi/10.), 2*math.cos(17.*pi/10.), 2*math.cos(13.*pi/10.), 2*math.cos(9.*pi/10.), 0],
		'y' : [2, 2*math.sin(pi/10.), 2*math.sin(17.*pi/10.), 2*math.sin(13.*pi/10.), 2*math.sin(9.*pi/10.), 2],
	},
	type_hexagon : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0],
	 	'y': [2, 1, -1, -2, -1, 1, 2]
	},
	type_hexagon_small : {
		'x': [0, 0.45*s3, 0.45*s3, 0, -0.45*s3, -0.45*s3, 0],
	 	'y': [0.9, 0.45, -0.45, -0.9, -0.45, 0.45, 0.9]
	},
	type_hollow : {
		'x': [0, 1*s3, 1*s3, 0, -1*s3, -1*s3, 0, 0, -0.6*s3, -0.6*s3, 0, 0.6*s3, 0.6*s3, 0, 0],
	 	'y': [2, 1, -1, -2, -1, 1, 2, 1.2, 0.6, -0.6, -1.2, -0.6, 0.6, 1.2, 2]
	},
	type_circle : {
		'x': [0, 1, 1*s3, 2, 1*s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0],
	 	'y': [2, s3, 1, 0, -1, -1*s3, -2, -1*s3, -1, 0, 1, s3, 2]
	},
}

LD_pentapon_cells = {
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
}

LD_pentapon_cells_all = []
for i in range(type_pentagon_side1, type_pentagon_side6+1):
	LD_pentapon_cells_all += LD_pentapon_cells[i] 
