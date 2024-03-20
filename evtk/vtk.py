######################################################################################
# MIT License
# 
# Copyright (c) 2010-2024 Paulo A. Herrera
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
# *  Low level Python library to       *
# *  export data to binary VTK file.   *
# **************************************

from .evtk import writeBlockSize, writeArrayToFile, writeArraysToFile
from .xml import XmlWriter
import sys
import os

# ================================
#            VTK Types
# ================================

#     FILE TYPES
class VtkFileType:

    def __init__(self, name, ext):
        self.name = name
        self.ext  = ext

    def __str__(self):
        return "Name: %s  Ext: %s \n" % (self.name, self.ext)

VtkImageData        = VtkFileType("ImageData", ".vti")
VtkPolyData         = VtkFileType("PolyData", ".vtp")
VtkRectilinearGrid  = VtkFileType("RectilinearGrid", ".vtr")
VtkStructuredGrid   = VtkFileType("StructuredGrid", ".vts")
VtkUnstructuredGrid = VtkFileType("UnstructuredGrid", ".vtu")

#    DATA TYPES
class VtkDataType:

    def __init__(self, size, name):
        self.size = size
        self.name = name

    def __str__(self):
        return "Type: %s  Size: %d \n" % (self.name, self.size)

VtkInt8    = VtkDataType(1, "Int8")
VtkUInt8   = VtkDataType(1, "UInt8")
VtkInt16   = VtkDataType(2, "Int16")
VtkUInt16  = VtkDataType(2, "UInt16")
VtkInt32   = VtkDataType(4, "Int32")
VtkUInt32  = VtkDataType(4, "UInt32")
VtkInt64   = VtkDataType(8, "Int64")
VtkUInt64  = VtkDataType(8, "UInt64")
VtkFloat32 = VtkDataType(4, "Float32")
VtkFloat64 = VtkDataType(8, "Float64")

# Map numpy to VTK data types
np_to_vtk = { 'int8'    : VtkInt8,
              'uint8'   : VtkUInt8,
              'int16'   : VtkInt16,
              'uint16'  : VtkUInt16,
              'int32'   : VtkInt32,
              'uint32'  : VtkUInt32,
              'int64'   : VtkInt64,
              'uint64'  : VtkUInt64,
              'float32' : VtkFloat32,
              'float64' : VtkFloat64 }

#    CELL TYPES
class VtkCellType:

    def __init__(self, tid, name):
        self.tid = tid
        self.name = name

    def __str__(self):
        return "VtkCellType( %s ) \n" % ( self.name )

VtkVertex = VtkCellType(1, "Vertex")
VtkPolyVertex = VtkCellType(2, "PolyVertex")
VtkLine = VtkCellType(3, "Line")
VtkPolyLine = VtkCellType(4, "PolyLine")
VtkTriangle = VtkCellType(5, "Triangle")
VtkTriangleStrip = VtkCellType(6, "TriangleStrip")
VtkPolygon = VtkCellType(7, "Polygon")
VtkPixel = VtkCellType(8, "Pixel")
VtkQuad = VtkCellType(9, "Quad")
VtkTetra = VtkCellType(10, "Tetra")
VtkVoxel = VtkCellType(11, "Voxel")
VtkHexahedron = VtkCellType(12, "Hexahedron")
VtkWedge = VtkCellType(13, "Wedge")
VtkPyramid = VtkCellType(14, "Pyramid")
VtkQuadraticEdge = VtkCellType(21, "Quadratic_Edge")
VtkQuadraticTriangle = VtkCellType(22, "Quadratic_Triangle")
VtkQuadraticQuad = VtkCellType(23, "Quadratic_Quad")
VtkQuadraticTetra = VtkCellType(24, "Quadratic_Tetra")
VtkQuadraticHexahedron = VtkCellType(25, "Quadratic_Hexahedron")

# ==============================
#       Helper functions
# ==============================
def _mix_extents(start, end):
    assert (len(start) == len(end) == 3)
    string = "%d %d %d %d %d %d" % (start[0], end[0], start[1], end[1], start[2], end[2])
    return string

