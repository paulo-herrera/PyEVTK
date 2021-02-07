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

# **************************************
# *  High level Python library to      *
# *  export data to binary VTK file.   *
# **************************************

from .vtk import * # VtkFile, VtkUnstructuredGrid, etc.
try:
    import numpy as np
except:
    print("Numpy is not installed. Please install it before running EVTK again.")

# =================================
#       Helper functions
# =================================
def _addDataToFile(vtkFile, cellData, pointData):
    # Point data
    if pointData:
        keys = sorted(list(pointData.keys()))
        vtkFile.openData("Point", scalars = keys[0])
        for key in keys:
            data = pointData[key]
            vtkFile.addData(key, data)
        vtkFile.closeData("Point")

    # Cell data
    if cellData:
        keys = sorted(list(cellData.keys()))
        vtkFile.openData("Cell", scalars = keys[0])
        for key in keys:
            data = cellData[key]
            vtkFile.addData(key, data)
        vtkFile.closeData("Cell")

def _appendDataToFile(vtkFile, cellData, pointData):
    # Append data to binary section
    if pointData != None:
        keys = sorted(list(pointData.keys()))
        for key in keys:
            data = pointData[key]
            vtkFile.appendData(data)

    if cellData != None:
        keys = sorted(list(cellData.keys()))
        for key in keys:
            data = cellData[key]
            vtkFile.appendData(data)

def __convertListToArray(list1d):
    ''' If data is a list and no a Numpy array, then it convert it
        to an array, otherwise return the same array '''
    if (list1d is not None) and (not type(list1d).__name__ == "ndarray"):
        assert isinstance(list1d, (list, tuple))
        return np.array(list1d)
    else:
        return list1d

def __convertDictListToArrays(data):
    ''' If data in dictironary are lists and no a Numpy array,
        then it creates a new dictionary and convert the list to arrays,
        otherwise return the same dictionary '''
    if data is not None:
        dict = {}
        for k, list1d in data.items():
            dict[k] = __convertListToArray(list1d)
        return dict
    else:
        return data # None
        
# =================================
#       High level functions      
# =================================
def imageToVTK(path, origin = (0.0,0.0,0.0), spacing = (1.0,1.0,1.0), cellData = None, pointData = None, comments = None ):
    """ Exports data values as a rectangular image.
        
        PARAMETERS:
            path: name of the file without extension where data should be saved.
            origin: grid origin (default = (0,0,0))
            spacing: grid spacing (default = (1,1,1))
            cellData: dictionary containing arrays with cell centered data.
                      Keys should be the names of the data arrays.
                      Arrays must have the same dimensions in all directions and must contain 
                      only scalar data.
            nodeData: dictionary containing arrays with node centered data.
                      Keys should be the names of the data arrays.
                      Arrays must have same dimension in each direction and 
                      they should be equal to the dimensions of the cell data plus one and
                      must contain only scalar data.
            comments: list of comment strings, which will be added to the header section of the file.
         
         RETURNS:
            Full path to saved file.

        NOTE: At least, cellData or pointData must be present to infer the dimensions of the image.
    """
    assert (cellData != None or pointData != None)
    
    # Extract dimensions
    start = (0,0,0)
    end = None
    if cellData != None:
        keys = list(cellData.keys())
        data = cellData[keys[0]]
        end = data.shape
    elif pointData != None:
        keys = list(pointData.keys())
        data = pointData[keys[0]]
        end = data.shape
        end = (end[0] - 1, end[1] - 1, end[2] - 1)

    # Write data to file
    w = VtkFile(path, VtkImageData)
    if comments: w.addComments(comments)
    w.openGrid(start = start, end = end, origin = origin, spacing = spacing)
    w.openPiece(start = start, end = end)
    _addDataToFile(w, cellData, pointData)
    w.closePiece()
    w.closeGrid()
    _appendDataToFile(w, cellData, pointData)
    w.save()
    return w.getFileName()

