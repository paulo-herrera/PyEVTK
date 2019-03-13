#! /usr/bin/env python

# ***********************************************************************************
# * Copyright 2010 - 2016 Paulo A. Herrera. All rights reserved.                    * 
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

# **************************************************************
# * Example of how to use the high level pointsToVTK function. *
# **************************************************************

from evtk.hl import polyLinesToVTK
import numpy as np

# Positions of points that define lines
npoints = 7
x = np.zeros(npoints)
y = np.zeros(npoints)
z = np.zeros(npoints)

# First line
x[0], y[0], z[0] = 0.0, 0.0, 0.0
x[1], y[1], z[1] = 1.0, 1.0, 0.0
x[2], y[2], z[2] = 2.0, 0.0, 0.0
x[3], y[3], z[3] = 3.0, -1.0, 0.0

# Second line
x[4], y[4], z[4] = 0.0, 0.0, 3.0
x[5], y[5], z[5] = 1.0, 1.0, 3.0
x[6], y[6], z[6] = 2.0, 0.0, 3.0

# Connectivity of the lines
pointsPerLine = np.zeros(2)
pointsPerLine[0] = 4
pointsPerLine[1] = 3

# Some variables
pressure = np.random.rand(npoints)
temp = np.random.rand(npoints)
vel = np.zeros(6)
vel[0:3] = 1.0
vel[4:6] = 5.0

polyLinesToVTK("./poly_lines", x, y, z, pointsPerLine = pointsPerLine, cellData = {"vel" : vel}, pointData = {"temp" : temp, "pressure" : pressure})


