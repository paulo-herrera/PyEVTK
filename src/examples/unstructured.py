#! /usr/bin/env python

# ***********************************************************************************
# * Copyright 2010 - 2017 Paulo A. Herrera. All rights reserved.                    * 
# *                                                                                 *
# * Redistribution and use in source and binary forms, with or without              *
# * modification, are permitted provided that the following conditions are met:     *
# *                                                                                 *
# *  1. Redistributions of source code must retain the above copyright notice,      *
# *  this list of conditions and the following disclaimer.                          *
# *                                                                                 *
# *  2. Redistributions in binary form must reproduce the above copyright notice,   *
# *  this list of conditions and the following disclaimer in the documentation      *
# *  and/or other materials provided with the distribution.                         *
# *                                                                                 *
# * THIS SOFTWARE IS PROVIDED BY PAULO A. HERRERA ``AS IS'' AND ANY EXPRESS OR      *
# * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF    *
# * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO      *
# * EVENT SHALL <COPYRIGHT HOLDER> OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,        *
# * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,  *
# * BUT NOT LIMITED TO, PROCUREMEN OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,    *
# * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY           *
# * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING  *
# * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS              *
# * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                    *
# ***********************************************************************************

# ************************************************************************
# * Example of how to use the high level unstructuredGridToVTK function. *
# * This example shows how to export a unstructured grid give its        *
# * nodes and topology through a connectivity and offset lists.          *
# * Check the VTK file format for details of the unstructured grid.      *
# ************************************************************************

from evtk.hl import unstructuredGridToVTK
from evtk.vtk import VtkTriangle, VtkQuad
import numpy as np

# Define vertices
x = np.zeros(6)
y = np.zeros(6)
z = np.zeros(6)

x[0], y[0], z[0] = 0.0, 0.0, 0.0
x[1], y[1], z[1] = 1.0, 0.0, 0.0
x[2], y[2], z[2] = 2.0, 0.0, 0.0
x[3], y[3], z[3] = 0.0, 1.0, 0.0
x[4], y[4], z[4] = 1.0, 1.0, 0.0
x[5], y[5], z[5] = 2.0, 1.0, 0.0

# Define connectivity or vertices that belongs to each element
conn = np.zeros(10)

conn[0], conn[1], conn[2] = 0, 1, 3              # first triangle
conn[3], conn[4], conn[5] = 1, 4, 3              # second triangle
conn[6], conn[7], conn[8], conn[9] = 1, 2, 5, 4  # rectangle

# Define offset of last vertex of each element
offset = np.zeros(3)
offset[0] = 3
offset[1] = 6
offset[2] = 10

# Define cell types

ctype = np.zeros(3)
ctype[0], ctype[1] = VtkTriangle.tid, VtkTriangle.tid
ctype[2] = VtkQuad.tid
 
unstructuredGridToVTK("unstructured", x, y, z, connectivity = conn, offsets = offset, cell_types = ctype, cellData = None, pointData = None)
