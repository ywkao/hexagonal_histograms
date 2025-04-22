import os
import sys
import json

utils_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(utils_dir)

import queries_for_coordinates as tc

class AuxiliaryLineProducer():
    def __init__(self, waferType, json_file):
        self.waferType = waferType

        # Load JSON data
        try:
            with open(json_file, 'r') as f:
                self.json_data = json.loads(f.read())
        except FileNotFoundError:
            print(f"Error: Could not find file {json_file}")
            self.json_data = {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file {json_file}")
            self.json_data = {}

    def get_coordinate(self, tuple_query):
        channel, point = tuple_query
        x = self.json_data[str(channel)]["x"][point]
        y = self.json_data[str(channel)]["y"][point]
        return x, y

    def get_mean_coordinate(self, list_queries):
        lx, ly = [], []
        for query in list_queries:
            x, y = self.get_coordinate(query)
            lx.append(x)
            ly.append(y)

        average_x, average_y = sum(lx)/len(lx), sum(ly)/len(ly)
        return average_x, average_y

    def get_collection_xy(self, line):
        output_list_x, output_list_y = [], []
        for ele in line:
            channels = ele[0]
            corners  = ele[1]
            query = zip(channels, corners)
            x, y = self.get_mean_coordinate(query)
            output_list_x.append(x)
            output_list_y.append(y)
        return output_list_x, output_list_y

    def print_coordinate(self, varName, query, num="N_boundary_points"):
        varx, vary = varName
        x, y = self.get_collection_xy(query)
        output_x = "double %s[%s] = {" % (varx, num)
        output_y = "double %s[%s] = {" % (vary, num)

        for i in range(len(x)):
            if not i+1==len(x):
                output_x += "%f, " % x[i]
                output_y += "%f, " % y[i]
            else:
                output_x += "%f};" % x[i]
                output_y += "%f};" % y[i]

        self.fout.write(output_x+'\n')
        self.fout.write(output_y+'\n')
        # print(output_x)
        # print(output_y)

    def create_cpp_headers(self):
        if self.waferType == "full": # LD full
            fname = "./scripts/include/auxiliary_boundary_lines.h"
            self.fout = open(fname, 'w')
            self.fout.write("#ifndef __auxiliary_boundary_lines__\n")
            self.fout.write("#define __auxiliary_boundary_lines__\n")
            self.fout.write("\n")

            self.fout.write("namespace aux {\n")
            self.fout.write("const int N_boundary_points = 16;\n")
            self.fout.write("\n")
            self.print_coordinate(("x1", "y1"), tc.query_line1)
            self.print_coordinate(("x2", "y2"), tc.query_line2)
            self.print_coordinate(("x3", "y3"), tc.query_line3)
            self.print_coordinate(("x4", "y4"), tc.query_line4)
            self.print_coordinate(("x5", "y5"), tc.query_line5)
            self.print_coordinate(("x6", "y6"), tc.query_line6)
            self.fout.write("}; // end of aux\n")

            self.fout.write("\n")
            self.fout.write("#endif // __auxiliary_boundary_lines__\n")
            self.fout.close()

        elif self.waferType == "LD3":
            fname = "./scripts/include/auxiliary_boundary_lines_partial_wafer.h"
            self.fout = open(fname, 'w')
            self.fout.write("#ifndef __auxiliary_boundary_lines_partial_wafer__\n")
            self.fout.write("#define __auxiliary_boundary_lines_partial_wafer__\n")
            self.fout.write("\n")

            self.fout.write("namespace aux {\n")
            self.print_coordinate(("x1_partial_wafer", "y1_partial_wafer"), tc.query_partial_wafer_line1, "15")
            self.print_coordinate(("x2_partial_wafer", "y2_partial_wafer"), tc.query_partial_wafer_line2, "17")
            self.fout.write("}; // end of aux\n")

            self.fout.write("\n")
            self.fout.write("#endif // __auxiliary_boundary_lines_partial_wafer__\n")
            self.fout.close()

        elif self.waferType == "LD4":
            fname = "./scripts/include/auxiliary_boundary_lines_LD4_partial_wafer.h"
            self.fout = open(fname, 'w')
            self.fout.write("#ifndef __auxiliary_boundary_lines_LD4_partial_wafer__\n")
            self.fout.write("#define __auxiliary_boundary_lines_LD4_partial_wafer__\n")
            self.fout.write("\n")

            self.fout.write("namespace aux {\n")
            self.print_coordinate(("x1_LD4_partial_wafer", "y1_LD4_partial_wafer"), tc.query_LD4_wafer_line1, "15")
            self.print_coordinate(("x2_LD4_partial_wafer", "y2_LD4_partial_wafer"), tc.query_LD4_wafer_line2, "17")
            self.fout.write("}; // end of aux\n")

            self.fout.write("\n")
            self.fout.write("#endif // __auxiliary_boundary_lines_LD4_partial_wafer__\n")
            self.fout.close()

        elif self.waferType == "HD":
            fname = "./scripts/include/auxiliary_boundary_lines_HD_full_wafer.h"
            self.fout = open(fname, 'w')
            self.fout.write("#ifndef __auxiliary_boundary_lines_HD_full_wafer__\n")
            self.fout.write("#define __auxiliary_boundary_lines_HD_full_wafer__\n")
            self.fout.write("\n")

            self.fout.write("namespace aux {\n")
            self.fout.write("const int N_HD_boundary_points = 24;\n")
            self.fout.write("\n")
            self.print_coordinate(("x1_HD_full_wafer", "y1_HD_full_wafer"), tc.query_HD_full_wafer_line1, "N_HD_boundary_points")
            self.print_coordinate(("x2_HD_full_wafer", "y2_HD_full_wafer"), tc.query_HD_full_wafer_line2, "N_HD_boundary_points")
            self.print_coordinate(("x3_HD_full_wafer", "y3_HD_full_wafer"), tc.query_HD_full_wafer_line3, "N_HD_boundary_points")
            self.print_coordinate(("x4_HD_full_wafer", "y4_HD_full_wafer"), tc.query_HD_full_wafer_line4, "N_HD_boundary_points")
            self.print_coordinate(("x5_HD_full_wafer", "y5_HD_full_wafer"), tc.query_HD_full_wafer_line5, "N_HD_boundary_points")
            self.print_coordinate(("x6_HD_full_wafer", "y6_HD_full_wafer"), tc.query_HD_full_wafer_line6, "N_HD_boundary_points")
            self.fout.write("}; // end of aux\n")

            self.fout.write("\n")
            self.fout.write("#endif // __auxiliary_boundary_lines_HD_full_wafer__\n")
            self.fout.close()

        print(f"[INFO] {fname} is created!")

if __name__ == "__main__":
    producer = AuxiliaryLineProducer("HD", "data/output_my_coordinate_HD_wafer.json")
    producer.create_cpp_headers()
