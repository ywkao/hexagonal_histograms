#!/usr/bin/env python3
import yaml
import os
from typing import Tuple, Dict, List, Any

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

    # Update with type-specific parameters
    type_specific = config.get('type_specific_params', {}).get(type_code, {})
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
        config.get('tag', f"{type_code}_wafer"),
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
