# hexagonal_histograms

## Environment

On lxplus,
```
source /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.34.04/x86_64-almalinux9.5-gcc115-opt/bin/thisroot.sh
```

## Commands
```
$ git clone -b dev git@github.com:ywkao/hexagonal_histograms.git
$ cd hexagonal_histograms
$ make
$ ./exe.py -w full -d -v # LD full wafer
$ ./exe.py -w LD3 -d -v # LD3 partial wafer
$ ./exe.py -w LD4 -d -v # LD4 partial wafer
$ ./exe.py -w HD -d -v # HD full wafer
```

## Description of main scripts
| File                         | Description                                                           |
| ---------------------------- | --------------------------------------------------------------------- |
| `exe.py`                     | Top-level script steering workflow with the following options:<br> -w, --waferType [full\|LD3\|LD4\|HD] # set wafer type<br> -d, --drawLine # draw boundary lines<br> -v, --verbose # set verbosity level |
| `toolbox/polygon_manager.py` | Methods for generating polygonal bins & producing geometry root files |
| `toolbox/geometry.py`        | Parameters of polygons                                                |
| `th2poly.C`                  | Macro drawing wafer maps from a geometry root file                    |

## Workflow in the code
- Build a c++ shared library which contains a function to convert HGCAL (u, v) to (x, y)
- Import c++ class using PyRoot gInterpreter and gSystem
- Load cell information from `data/WaferCellMapTrg.txt`
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
