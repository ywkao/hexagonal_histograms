# hexagonal_histograms

The package provides commands to generate geometry root files for the HGCAL DQM wafer maps.
Each root file contains a collection of polygons/cells/silicon pads as TGraph objects, created using PyROOT.

For each cell, the center position (x, y) is derived using HGCAL DPG tool, `src/HGCalCell.cc`.
This C++ class is invoked from Python using `ROOT.gInterpreter` in `utils/polygon_manager.py`, as shown below:

```python
ROOT.gInterpreter.ProcessLine('#include "include/HGCalCell.h"')
ROOT.gSystem.Load("./build/libHGCalCell.so")
cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)
```

The default cell shape is hexagonal.
Other polygonal shapes are assigned via the `_get_polygon_information()` method in `utils/polygon_manager.py`,
which uses the `irregular_polygonal_cells` dictionary defined in `utils/geometry.py`.

⚠️  To run the package, ensure that your Python version is compatible with the one used to build ROOT.
To avoid building ROOT from scratch and potential compatible issues, we recommend using the pre-built CVMFS ROOT from LCG releases.

## Environment

On lxplus, set up the environment as follows:

1. Load ROOT
Run the following command to source the ROOT environment:
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.34.04/x86_64-almalinux9.5-gcc115-opt/bin/thisroot.sh
```

2. Set up Python environment (first time only)
Create a virtual environment for Python dependencies:
```
python3 -m venv pandas_env
source pandas_env/bin/activate
pip install pandas
pip install pyyaml
```

3. Routine session (after first setup)
For regular use, activate the environments as follows:
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.34.04/x86_64-almalinux9.5-gcc115-opt/bin/thisroot.sh
source pandas_env/bin/activate
```

To deactivate the virtual environment when finished:
```
deactivate # deactivate the environment when finished
```

## Setup
Clone the repository and build the project:
```
$ git clone -b dev git@github.com:ywkao/hexagonal_histograms.git
$ cd hexagonal_histograms
$ make
```

## Usage
List available wafer types
```
$ ./exe.py --list-types # List all available wafer types
```

Generate outputs for specific wafer types (with verbose logging)
```
$ ./exe.py -t ML-F -v
$ ./exe.py -t MH-F -v
$ ./exe.py -t ML-T -v
$ ./exe.py -t ML-B -v
$ ./exe.py -t ML-L -v
$ ./exe.py -t ML-R -v
$ ./exe.py -t ML-5 -v
$ ./exe.py -t MH-T -v
$ ./exe.py -t MH-B -v
$ ./exe.py -t MH-L -v
$ ./exe.py -t MH-R -v
```

Output directories
- `output/geometry/`: Root geometry files
- `output/waferMaps/`: Wafer map visualizations
- `output/coordinates/`: JSON files with cell coordinates
- `output/mapping/`: JSON files with cell ID mappings

Verbose option `-v` includes:
- cell name (e.g., `hex`, `hex_nc`, `hex_cm`)
- cell IDs (Global ID / ROC Pin / SiCell)
- cell area in mm^2

Produce {global_channel_id: sicell/rocpin} maps
```
$ python3 utils/channel_id_mapper.py

# Expected output:
#   ./scripts/include/map_channel_numbers.h
#   ./output/mapping_csv/{wafer_type}_globalId_vs_sicell.csv
```

Demonstration of how to `TH2Poly` with a geometry ROOT file
```
$ root -l -b -q scripts/tutorial_th2poly.C

# Expected output:
#   ./output/waferMaps/tutorial.png
```

## Description of main scripts
| File                             | Description                                                                                                                                                                    |
| ----------------------------     | ---------------------------------------------------------------------                                                                                                          |
| `exe.py`                         | Top-level script steering workflow with the following options:<br> `-t`, `--waferType` [ML-F|MH-F|ML-L|...] to set wafer type<br> `-v`, `--verbose` to enable verbose logging  |
| `utils/polygon_manager.py`       | Contains a class that provides methods to generate polygonal bins & export geometry root files                                                                                 |
| `utils/geometry.py`              | - Defines all basic polygonal shapes in HGCAL silicon wafers<br>- Implements channel mapping between SiCell ID and irregular polygons                                          |
| `utils/config_handler.py`        | - Sets up argument parser and logger.<br>- Provides methods to wrap config parameters from `config/wafer_config.yaml`.                                                         |
| `config/wafer_config.yaml`       | Defines parameters to use for low-density and high-density modules, as well as output string templates.                                                                        |
| `scripts/generate_wafer_maps.C`  | ROOT macro for drawing wafer maps from a generated geometry root file                                                                                                          |

## Processing flow in the code
- Build a c++ shared library that converts HGCAL (u, v) cell indices to (x, y) positions.
- Import c++ class using PyRoot `gInterpreter` and `gSystem`.
- Load cell information from `data/input/WaferCellMapTraces.txt`.
- Generate polygonal bins as `TGraph` object.
- Output a geometry root file containing the graphs.
- Use `TH2Poly` in a ROOT macro to create a hexagonal histogram.

## Steps for DQM GUI display (not in this repository)
- Main idea: txt file -> TGraphs -> TH2Poly -> DQM GUI Display
- Require TH2Poly implemented in DQM EDAnalyzer (PR#41932 on CMSSW has merged)
- Load the geometry root file in DQM EDAnalyzer
- Fill entries & produce plots

## References
- https://root.cern/manual/python/
- https://root.cern/doc/master/th2polyEurope_8C.html
- https://github.com/cms-sw/cmssw/blob/master/Geometry/HGCalCommonData/src/HGCalCell.cc

## Examples
| ML-F | ML-L | ML-R |
| --- | --- | --- |
| ![ML-F](examples/ML_F_wafer_example.png) |![ML-L](examples/ML_L_wafer_example.png) | ![ML-R](examples/ML_R_wafer_example.png) |
| ML-5 | ML-T | ML-B |
|![ML-5](examples/ML_5_wafer_example.png) |![ML-T](examples/ML_T_wafer_example.png) |![ML-B](examples/ML_B_wafer_example.png) |
| MH-F | MH-L | MH-R |
| ![MH-F](examples/MH_F_wafer_example.png) | ![MH-L](examples/MH_L_wafer_example.png) | ![MH-R](examples/MH_R_wafer_example.png) |
| MH-T | MH-B | |
| ![MH-T](examples/MH_T_wafer_example.png) | ![MH-B](examples/MH_B_wafer_example.png) | |
