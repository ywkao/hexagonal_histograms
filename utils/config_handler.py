#!/usr/bin/env python3
import argparse, logging
import os, yaml
from typing import Tuple, Dict, List, Any

#--------------------------------------------------
# parser and logger
#--------------------------------------------------

def setup_parser():
    """Configure and return the argument parser"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help="number of cells", type=int, default=9999)
    parser.add_argument('-t', '--waferType', help="wafer type code (ML-F, MH-F, etc.)", type=str, default="ML-F")
    parser.add_argument('-d', '--drawLine', help="draw boundary lines", action='store_true')
    parser.add_argument('-v', '--verbose', help="set verbosity level", action='store_true')
    parser.add_argument('--listTypes', help="list available type codes", action='store_true')
    parser.add_argument('--rotation', choices=['0', '30', '150'], default='0', help="Rotation angle in degrees (0, 30, or 150)")
    return parser

def setup_logging(verbose=False, module_name="logger", log_file=None):
    """Configure logging with appropriate level based on verbosity"""
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s-%(name)s-%(levelname)s: %(message)s'

    logging.basicConfig(level=log_level,
                        format=log_format,
                        datefmt='%H:%M:%S')

    logger = logging.getLogger(module_name)

    # Add file handler if log_file is specified and verbosity is enabled
    if log_file and verbose:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter(log_format)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

#--------------------------------------------------
# Wafer config related
#--------------------------------------------------

def load_wafer_config(config_path="./config/wafer_config.yaml") -> Dict:
    """Load wafer configuration from YAML file"""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    return config

def get_type_config(type_code: str) -> Dict[str, Any]:
    """Get configuration for a specific type code"""
    config = load_wafer_config()

    # Start with default parameters
    type_config = config.get('default_params', {}).copy()

    # Update with type-specific parameters (expect either "ML" or "MH"; otherwise use default values in yaml)
    type_specific = config.get('type_specific_params', {}).get(type_code[:2], {})
    type_config.update(type_specific)

    # Generate output paths
    output_paths = {}
    for key, path_template in config.get('output_paths', {}).items():
        output_paths[key] = path_template.format(type_code=type_code.replace('-', '_'))

    type_config['output_paths'] = output_paths

    return type_config

def get_macro_arguments(type_code: str):
    """Get macro arguments for a specific type code"""
    config = get_type_config(type_code)
    return (
        config.get('scope', 14),
        f"{type_code}_wafer".replace('-', '_'),
        config['output_paths']['output_name'],
        config.get('marker_size', 0.7)
    )

def get_exported_file_names(type_code: str):
    """Get file names to export geometry/coordinates/id mapping"""
    config = get_type_config(type_code)
    paths = config['output_paths']
    return (
        paths['geometry_root_file'],
        paths['cell_coordinate_json'],
        paths['cell_id_mapping_json']
    )


if __name__=="__main__":
    data = get_macro_arguments("ML-F")
    mConfig = load_wafer_config(wafer_type="ML-F")
    print(data)
    print(len(mConfig))
