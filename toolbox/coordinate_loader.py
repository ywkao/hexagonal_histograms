#!/usr/bin/env python2
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-w', '--waferType', help="set wafer type (LD3, full, HD)", type=str, default="full")
args = parser.parse_args()

if args.waferType == "HD":
    json_file = "data/output_my_coordinate_HD_wafer.json"
elif args.waferType == "full": # LD full
    json_file = "data/output_my_coordinate_data.json"
elif args.waferType == "LD3":
    json_file = "data/output_my_coordinate_LD3_wafer.json"
elif args.waferType == "LD4":
    json_file = "data/output_my_coordinate_LD4_wafer.json"

with open(json_file, 'r') as f:
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

def print_coordinate(varName, query, num="N_boundary_points"):
    varx, vary = varName
    x, y = get_collection_xy(query)
    output_x = "double %s[%s] = {" % (varx, num)
    output_y = "double %s[%s] = {" % (vary, num)

    for i in range(len(x)):
        if not i+1==len(x):
            output_x += "%f, " % x[i]
            output_y += "%f, " % y[i]
        else:
            output_x += "%f};" % x[i]
            output_y += "%f};" % y[i]

    fout.write(output_x+'\n')
    fout.write(output_y+'\n')
    print output_x
    print output_y

if __name__ == "__main__":
    import queries_for_coordinates as tc

    if args.waferType == "full": # LD full
        fout = open("include/auxiliary_boundary_lines.h", 'w')
        fout.write("#ifndef __auxiliary_boundary_lines__\n")
        fout.write("#define __auxiliary_boundary_lines__\n")
        fout.write("\n")

        fout.write("namespace aux {\n")
        fout.write("const int N_boundary_points = 16;\n")
        fout.write("\n")
        print_coordinate(("x1", "y1"), tc.query_line1)
        print_coordinate(("x2", "y2"), tc.query_line2)
        print_coordinate(("x3", "y3"), tc.query_line3)
        print_coordinate(("x4", "y4"), tc.query_line4)
        print_coordinate(("x5", "y5"), tc.query_line5)
        print_coordinate(("x6", "y6"), tc.query_line6)
        fout.write("}; // end of aux\n")

        fout.write("\n")
        fout.write("#endif // __auxiliary_boundary_lines__\n")
        fout.close()

    elif args.waferType == "LD3":
        fout = open("include/auxiliary_boundary_lines_partial_wafer.h", 'w')
        fout.write("#ifndef __auxiliary_boundary_lines_partial_wafer__\n")
        fout.write("#define __auxiliary_boundary_lines_partial_wafer__\n")
        fout.write("\n")

        fout.write("namespace aux {\n")
        print_coordinate(("x1_partial_wafer", "y1_partial_wafer"), tc.query_partial_wafer_line1, "15")
        print_coordinate(("x2_partial_wafer", "y2_partial_wafer"), tc.query_partial_wafer_line2, "17")
        fout.write("}; // end of aux\n")

        fout.write("\n")
        fout.write("#endif // __auxiliary_boundary_lines_partial_wafer__\n")
        fout.close()

    elif args.waferType == "LD4":
        fout = open("include/auxiliary_boundary_lines_LD4_partial_wafer.h", 'w')
        fout.write("#ifndef __auxiliary_boundary_lines_LD4_partial_wafer__\n")
        fout.write("#define __auxiliary_boundary_lines_LD4_partial_wafer__\n")
        fout.write("\n")

        fout.write("namespace aux {\n")
        print_coordinate(("x1_LD4_partial_wafer", "y1_LD4_partial_wafer"), tc.query_LD4_wafer_line1, "15")
        print_coordinate(("x2_LD4_partial_wafer", "y2_LD4_partial_wafer"), tc.query_LD4_wafer_line2, "17")
        fout.write("}; // end of aux\n")

        fout.write("\n")
        fout.write("#endif // __auxiliary_boundary_lines_LD4_partial_wafer__\n")
        fout.close()

    elif args.waferType == "HD":
        fout = open("include/auxiliary_boundary_lines_HD_full_wafer.h", 'w')
        fout.write("#ifndef __auxiliary_boundary_lines_HD_full_wafer__\n")
        fout.write("#define __auxiliary_boundary_lines_HD_full_wafer__\n")
        fout.write("\n")

        fout.write("namespace aux {\n")
        fout.write("const int N_HD_boundary_points = 24;\n")
        fout.write("\n")
        print_coordinate(("x1_HD_full_wafer", "y1_HD_full_wafer"), tc.query_HD_full_wafer_line1, "N_HD_boundary_points")
        print_coordinate(("x2_HD_full_wafer", "y2_HD_full_wafer"), tc.query_HD_full_wafer_line2, "N_HD_boundary_points")
        print_coordinate(("x3_HD_full_wafer", "y3_HD_full_wafer"), tc.query_HD_full_wafer_line3, "N_HD_boundary_points")
        print_coordinate(("x4_HD_full_wafer", "y4_HD_full_wafer"), tc.query_HD_full_wafer_line4, "N_HD_boundary_points")
        print_coordinate(("x5_HD_full_wafer", "y5_HD_full_wafer"), tc.query_HD_full_wafer_line5, "N_HD_boundary_points")
        print_coordinate(("x6_HD_full_wafer", "y6_HD_full_wafer"), tc.query_HD_full_wafer_line6, "N_HD_boundary_points")
        fout.write("}; // end of aux\n")

        fout.write("\n")
        fout.write("#endif // __auxiliary_boundary_lines_HD_full_wafer__\n")
        fout.close()