# ==============================================================================
def rectilinearToVTK(path, x, y, z, cellData = None, pointData = None, comments = None):
    """
        Writes data values as a rectilinear or rectangular grid.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: coordinates of the nodes of the grid as 1D arrays.
                     The grid should be Cartesian, i.e. faces in all cells are orthogonal.
                     Arrays size should be equal to the number of nodes of the grid in each direction.
            cellData: dictionary containing arrays with cell centered data.
                      Keys should be the names of the data arrays.
                      Arrays must have the same dimensions in all directions and must contain 
                      only scalar data.
            pointData: dictionary containing arrays with node centered data.
                       Keys should be the names of the data arrays.
                       Arrays must have same dimension in each direction and 
                       they should be equal to the dimensions of the cell data plus one and
                       must contain only scalar data.
            comments: list of comment strings, which will be added to the header section of the file.
            
        RETURNS:
            Full path to saved file.

    """
    assert (x.ndim == 1 and y.ndim == 1 and z.ndim == 1), "Wrong array dimension"
    ftype = VtkRectilinearGrid
    nx, ny, nz = x.size - 1, y.size - 1, z.size - 1
    # Extract dimensions
    start = (0,0,0)
    end   = (nx, ny, nz)
    
    w =  VtkFile(path, ftype)
    if comments: w.addComments(comments)
    w.openGrid(start = start, end = end)
    w.openPiece(start = start, end = end)

    w.openElement("Coordinates")
    w.addData("x_coordinates", x)
    w.addData("y_coordinates", y)
    w.addData("z_coordinates", z)
    w.closeElement("Coordinates")

    _addDataToFile(w, cellData, pointData)
    w.closePiece()
    w.closeGrid()
    # Write coordinates
    w.appendData(x).appendData(y).appendData(z)
    # Write data
    _appendDataToFile(w, cellData, pointData)
    w.save()
    return w.getFileName()
    

def structuredToVTK(path, x, y, z, cellData = None, pointData = None, comments = None):
    """
        Writes data values as a rectilinear or rectangular grid.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: coordinates of the nodes of the grid as 3D arrays.
                     The grid should be structured, i.e. all cells should have the same number of neighbors.
                     Arrays size in each dimension should be equal to the number of nodes of the grid in each direction.
            cellData: dictionary containing arrays with cell centered data.
                      Keys should be the names of the data arrays.
                      Arrays must have the same dimensions in all directions and must contain 
                      only scalar data.
            pointData: dictionary containing arrays with node centered data.
                       Keys should be the names of the data arrays.
                       Arrays must have same dimension in each direction and 
                       they should be equal to the dimensions of the cell data plus one and
                       must contain only scalar data.
            comments: list of comment strings, which will be added to the header section of the file.
            
        RETURNS:
            Full path to saved file.

    """
    assert (x.ndim == 3 and y.ndim == 3 and z.ndim == 3), "Wrong arrays dimensions"
    
    ftype = VtkStructuredGrid
    s = x.shape
    nx, ny, nz = s[0] - 1, s[1] - 1, s[2] - 1
    start = (0,0,0)
    end = (nx, ny, nz)
 
    w =  VtkFile(path, ftype)
    if comments: w.addComments(comments)
    w.openGrid(start = start, end = end)
    w.openPiece(start = start, end = end)
    w.openElement("Points")
    w.addData("points", (x,y,z))
    w.closeElement("Points")

    _addDataToFile(w, cellData, pointData)
    w.closePiece()
    w.closeGrid()
    w.appendData( (x,y,z) )
    _appendDataToFile(w, cellData, pointData)
    w.save()
    return w.getFileName()
    
