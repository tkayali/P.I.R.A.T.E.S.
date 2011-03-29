from panda3d.core import GeomVertexWriter, GeomVertexData, GeomVertexFormat, GeomPrimitive, Geom, GeomNode, GeomVertexArrayFormat, InternalName, GeomLines, GeomPoints, GeomTristrips, GeomLinestrips, GeomTrifans
from pandac.PandaModules import *

from math import cos, sin, pi

class Gridspace:
    """
    This class contains information about an individual gridspace
    """
    __occupying_unit = None
    __occupiable = None
    __x = 0
    __z = 0
    __r = 0
    __tag = 0
    __vdata = None
    __vertex = None
    __normal = None
    __hex_primitive = None
    __hex_geometry = None
    __hex_node = None
    
    def __init__(self, __occupying_unit = None, __occupiable = True, 
	x = 0, z = 0, r = 5, tag = 0):
        self.__occupying_unit = __occupying_unit
        self.__occupiable = __occupiable
	self.__r = r
	self.__x = x
	self.__z = z
	self.__tag = tag
	
	#Procedurally creating a hex!
	geometry_array = GeomVertexArrayFormat()
	geometry_array.addColumn(InternalName.make('vertex'), 3, Geom.NTFloat32, Geom.CPoint)
	geometry_array.addColumn(InternalName.make('normal'), 3, Geom.NTFloat32, Geom.CPoint)
	format = GeomVertexFormat()
	format.addArray(geometry_array)
	format = GeomVertexFormat.registerFormat(format)
	self.__vdata = GeomVertexData('Hex', format, Geom.UHStatic)
	self.__vertex = GeomVertexWriter(self.__vdata, 'vertex')
	self.__normal = GeomVertexWriter(self.__vdata, 'normal')

	#Vertex 1
	self.__vertex.addData3f(self.__x, self.__z+self.__r, 0)
	self.__normal.addData3f(1, 0, 0)
	#Vertex 2
	self.__vertex.addData3f(self.__x+self.__r*sin(pi/3), self.__z+self.__r*cos(pi/3), 0)
	self.__normal.addData3f(1, 0, 0)
	#Vertex 3
	self.__vertex.addData3f(self.__x+self.__r*sin(pi/3), self.__z-self.__r*cos(pi/3), 0)
	self.__normal.addData3f(1, 0, 0)
	#Vertex 4
	self.__vertex.addData3f(self.__x, self.__z-self.__r, 0)
	self.__normal.addData3f(1, 0, 0)
	#Vertex 5
	self.__vertex.addData3f(self.__x-self.__r*sin(pi/3), self.__z-self.__r*cos(pi/3), 0)
	self.__normal.addData3f(1, 0, 0)
	#Vertex 6
	self.__vertex.addData3f(self.__x-self.__r*sin(pi/3), self.__z+self.__r*cos(pi/3), 0)
	self.__normal.addData3f(1, 0, 0)

	self.__hex_primitive = GeomTrifans(Geom.UHStatic)
	self.__hex_primitive.addVertices(5, 4)
	self.__hex_primitive.addVertices(3, 2)
	self.__hex_primitive.addVertices(1, 0)

	self.__hex_primitive.closePrimitive()
	self.__hex_geometry = Geom(self.__vdata)
	self.__hex_geometry.addPrimitive(self.__hex_primitive)
	self.__hex_node = GeomNode('HexNode')
	self.__hex_node.addGeom(self.__hex_geometry)

	nodePath = render.attachNewNode(self.__hex_node)
	nodePath.setTag( "hex", str(tag) )
	nodePath.node().setIntoCollideMask(BitMask32.bit(1))
    
    def get_x_position(self):
	return self.__x

    def get_y_position(self):
	return self.__z
	
    def get_occupying_unit(self):
        return self.__occupying_unit
    
    def set_occupying_unit(self, __occupying_unit):
        self.__occupying_unit = __occupying_unit
        
    def get_occupiable(self):
        return self.__occupiable
    
    def set_occupiable(self, __occupiable):
        self.__occupiable = __occupiable
