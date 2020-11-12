#!/bin/env python

from rootpy.io import File
from rootpy.io import root_open
import os.path as path
import glob
from collections import OrderedDict
from ROOT import TFile

data=File("Data.root")
mcfiles=("DYJetsToLL.root", "W+Jets.root", "tbar{t}.root", "VV.root", "SingleTop.root")
#mcfiles.remove("Tau.root")
mcfiles=[File(i) for i in mcfiles]

outputHists=OrderedDict()
dirs=set()
for dirpath, dirnames, filenames in data.walk():
    for filename in filenames:
        print dirpath
        h_data  =   data.Get(path.join(dirpath,filename))
        h_mc=h_data.empty_clone()
        for f in mcfiles:
            h=f.Get(path.join(dirpath,filename))
            h_mc+=h
        h_data-=h_mc
        outputHists[dirpath,filename]=h_data
        dirs.add(dirpath)
output_file = root_open("nicolas_lowMETandLS_QCDresult_102120.root", "NEW")
for d in dirs:
    output_file.cd()
    output_file.mkdir(d)

for dirpath,filename in outputHists:
    output_file.cd()
    output_file.cd(dirpath)
    outputHists[dirpath,filename].Write()
output_file.Close()
    





