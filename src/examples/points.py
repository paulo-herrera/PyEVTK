#! /usr/bin/env python

# ***********************************************************************************
# * Copyright 2010 - 2019 Paulo A. Herrera. All rights reserved.                    * 
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

from evtk.hl import pointsToVTK, pointsToVTKAsTIN
import numpy as np

# Example 1: Random point set
npoints = 100
x = np.random.rand(npoints)
y = np.random.rand(npoints)
z = np.random.rand(npoints)
pressure = np.random.rand(npoints)
temp = np.random.rand(npoints)
comments = [ "comment 1", "comment 2" ]

# keys are sorted before exporting, hence it is useful to prefix a number to determine an order
pointsToVTK("./rnd_points", x, y, z, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments) 

# Example 2: Export as TIN
ndim = 2 #only consider x, y coordinates to create the triangulation
pointsToVTKAsTIN("./rnd_points_TIN", x, y, z, ndim = ndim, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments)

# Example 3: Regular point set
x = np.arange(1.0,10.0,0.1)
y = np.arange(1.0,10.0,0.1)
z = np.arange(1.0,10.0,0.1)

comments = [ "comment 1", "comment 2" ]
pointsToVTK("./line_points", x, y, z, data = {"elev" : z}, comments = comments)

# Example 4: Point set of 5 points
x = [0.0, 1.0, 0.5, 0.368, 0.4]
y = [0.3, 2.0, 0.7, 0.1, 0.6]
z = [1.0, 1.0, 0.3, 0.75, 0.9]
pressure = [1.0, 2.0, 3.0, 4.0, 5.0]
temp = [1.0, 2.0, 3.0, 4.0, 5.0]
comments = [ "comment 1", "comment 2" ]

# keys are sorted before exporting, hence it is useful to prefix a number to determine an order
pointsToVTK("./points_as_lists", x, y, z, data = {"1_temp" : temp, "2_pressure" : pressure}, comments = comments) 