# def gridToVTK(path, x, y, z, cellData = None, pointData = None, comments = None):
    # """
        # Writes data values as a rectilinear or rectangular grid.

        # PARAMETERS:
            # path: name of the file without extension where data should be saved.
            # x, y, z: coordinates of the nodes of the grid. They can be 1D or 3D depending if
                     # the grid should be saved as a rectilinear or logically structured grid, respectively.
                     # Arrays should contain coordinates of the nodes of the grid.
                     # If arrays are 1D, then the grid should be Cartesian, i.e. faces in all cells are orthogonal.
                     # If arrays are 3D, then the grid should be logically structured with hexahedral cells.
                     # In both cases the arrays dimensions should be equal to the number of nodes of the grid.
            # cellData: dictionary containing arrays with cell centered data.
                      # Keys should be the names of the data arrays.
                      # Arrays must have the same dimensions in all directions and must contain 
                      # only scalar data.
            # pointData: dictionary containing arrays with node centered data.
                       # Keys should be the names of the data arrays.
                       # Arrays must have same dimension in each direction and 
                       # they should be equal to the dimensions of the cell data plus one and
                       # must contain only scalar data.
            # comments: list of comment strings, which will be added to the header section of the file.
            
        # RETURNS:
            # Full path to saved file.

    # """
    # # Extract dimensions
    # start = (0,0,0)
    # nx = ny = nz = 0

    # if (x.ndim == 1 and y.ndim == 1 and z.ndim == 1):
        # nx, ny, nz = x.size - 1, y.size - 1, z.size - 1
        # isRect = True
        # ftype = VtkRectilinearGrid
    # elif (x.ndim == 3 and y.ndim == 3 and z.ndim == 3):
        # s = x.shape
        # nx, ny, nz = s[0] - 1, s[1] - 1, s[2] - 1
        # isRect = False
        # ftype = VtkStructuredGrid
    # else:
        # assert(False)
    # end = (nx, ny, nz)


    # w =  VtkFile(path, ftype)
    # if comments: w.addComments(comments)
    # w.openGrid(start = start, end = end)
    # w.openPiece(start = start, end = end)

    # if isRect:
        # w.openElement("Coordinates")
        # w.addData("x_coordinates", x)
        # w.addData("y_coordinates", y)
        # w.addData("z_coordinates", z)
        # w.closeElement("Coordinates")
    # else:
        # w.openElement("Points")
        # w.addData("points", (x,y,z))
        # w.closeElement("Points")

    # _addDataToFile(w, cellData, pointData)
    # w.closePiece()
    # w.closeGrid()
    # # Write coordinates
    # if isRect:
        # w.appendData(x).appendData(y).appendData(z)
    # else:
        # w.appendData( (x,y,z) )
    # # Write data
    # _appendDataToFile(w, cellData, pointData)
    # w.save()
    # return w.getFileName()


# ==============================================================================
def pointsToVTK(path, x, y, z, data = None, comments = None ):
    """
        Export points and associated data as an unstructured grid.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D list-type object (list, tuple or numpy) with coordinates of the points.
            data: dictionary with variables associated to each point.
                  Keys should be the names of the variable stored in each array.
                  All 1D list-type object (list, tuple or numpy) must have the same number of elements.
            comments: list of comment strings, which will be added to the header section of the file.
            
        RETURNS:
            Full path to saved file.

    """
    assert (len(x) == len(y) == len(z) )
    x = __convertListToArray(x)
    y = __convertListToArray(y)
    z = __convertListToArray(z)
    data = __convertDictListToArrays(data)
    
    npoints = len(x)
    
    # create some temporary arrays to write grid topology
    offsets = np.arange(start = 1, stop = npoints + 1, dtype = 'int32')   # index of last node in each cell
    connectivity = np.arange(npoints, dtype = 'int32')                    # each point is only connected to itself
    cell_types = np.empty(npoints, dtype = 'uint8') 
   
    cell_types[:] = VtkVertex.tid

    w = VtkFile(path, VtkUnstructuredGrid)
    if comments: w.addComments(comments)
    w.openGrid()
    w.openPiece(ncells = npoints, npoints = npoints)
    
    w.openElement("Points")
    w.addData("points", (x,y,z))
    w.closeElement("Points")
    w.openElement("Cells")
    w.addData("connectivity", connectivity)
    w.addData("offsets", offsets)
    w.addData("types", cell_types)
    w.closeElement("Cells")
    
    _addDataToFile(w, cellData = None, pointData = data)

    w.closePiece()
    w.closeGrid()
    w.appendData( (x,y,z) )
    w.appendData(connectivity).appendData(offsets).appendData(cell_types)

    _appendDataToFile(w, cellData = None, pointData = data)

    w.save()
    return w.getFileName()
    
