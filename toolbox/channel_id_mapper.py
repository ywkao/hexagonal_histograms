#!/usr/bin/env python2
import json

json_file = "./data/output_my_chId_mapping_partial_wafer.json"

with open(json_file, 'r') as f:
	data = f.read()
	json_data = json.loads(data)

def get_coordinate(ch):
	sicell = json_data[ch][0]
	rocpin = json_data[ch][1]
	return x, y

if __name__ == "__main__":
    collection_sicell, collection_rocpin = "std::map<int, int> map_SiCell_padId_partial_wafer = { ", "std::map<int, int> map_HGCROC_pin_partial_wafer = { "
    for globalId, value in json_data.items():
        sicell, rocpin = value[0], value[1]
        
        if(isinstance(rocpin, str)): # "CALIB"
            """ not working in this case """
            print ">>> calib channel found: ", globalId, sicell, rocpin
            continue

        result_sicell = "{{{0},{1}}},".format(globalId, sicell)
        result_rocpin = "{{{0},{1}}},".format(globalId, rocpin)

        collection_sicell+=result_sicell
        collection_rocpin+=result_rocpin

    collection_sicell+= " };"
    collection_rocpin+= " };"
    
    print collection_sicell
    print collection_rocpin
