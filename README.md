# hexagonal_histograms

## commands
```
$ git clone git@github.com:ywkao/hexagonal_histograms.git
$ cd hexagonal_histograms
$ make && ./exe.py
```

## Workflow in the code
- Build a c++ shared library which contains a function to convert HGCAL (u, v) to (x, y)
- Import c++ class using PyRoot gInterpreter and gSystem
- Load geometry data
- Plot hexagons using TGraph
- Produce a geometry root file with a collection of graphs
- Make a hexagonal histogram using TH2Poly in a ROOT macro

## Steps for DQM GUI display (not in this repository)
- Main idea: txt file -> TGraphs -> TH2Poly -> DQM GUI Display
- Need to implement TH2Poly in DQM EDAnalyzer
- Load the geometry root file in DQM EDAnalyzer
- Fill entries & produce plots

## Reference
https://root.cern/manual/python/
https://root.cern/doc/master/th2polyEurope_8C.html
https://github.com/cms-sw/cmssw/blob/master/Geometry/HGCalCommonData/src/HGCalCell.cc
