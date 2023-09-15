#!/usr/bin/env python2
"""
Recipe:
1. :!./exe.py -w "HD" -v > log.txt
2. :!./toolbox/obtain_alternative_rocpin_for_calib.py
"""

import subprocess
type_hollow = [29, 150, 157, 36, 387, 411, 297, 267, 261, 87, 207, 381] # cells around a calib channel

def exe(command):
    subprocess.call(command, shell=True)

class Manager():
    def __init__(self):
        self.output = "record.txt"
        self.collection = {}

    def extract_information_calib_hollow(self):
        """
        In ./toolbox/polygon_manager.py ,
        def __str__(self):
            # channel ID info
            return "{0} {1} {2} {3}".format(self.globalId, self.rocpin, self.sicell, (self.iu,self.iv))
        """
        with open(self.output, 'w') as fout: fout.write("# extracted info for modify calib rocpin\n")
        for ele in type_hollow:
            key = "sicell = %d," % ele
            command = 'grep \"%s\" log.txt >> %s' % (key, self.output)
            exe(command)
        exe('grep CALIB log.txt >> %s' % self.output)
    
    def load_info(self):
        with open(self.output, 'r') as f: contents = f.readlines()
        for line in contents:
            if '#' in line: continue
            info = line.split(', ')
            globalId = info[0].split(' = ')[1]
            rocpin = info[1].split(' = ')[1]
            sicell = info[2].split(' = ')[1]
            u = info[3].split('(')[1]
            v = info[4].split(')')[0]

            self.collection[globalId] = globalId, rocpin, sicell, u, v
            print self.collection[globalId]


if __name__ == "__main__":
    m = Manager()
    m.extract_information_calib_hollow()
    m.load_info()

    """
    Remaining tasks:
    1. search "CALIB" (cell-A)
    2. get u v
    3. find another entry with the same u v (cell-B)
    4. obtain rocpin of that entry
    5. return a pair of global ID (cell-A) and rocpin (cell-B)
    """
