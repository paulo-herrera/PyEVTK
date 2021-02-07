#! /usr/bin/env python

######################################################################################
# MIT License
# 
# Copyright (c) 2010-2021 Paulo A. Herrera
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################

# **************************************************************
# * Example of how to create a VTK group to visualize time     *
# * dependent data.                                            *
# **************************************************************
import os
from evtk.vtk import VtkGroup

FILE_PATH = "./group"
def clean():
    try:
        os.remove(FILE_PATH + ".pvd")
    except:
        pass

def run():
    print("Running group...")
    g = VtkGroup(FILE_PATH)
    g.addFile(filepath = "sim0000.vtu", sim_time = 0.0)
    g.addFile(filepath = "sim0001.vtu", sim_time = 1.0)
    g.addFile(filepath = "sim0002.vtu", sim_time = 2.0)
    g.addFile(filepath = "sim0003.vtu", sim_time = 3.0)
    g.save()

if __name__ == "__main__":
	run()