# ==============================================================================
def pointsToVTKAsTIN(path, x, y, z, data = None, comments = None, ndim = 2):
    """
        Export points and associated data as a triangula irregular grid.
        It builds a triangular grid that has the input points as nodes
        using the Delaunay triangulation function in Scipy, which requires
        a convex set of points (check the documentation for further details
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html).

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D list-type object (list, tuple or numpy) with coordinates of the points.
            data: dictionary with variables associated to each point.
                  Keys should be the names of the variable stored in each array.
                  All 1D list-type object (list, tuple or numpy) must have the same number of elements.
            comments: list of comment strings, which will be added to the header section of the file.
            ndim: is the number of dimensions considered when calling Delaunay.
                  If ndim = 2, then only coordinates x and y are passed.
                  If ndim = 3, then x, y and z coordinates are passed.
            
        RETURNS:
            Full path to saved file.
        
        REQUIRES: Scipy > 1.2.
    """
    # TODO: Check if it makes and it would be possible to add cellData.
    try:
    	from scipy.spatial import Delaunay
    except:
        print("Failed to import scipy.spatial. Please install it if it is not installed.")

    assert len(x) == len(y) and len(x) == len(z)
    assert (ndim == 2) or (ndim == 3)
    x = __convertListToArray(x)
    y = __convertListToArray(y)
    z = __convertListToArray(z)
    data = __convertDictListToArrays(data)
    
    npts = len(x)
    
    points = np.zeros( (npts, ndim) ) # needs to create the 2D or 3D temporary array to call Delaunay
    for i in range(npts):
        points[i,0] = x[i]
        points[i,1] = y[i]
        if ndim > 2: points[i,2] = z[i]
        
    tri = Delaunay(points)
        
    # list of triangles that form the tesselation
    ncells, npoints_per_cell = tri.simplices.shape[0], tri.simplices.shape[1]
    conn =  np.zeros(ncells * 3)
    for i in range(ncells):
        ii = i * 3
        conn[ii]     = tri.simplices[i,0]
        conn[ii + 1] = tri.simplices[i,1]
        conn[ii + 2] = tri.simplices[i,2]
        
    offset = np.zeros(ncells)
    for i in range(ncells): offset[i] = (i + 1) * 3
        
    cell_type = np.ones(ncells) * VtkTriangle.tid
    unstructuredGridToVTK(path, x, y, z, connectivity = conn, offsets = offset, cell_types = cell_type, cellData = None, pointData = {"Elevation" : z}, comments = None)
        
# ==============================================================================
def linesToVTK(path, x, y, z, cellData = None, pointData = None, comments = None ):
    """
        Export line segments that joint 2 points and associated data.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D list-type object (list, tuple or numpy) with coordinates of the vertex of the lines. It is assumed that each line.
                     is defined by two points, then the lenght of the arrays should be equal to 2 * number of lines.
            cellData: dictionary with variables associated to each line.
                  Keys should be the names of the variable stored in each array.
                  All 1D list-type object (list, tuple or numpy) must have the same number of elements.         
            pointData: dictionary with variables associated to each vertex.
                  Keys should be the names of the variable stored in each array.
                  All 1D list-type object (list, tuple or numpy) must have the same number of elements.
            comments: list of comment strings, which will be added to the header section of the file.
                  
        RETURNS:
            Full path to saved file.

    """
    assert (x.size == y.size == z.size)
    assert (x.size % 2 == 0)
    
    x = __convertListToArray(x)
    y = __convertListToArray(y)
    z = __convertListToArray(z)
    cellData = __convertDictListToArrays(cellData)
    pointData = __convertDictListToArrays(pointData)
    
    npoints = len(x)
    ncells = int(len(x) / 2.0)
    
    # Check cellData has the same size that the number of cells
    
    # create some temporary arrays to write grid topology
    offsets = np.arange(start = 2, step = 2, stop = npoints + 1, dtype = 'int32')   # index of last node in each cell
    connectivity = np.arange(npoints, dtype = 'int32')                              # each point is only connected to itself
    cell_types = np.empty(npoints, dtype = 'uint8') 
   
    cell_types[:] = VtkLine.tid

    w = VtkFile(path, VtkUnstructuredGrid)
    if comments: w.addComments(comments)
    w.openGrid()
    w.openPiece(ncells = ncells, npoints = npoints)
    
    w.openElement("Points")
    w.addData("points", (x,y,z))
    w.closeElement("Points")
    w.openElement("Cells")
    w.addData("connectivity", connectivity)
    w.addData("offsets", offsets)
    w.addData("types", cell_types)
    w.closeElement("Cells")
    
    _addDataToFile(w, cellData = cellData, pointData = pointData)

    w.closePiece()
    w.closeGrid()
    w.appendData( (x,y,z) )
    w.appendData(connectivity).appendData(offsets).appendData(cell_types)

    _appendDataToFile(w, cellData = cellData, pointData = pointData)

    w.save()
    return w.getFileName()

