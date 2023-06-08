#!/usr/bin/env python2
import json

with open("data/output_my_coordinate_data.json", 'r') as f:
	data = f.read()
	json_data = json.loads(data)

def get_coordinate(tuple_query):
	channel, point = tuple_query
	x = json_data[str(channel)]["x"][point]
	y = json_data[str(channel)]["y"][point]
	return x, y

def get_mean_coordinate(list_queries):
	lx, ly = [], []
	for query in list_queries:
		x, y = get_coordinate(query)
		lx.append(x)
		ly.append(y)

	average_x, average_y = sum(lx)/len(lx), sum(ly)/len(ly)	
	return average_x, average_y

def get_collection_xy(line):
	output_list_x, output_list_y = [], []
	for ele in line:
		channels = ele[0]
		corners  = ele[1]
		query = zip(channels, corners)
		x, y = get_mean_coordinate(query)
		output_list_x.append(x)
		output_list_y.append(y)
	return output_list_x, output_list_y

def print_coordinate(varName, query):
	varx, vary = varName
	x, y = get_collection_xy(query)
	output_x = "double %s[N] = {" % varx
	output_y = "double %s[N] = {" % vary

	for i in range(len(x)):
		if not i+1==len(x):
			output_x += "%f, " % x[i]
			output_y += "%f, " % y[i]
		else:
			output_x += "%f};" % x[i]
			output_y += "%f};" % y[i]

	print output_x
	print output_y

if __name__ == "__main__":
	import queries_for_coordinates as tc
	print_coordinate(("x1", "y1"), tc.query_line1)
	print_coordinate(("x2", "y2"), tc.query_line2)
	print_coordinate(("x3", "y3"), tc.query_line3)