def _array_to_string(a):
    s = "".join([repr(num) + " " for num in a])
    return s

def _get_byte_order():
    if sys.byteorder == "little":
        return "LittleEndian"
    else:
        return "BigEndian"

# ================================
#        VtkGroup class
# ================================
class VtkGroup:
    
    def __init__(self, filepath):
        """ Creates a VtkGroup file that is stored in filepath.
            
            PARAMETERS:
                filepath: filename without extension.
        """
        self.xml = XmlWriter(filepath + ".pvd")
        self.xml.openElement("VTKFile")
        self.xml.addAttributes(type = "Collection", version = "0.1",  byte_order = _get_byte_order())
        self.xml.openElement("Collection")
        self.root = os.path.dirname(filepath)

    def save(self):
        """ Closes this VtkGroup. """
        self.xml.closeElement("Collection")
        self.xml.closeElement("VTKFile")
        self.xml.close()
    
    def addFile(self, filepath, sim_time, group = "", part = "0"):
        """ Adds file to this VTK group.

            PARAMETERS:
                filepath: full path to VTK file.
                sim_time: simulated time.
                group: This attribute is not required; it is only for informational purposes.
                part: It is an integer value greater than or equal to 0.
                
            See: http://www.paraview.org/Wiki/ParaView/Data_formats#PVD_File_Format for details.
        """
        # TODO: Check what the other attributes are for.
        filename = os.path.relpath(filepath, start = self.root)
        self.xml.openElement("DataSet")
        self.xml.addAttributes(timestep = sim_time, group = group, part = part, file = filename)
        self.xml.closeElement()
        


# ================================
#        VtkFile class         
# ================================
class VtkFile:
    
    def __init__(self, filepath, ftype, largeFile = False):
        """
            PARAMETERS:
                filepath: filename without extension.
                ftype: file type, e.g. VtkImageData, etc.
                largeFile: If size of the stored data cannot be represented by a UInt32.
        """
        self.ftype = ftype
        self.filename = filepath + ftype.ext
        self.xml = XmlWriter(self.filename)
        self.offset = 0  # offset in bytes after beginning of binary section
        self.appendedDataIsOpen = False
#        self.largeFile = largeFile

