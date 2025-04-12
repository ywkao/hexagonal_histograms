import json

class ChannelMapper:
    def __init__(self):
        self.output_file_name = "./scripts/include/map_channel_numbers.h"
        self.types = ["MH_B", "MH_F", "MH_L", "MH_R", "MH_T", "ML_5", "ML_B", "ML_F", "ML_L", "ML_R", "ML_T"]
        self.contents = ""

    def create_channel_mapping_header_file(self):
        self._add_head()
        for wafer_type in self.types:
            self._produce_map(wafer_type)
        self._add_end()

    def show_cpp_if_else_statements(self):
        for idx, w in enumerate(self.types):
            if idx==0:
                self.contents =  f'    if (NameTag.Contains("{w}")) {{\n'
                self.contents += f'        map_HGCROC_pin = map_HGCROC_pin_{w};\n'
                self.contents += f'        map_SiCell_pad = map_SiCell_pad_{w};'

            elif idx+1==len(self.types):
                self.contents =  f'    }} else {{\n'
                self.contents += f'        map_HGCROC_pin = map_HGCROC_pin_{w};\n'
                self.contents += f'        map_SiCell_pad = map_SiCell_pad_{w};\n'
                self.contents += f'    }}'

            else:
                self.contents =  f'    }} else if (NameTag.Contains("{w}")) {{\n'
                self.contents += f'        map_HGCROC_pin = map_HGCROC_pin_{w};\n'
                self.contents += f'        map_SiCell_pad = map_SiCell_pad_{w};'

            print(self.contents)

    def _produce_map(self, wafer_type):
        json_file = f"./output/mapping/{wafer_type}_wafer_mapping.json"

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        collection_sicell = "std::map<int, int> map_SiCell_pad_%s = { " % wafer_type
        collection_rocpin = "std::map<int, int> map_HGCROC_pin_%s = { " % wafer_type

        for globalId, value in json_data.items():
            sicell, rocpin = value[0], value[1]

            if(isinstance(rocpin, str)): # "CALIB"
                """ not working in this case """
                print(">>> calib channel found: ", globalId, sicell, rocpin)
                continue

            result_sicell = "{{{0},{1}}},".format(globalId, sicell)
            result_rocpin = "{{{0},{1}}},".format(globalId, rocpin)

            collection_sicell+=result_sicell
            collection_rocpin+=result_rocpin

        collection_sicell+= " };"
        collection_rocpin+= " };"

        self.contents =  collection_sicell + "\n"
        self.contents += collection_rocpin + "\n"
        self.contents += "\n"
        self._write()

    def _add_head(self):
        self.contents =  "#ifndef __map_channel_numbers_h__\n"
        self.contents += "#define __map_channel_numbers_h__\n"
        self.contents += "\n"
        self.contents += "//----------------------------------------------------------------------------------------------------\n"
        self.contents += "// Map information for sicell (pad ID) and HGCROC pin\n"
        self.contents += "// key = globalId, value = pad ID or HGCROC pin (specified on map name)\n"
        self.contents += "// 'CALIB' is replaced with the same pin number as its outer cell\n"
        self.contents += "//----------------------------------------------------------------------------------------------------\n"
        self.contents += "\n"
        self._write(mode='w')

    def _add_end(self):
        self.contents = "#endif // __map_channel_numbers_h__"
        self._write()

    def _write(self, mode='a'):
        with open(self.output_file_name, mode) as fout:
            fout.write(self.contents)

if __name__ == "__main__":
    mapper = ChannelMapper()
    mapper.create_channel_mapping_header_file()
    mapper.show_cpp_if_else_statements()