# ==============================================================================
def polyLinesToVTK(path, x, y, z, pointsPerLine, cellData = None, pointData = None, comments = None ):
    """
        Export line segments that joint 2 points and associated data.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D list-type object (list, tuple or numpy) arrays with coordinates of the vertices of the lines. It is assumed that each line.
                     has diffent number of points.
            pointsPerLine: 1D list-type object (list, tuple or numpy) array that defines the number of points associated to each line. Thus, 
                           the length of this array define the number of lines. It also implicitly 
                           defines the connectivity or topology of the set of lines. It is assumed 
                           that points that define a line are consecutive in the x, y and z arrays.
            cellData: Dictionary with variables associated to each line.
                      Keys should be the names of the variable stored in each array.
                      All 1D list-type object (list, tuple or numpy) must have the same number of elements.         
            pointData: Dictionary with variables associated to each vertex.
                       Keys should be the names of the variable stored in each array.
                       1D list-type object (list, tuple or numpy) must have the same number of elements.
            comments: list of comment strings, which will be added to the header section of the file.
            
        RETURNS:
            Full path to saved file.

    """
    assert (x.size == y.size == z.size)
    
    x = __convertListToArray(x)
    y = __convertListToArray(y)
    z = __convertListToArray(z)
    cellData = __convertDictListToArrays(cellData)
    pointData = __convertDictListToArrays(pointData)
    
    npoints = len(x)
    ncells = pointsPerLine.size
    
    # create some temporary arrays to write grid topology
    offsets = np.zeros(ncells, dtype = 'int32')         # index of last node in each cell
    ii = 0
    for i in range(ncells):
        ii += pointsPerLine[i]
        offsets[i] = ii
    
    connectivity = np.arange(npoints, dtype = 'int32')      # each line connects points that are consecutive
   
    cell_types = np.empty(npoints, dtype = 'uint8') 
    cell_types[:] = VtkPolyLine.tid

    w = VtkFile(path, VtkUnstructuredGrid)
    if comments: w.addComments(comments)
    w.openGrid()
    w.openPiece(ncells = ncells, npoints = npoints)
    
    w.openElement("Points")
    w.addData("points", (x,y,z))
    w.closeElement("Points")
    w.openElement("Cells")
    w.addData("connectivity", connectivity)
    w.addData("offsets", offsets)
    w.addData("types", cell_types)
    w.closeElement("Cells")
    
    _addDataToFile(w, cellData = cellData, pointData = pointData)

    w.closePiece()
    w.closeGrid()
    w.appendData( (x,y,z) )
    w.appendData(connectivity).appendData(offsets).appendData(cell_types)

    _appendDataToFile(w, cellData = cellData, pointData = pointData)

    w.save()
    return w.getFileName()

# ==============================================================================
def unstructuredGridToVTK(path, x, y, z, connectivity, offsets, cell_types, cellData = None, pointData = None, comments = None ):
    """
        Export unstructured grid and associated data.

        PARAMETERS:
            path: name of the file without extension where data should be saved.
            x, y, z: 1D list-type object (list, tuple or numpy) with coordinates of the vertices of cells. It is assumed that each element
                     has diffent number of vertices.
            connectivity: 1D list-type object (list, tuple or numpy) that defines the vertices associated to each element. 
                          Together with offset define the connectivity or topology of the grid. 
                          It is assumed that vertices in an element are listed consecutively.
            offsets: 1D list-type object (list, tuple or numpy) with the index of the last vertex of each element in the connectivity array.
                     It should have length nelem, where nelem is the number of cells or elements in the grid.
            cell_types: 1D list-type object (list, tuple or numpy) with an integer that defines the cell type of each element in the grid.
                        It should have size nelem. This should be assigned from evtk.vtk.VtkXXXX.tid, where XXXX represent
                        the type of cell. Please check the VTK file format specification for allowed cell types.                       
            cellData: Dictionary with variables associated to each line.
                      Keys should be the names of the variable stored in each array.
                      All 1D list-type object (list, tuple or numpy) must have the same number of elements.        
            pointData: Dictionary with variables associated to each vertex.
                       Keys should be the names of the variable stored in each array.
                       All 1D list-type object (list, tuple or numpy) must have the same number of elements.
            comments: list of comment strings, which will be added to the header section of the file.
            
        RETURNS:
            Full path to saved file.

    """
    assert (x.size == y.size == z.size)
    x = __convertListToArray(x)
    y = __convertListToArray(y)
    z = __convertListToArray(z)
    connectivity = __convertListToArray(connectivity)
    offsets = __convertListToArray(offsets)
    cell_types = __convertListToArray(cell_types)
    cellData = __convertDictListToArrays(cellData)
    pointData = __convertDictListToArrays(pointData)
    
    npoints = x.size
    ncells = cell_types.size
    assert (offsets.size == ncells)
    
    w = VtkFile(path, VtkUnstructuredGrid)
    if comments: w.addComments(comments)
    w.openGrid()
    w.openPiece(ncells = ncells, npoints = npoints)
    
    w.openElement("Points")
    w.addData("points", (x,y,z))
    w.closeElement("Points")
    w.openElement("Cells")
    w.addData("connectivity", connectivity)
    w.addData("offsets", offsets)
    w.addData("types", cell_types)
    w.closeElement("Cells")
    
    _addDataToFile(w, cellData = cellData, pointData = pointData)

    w.closePiece()
    w.closeGrid()
    w.appendData( (x,y,z) )
    w.appendData(connectivity).appendData(offsets).appendData(cell_types)

    _appendDataToFile(w, cellData = cellData, pointData = pointData)

    w.save()
    return w.getFileName()
    