#       if largeFile == False:
#            self.xml.openElement("VTKFile").addAttributes(type = ftype.name,
#                                                          version = "0.1",
#                                                          byte_order = _get_byte_order())
#        else:
#           print "WARNING: output file only compatible with VTK 6.0 and later."
        self.xml.openElement("VTKFile").addAttributes(type = ftype.name,
                                                          version = "1.0",
                                                          byte_order = _get_byte_order(),
                                                          header_type = "UInt64")

    def addComments(self, comments):
        """ Insert strings stored in comments list as comments into the xml header section of the file. 
            This method does not make any check for forbidden or special characters in XML comments. 
            This method should be called right after creating the file to avoid including comments in the 
            wrong place within the header. BE AWARE!!!
        """
        assert not self.appendedDataIsOpen
        for c in comments:
            self.xml.addComment(c)
        
    def getFileName(self):
        """ Returns absolute path to this file. """
        return  os.path.abspath(self.filename)

    def openPiece(self, start = None, end = None,
                        npoints = None, ncells = None,
                        nverts = None, nlines = None, nstrips = None, npolys = None): 
        """ Open piece section.
            
            PARAMETERS:
                Next two parameters must be given together.
                start: array or list with start indexes in each direction.
                end:   array or list with end indexes in each direction.

                npoints: number of points in piece (int).
                ncells: number of cells in piece (int). If present,
                        npoints must also be given.

                All the following parameters must be given together with npoints.
                They should all be integer values.
                nverts: number of vertices.
                nlines: number of lines.
                nstrips: number of strips.
                npolys: number of .

            RETURNS:
                this VtkFile to allow chained calls.
        """
        # TODO: Check what are the requirements for each type of grid.

        self.xml.openElement("Piece")
        if (start and end):
            ext = _mix_extents(start, end)
            self.xml.addAttributes( Extent = ext)
        
        elif (ncells and npoints):
            self.xml.addAttributes(NumberOfPoints = npoints, NumberOfCells = ncells)
       
        elif npoints or nverts or nlines or nstrips or npolys:
            if npoints is None: npoints = str(0)
            if nverts is None: nverts = str(0)
            if nlines is None: nlines = str(0)
            if nstrips is None: nstrips = str(0)
            if npolys is None: npolys = str(0)
            self.xml.addAttributes(NumberOfPoints = npoints, NumberOfVerts = nverts,
                                   NumberOfLines = nlines, NumberOfStrips = nstrips, NumberOfPolys = npolys)
        else:
            assert(False)

        return self

    def closePiece(self):
        self.xml.closeElement("Piece")

    def openData(self, nodeType, scalars=None, vectors=None, normals=None, tensors=None, tcoords=None):
        """ Open data section.

            PARAMETERS:
                nodeType: Point or Cell.
                scalars: default data array name for scalar data.
                vectors: default data array name for vector data.
                normals: default data array name for normals data.
                tensors: default data array name for tensors data.
                tcoords: dafault data array name for tcoords data.

            RETURNS:
                this VtkFile to allow chained calls.
        """
        self.xml.openElement(nodeType + "Data")
        if scalars:
            self.xml.addAttributes(scalars = scalars)
        if vectors:
            self.xml.addAttributes(vectors = vectors)
        if normals:
            self.xml.addAttributes(normals = normals)
        if tensors:
            self.xml.addAttributes(tensors = tensors)
        if tcoords:
            self.xml.addAttributes(tcoords = tcoords)

        return self

    def closeData(self, nodeType):
        """ Close data section.

            PARAMETERS:
                nodeType: Point or Cell.
 
            RETURNS:
                this VtkFile to allow chained calls.
        """
        self.xml.closeElement(nodeType + "Data")


    def openGrid(self, start = None, end = None, origin = None, spacing = None):
        """ Open grid section.

            PARAMETERS:
                start: array or list of start indexes. Required for Structured, Rectilinear and ImageData grids.
                end: array or list of end indexes. Required for Structured, Rectilinear and ImageData grids.
                origin: 3D array or list with grid origin. Only required for ImageData grids.
                spacing: 3D array or list with grid spacing. Only required for ImageData grids.

            RETURNS:
                this VtkFile to allow chained calls.
        """
        gType = self.ftype.name
        self.xml.openElement(gType)
        if (gType == VtkImageData.name):
            if (not start or not end or not origin or not spacing): assert(False)
            ext = _mix_extents(start, end)
            self.xml.addAttributes(WholeExtent = ext,
                                   Origin = _array_to_string(origin),
                                   Spacing = _array_to_string(spacing))
        
        elif (gType == VtkStructuredGrid.name or gType == VtkRectilinearGrid.name):
            if (not start or not end): assert (False)
            ext = _mix_extents(start, end)
            self.xml.addAttributes(WholeExtent = ext) 
                
        return self

    def closeGrid(self):
        """ Closes grid element.

            RETURNS:
                this VtkFile to allow chained calls.
        """
        self.xml.closeElement(self.ftype.name)

    
    def addHeader(self, name, dtype, nelem, ncomp):
        """ Adds data array description to xml header section.

            PARAMETERS:
                name: data array name.
                dtype: string describing type of the data.
                       Format is the same as used by numpy, e.g. 'float64'.
                nelem: number of elements in the array.
                ncomp: number of components, 1 (=scalar) and 3 (=vector).

            RETURNS:
                This VtkFile to allow chained calls.
            
            NOTE: This is a low level function. Use addData if you want
                  to add a numpy array.
        """
        dtype = np_to_vtk[dtype]

        self.xml.openElement( "DataArray")
        self.xml.addAttributes( Name = name,
                                NumberOfComponents = ncomp,
                                type = dtype.name,
                                format = "appended",
                                offset = self.offset)
        self.xml.closeElement()

        #TODO: Check if 4/8 is platform independent
        #if self.largeFile == False:
        #    self.offset += nelem * ncomp * dtype.size + 4 # add 4 to indicate array size
        #else:
        self.offset += nelem * ncomp * dtype.size + 8 # add 8 to indicate array size
        return self

    def addData(self, name, data):
        """ Adds array description to xml header section.
            
             PARAMETERS:
                name: data array name.
                data: one numpy array or a tuple with 3 numpy arrays. If a tuple, the individual
                      arrays must represent the components of a vector field.
                      All arrays must be one dimensional or three-dimensional.
        """
        if type(data).__name__ == "tuple": # vector data
            assert (len(data) == 3)
            x = data[0]
            self.addHeader(name, x.dtype.name, x.size, 3)
        elif type(data).__name__ == "ndarray":
            if data.ndim == 1 or data.ndim == 3:
                self.addHeader(name, data.dtype.name, data.size, 1)
            else:
                assert False, "Bad array shape: " + str(data.shape)
        else:
            assert False, "Argument must be a Numpy array"

    def appendHeader(self, dtype, nelem, ncomp):
        """ This function only writes the size of the data block that will be appended.
            The data itself must be written immediately after calling this function.
            
            PARAMETERS:
                dtype: string with data type representation (same as numpy). For example, 'float64'
                nelem: number of elements.
                ncomp: number of components, 1 (=scalar) or 3 (=vector).
        """
        self.openAppendedData()
        dsize = np_to_vtk[dtype].size
        block_size = dsize * ncomp * nelem
        if self.largeFile == False:
            writeBlockSize(self.xml.stream, block_size)
        else:
            writeBlockSize64Bit(self.xml.stream, block_size)

            
    def appendData(self, data):
        """ Append data to binary section.
            This function writes the header section and the data to the binary file.

            PARAMETERS:
                data: one numpy array or a tuple with 3 numpy arrays. If a tuple, the individual
                      arrays must represent the components of a vector field.
                      All arrays must be one dimensional or three-dimensional.
                      The order of the arrays must coincide with the numbering scheme of the grid.
            
            RETURNS:
                This VtkFile to allow chained calls

            TODO: Extend this function to accept contiguous C order arrays.
        """
        self.openAppendedData()

        if type(data).__name__ == 'tuple': # 3 numpy arrays
            ncomp = len(data)
            assert (ncomp == 3)
            dsize = data[0].dtype.itemsize
            nelem = data[0].size
            block_size = ncomp * nelem * dsize
            #if self.largeFile == False:
            writeBlockSize(self.xml.stream, block_size)
            #else:
            #    writeBlockSize64Bit(self.xml.stream, block_size)
            x, y, z = data[0], data[1], data[2]
            writeArraysToFile(self.xml.stream, x, y, z)
            
        elif type(data).__name__ == 'ndarray' and (data.ndim == 1 or data.ndim == 3): # single numpy array
            ncomp = 1 
            dsize = data.dtype.itemsize
            nelem = data.size
            block_size = ncomp * nelem * dsize
            #if self.largeFile == False:
            writeBlockSize(self.xml.stream, block_size)
            #else:
            #    writeBlockSize64Bit(self.xml.stream, block_size)
            writeArrayToFile(self.xml.stream, data)
         
        else:
            assert False

        return self

    def openAppendedData(self):
        """ Opens binary section.

            It is not necessary to explicitly call this function from an external library.
        """
        if not self.appendedDataIsOpen:
            self.xml.openElement("AppendedData").addAttributes(encoding = "raw").addText("_")
            self.appendedDataIsOpen = True

    def closeAppendedData(self):
        """ Closes binary section.

            It is not necessary to explicitly call this function from an external library.
        """
        self.xml.closeElement("AppendedData")

    def openElement(self, tagName):
        """ Useful to add elements such as: Coordinates, Points, Verts, etc. """
        self.xml.openElement(tagName)

    def closeElement(self, tagName):
        self.xml.closeElement(tagName)

    def save(self):
        """ Closes file """
        if self.appendedDataIsOpen:
            self.xml.closeElement("AppendedData")
        self.xml.closeElement("VTKFile")
        self.xml.close()
    
