# hexagonal_histograms

The package is used to generate geometry root files for the HGCAL DQM wafer maps.

We use PyROOT to create a collection of polygons/cells/silicon pads as TGraph objects in geometry root file.
For each cell, the center position (x, y) is derived using HGCAL DPG tool, `src/HGCalCell.cc`.
The C++ class is used in Python script through `ROOT.gInterpreter` in `utils/polygon_manager.py`, as shown the following lines:

```
ROOT.gInterpreter.ProcessLine('#include "include/HGCalCell.h"')
ROOT.gSystem.Load("./build/libHGCalCell.so")
cell_helper = ROOT.HGCalCell(waferSize, nFine, nCoarse)
```

Therefore, to run the package, we need to ensure that the Python version is compatible with the one used to build ROOT.
To avoid building ROOT from scratch and potential compatible issues, we recommend using the pre-built CVMFS ROOT from LCG releases.

## Environment

On lxplus,
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.34.04/x86_64-almalinux9.5-gcc115-opt/bin/thisroot.sh
```

Create env to use pandas module (only for the first time)
```
python3 -m venv pandas_env
source pandas_env/bin/activate
pip install pandas
pip install pyyaml
```

Routine environment setting
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.34.04/x86_64-almalinux9.5-gcc115-opt/bin/thisroot.sh
source pandas_env/bin/activate
deactivate # deactivate the environment when finished
```

## Commands
```
$ git clone -b dev git@github.com:ywkao/hexagonal_histograms.git
$ cd hexagonal_histograms
$ make
$ ./exe.py --list-types # List all available wafer types
$ ./exe.py -t ML-L
$ ./exe.py -t ML-R
$ ./exe.py -t ML-T
$ ./exe.py -t ML-B
$ ./exe.py -t ML-5

# Output files will be created in:
# - output/geometry/: Root geometry files
# - output/waferMaps/: Wafer map visualizations
# - output/coordinates/: JSON files with cell coordinates
# - output/mapping/: JSON files with cell ID mappings
```

## Description of main scripts
| File                         | Description                                                           |
| ---------------------------- | --------------------------------------------------------------------- |
| `exe.py`                     | Top-level script steering workflow with the following options:<br> -w, --waferType [full\|LD3\|LD4\|HD] # set wafer type<br> -d, --drawLine # draw boundary lines<br> -v, --verbose # set verbosity level |
| `utils/polygon_manager.py`   | Methods for generating polygonal bins & producing geometry root files |
| `utils/geometry.py`          | Parameters of polygons                                                |
| `th2poly.C`                  | Macro drawing wafer maps from a geometry root file                    |

## Workflow in the code
- Build a c++ shared library which contains a function to convert HGCAL (u, v) to (x, y)
- Import c++ class using PyRoot gInterpreter and gSystem
- Load cell information from `data/input/WaferCellMapTrg.txt`
- Generate polygonal bins in TGraph
- Produce a geometry root file with a collection of graphs
- Make a hexagonal histogram using TH2Poly in a ROOT macro

## Steps for DQM GUI display (not in this repository)
- Main idea: txt file -> TGraphs -> TH2Poly -> DQM GUI Display
- Require TH2Poly implemented in DQM EDAnalyzer
- Load the geometry root file in DQM EDAnalyzer
- Fill entries & produce plots

## Reference
- https://root.cern/manual/python/
- https://root.cern/doc/master/th2polyEurope_8C.html
- https://github.com/cms-sw/cmssw/blob/master/Geometry/HGCalCommonData/src/HGCalCell.cc
