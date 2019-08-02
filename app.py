#!/usr/bin/env python3

import h5py
import numpy

with open("52_Ta_18_Ar1100_1.dp_rpc_asc") as data_file:
    for line in data_file:
        # Check for Sample ID
        if(line):
            # dataObject.sampleID = line[]
            print(line)
        # Check for Date
        elif(line):
            # dataObject.sampleDate = line[]
            print(line)
        # Do this for every line 
        else:
            break