# ==============================================================================
def cylinderToVTK(path, x0, y0, z0, z1, radius, nlayers, npilars = 16, cellData=None, pointData=None, comments = None ):
    """
        Export cylinder as VTK unstructured grid.
    
      PARAMETERS:
        path: path to file without extension.
        x0, yo: center of cylinder.
        z0, z1: lower and top elevation of the cylinder.
        radius: radius of cylinder.
        nlayers: Number of layers in z direction to divide the cylinder.
        npilars: Number of points around the diameter of the cylinder. 
                 Higher value gives higher resolution to represent the curved shape.
        cellData: dictionary with 1D arrays that store cell data. 
                  Arrays should have number of elements equal to ncells = npilars * nlayers.
        pointData: dictionary with 1D arrays that store point data.
                  Arrays should have number of elements equal to npoints = npilars * (nlayers + 1).
        comments: list of comment strings, which will be added to the header section of the file.
                    
      RETURNS: 
            Full path to saved file.
        
        NOTE: This function only export vertical shapes for now. However, it should be easy to 
              rotate the cylinder to represent other orientations.
    """
    import math as m
    
    # Define x, y coordinates from polar coordinates.
    dpi = 2.0 * m.pi / npilars
    angles = np.arange(0.0, 2.0 * m.pi, dpi)

    x = radius * np.cos(angles) + x0
    y = radius * np.sin(angles) + y0

    dz = (z1 - z0) / nlayers
    z = np.arange(z0, z1+dz, step = dz)

    npoints = npilars * (nlayers + 1)
    ncells  = npilars * nlayers

    xx = np.zeros(npoints)
    yy = np.zeros(npoints)
    zz = np.zeros(npoints)

    ii = 0
    for k in range(nlayers + 1):
        for p in range(npilars):
            xx[ii] = x[p]
            yy[ii] = y[p]
            zz[ii] = z[k]
            ii = ii + 1

    # Define connectivity
    conn = np.zeros(4 * ncells, dtype = np.int64)
    ii = 0
    for l in range(nlayers):
        for p in range(npilars):
            p0 = p
            if(p + 1 == npilars):
                p1 = 0 
            else: 
                p1 = p + 1 # circular loop
       
            n0 = p0 + l * npilars
            n1 = p1 + l * npilars 
            n2 = n0 + npilars
            n3 = n1 + npilars
        
            conn[ii + 0] = n0
            conn[ii + 1] = n1
            conn[ii + 2] = n3
            conn[ii + 3] = n2 
            ii = ii + 4
 
    # Define offsets 
    offsets = np.zeros(ncells, dtype = np.int64)
    for i in range(ncells):
        offsets[i] = (i + 1) * 4

    # Define cell types
    ctype = np.ones(ncells) + VtkPixel.tid
    
    return unstructuredGridToVTK(path, xx, yy, zz, connectivity = conn, offsets = offsets, cell_types = ctype, cellData = cellData, pointData = pointData, comments = comments)
