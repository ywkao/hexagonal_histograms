#!/usr/bin/env python2
import yaml
import os
from typing import Tuple, Dict, List

def load_wafer_config(config_path="./config/wafer_config.yaml"):
    """ Load wafer type configuration from YAML file """
    if not os.path.exists(config_path):
        raise FileNotFoundError("Configuration file not found:", config_path)
        
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config['wafer_types']

def get_macro_arguments(wafer_type):
    """ Get macro arguments for a specific wafer type """
    config = load_wafer_config()
    
    if wafer_type not in config:
        raise ValueError("Unknown wafer type:", wafer_type)
    
    params = config[wafer_type]
    return params['scope'], params['tag'], params['output_name'], params['marker_size']

def load_wafer_contents(wafer_type, file_path="./data/WaferCellMapTrg.txt"):
    """ Load contents from text file based on wafer type indices """
    config = load_wafer_config()
    
    if wafer_type not in config:
        raise ValueError("Unknown wafer type:", wafer_type)
    
    params = config[wafer_type]
    begin_idx, end_idx = params['begin_idx'], params['end_idx']
    
    with open(file_path, 'r') as fin:
        contents = fin.readlines()[begin_idx:end_idx]
    
    return contents

if __name__=="__main__":
    data = get_macro_arguments("HD")
    contents = load_wafer_contents(wafer_type="HD")
    print(data)
    print(len(contents))
