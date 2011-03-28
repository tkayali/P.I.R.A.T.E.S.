#This is the gamestate .py file
#Here goes all the config variables that Tarif will fill in later

#First we need the config variables. We'll ignore these for now.

#Second we need all the import statements for our lovely classes to work.
from PUnit import Unit
from PEnemy import Enemy
from PQueen import Queen
from PSonatu import Sonatu
from PCombatUI import CombatUI
from PGridspace import Gridspace
#from PLimbo import Limbo

from math import pi, sin, cos
import random, sys, os

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import TextureStage, TransparencyAttrib
from pandac.PandaModules import *
from panda3d.core import loadPrcFile, ConfigVariableString
 
loadPrcFile("Config/Config.prc")

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()		

		self.limbo()
		self.combat_collision_detection()
		self.mouseTask = taskMgr.add(self.combat_mouse_task, 'combat_mouse_task')
		
		self.accept("escape", sys.exit)
		self.accept("h", self.limbo_hide_all )
		self.accept("c", self.combat )
		self.accept("l", self.combat_hide_all )

		
	def limbo(self):
		#Set up the Limbo Sonatu
		self.limbo_sonatu = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.limbo_sonatu.setPos(0, 0, 0)
		self.limbo_sonatu.setHpr(-90, 0, 0)
		self.limbo_sonatu.reparentTo(self.render)
		
		#Set up the camera for the Limbo Menu
		self.taskMgr.add(self.limbo_camera_task, "Limbo Camera")

	def combat(self):
		#Combat water
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(1000)
		self.water.setSy(1000)
		self.water.setPos(0,0,-1)
		ts = TextureStage('ts')
		self.water.setTexture(ts,loader.loadTexture("textures\Water.jpg"))
		self.water.setTexScale(ts,4)
		self.water.reparentTo(self.render)

		#Combat Sonatu
		self.combat_sonatu = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.combat_sonatu.setSx(.025)
		self.combat_sonatu.setSy(.025)
		self.combat_sonatu.setSz(.025)
		self.combat_sonatu.setPos(0, 0, 1)
		self.combat_sonatu.lookAt(-1000, 0, 0)
		self.combat_sonatu.reparentTo(self.render)
		sonatu = Sonatu(0, 0, 0, self.combat_sonatu, 2)

		#Create the hex grid
		self.gridspace_list = []
		y_counter = 0
		hex_radius = 10
		for j in range(6):
			x_counter1 = 0
			x_counter2 = 10*sin(pi/3)
			for i in range(16):
				self.gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius, j*i+i))
				x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)
			
			y_counter = y_counter - 3/2.0*hex_radius
			for i in range(15):
				self.gridspace_list.append(Gridspace(None, True, x_counter2, y_counter, hex_radius, j*i+i+16))
				x_counter2 = x_counter2 + 2*hex_radius*sin(pi/3)
			y_counter = y_counter - 3/2.0*hex_radius
			if j == 5: 
				x_counter1 = 0
				for i in range (16):
					self.gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius, (j+1)*i+i))
					x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)		

		#Add a hex grid texture
		self.map_grid = self.loader.loadModel("square.egg")
		self.map_grid.setTexture(ts, loader.loadTexture("textures\HexGrid.png"))	
		self.map_grid.setPos(20*sin(pi/3)*7.5, -15*6, 1)
		self.map_grid.setSx(16*20*sin(pi/3))
		self.map_grid.setSy(13.5*15)
		self.map_grid.setTransparency(TransparencyAttrib.MAlpha)
		self.map_grid.reparentTo(self.render)				

		#Set up camera for combat
		self.taskMgr.add(self.combat_camera_task, "Combat Camera")
	
	def limbo_hide_all(self):
		self.limbo_sonatu.hide()
	
	def combat_hide_all(self):
		self.map_grid.hide()
		self.water.hide()
		self.combat_sonatu.hide()

	def combat_mouse_task(self, task):
		if base.mouseWatcherNode.hasMouse():
			self.accept("mouse1", self.move_sonatu )
		return Task.cont

	def PointAtZ(self, z, point, vec):
		print point + vec * ((z-point.getZ()) / vec.getZ())
  		return point + vec * ((z-point.getZ()) / vec.getZ())
	
	def move_sonatu(self):
		if base.mouseWatcherNode.hasMouse():
			self.mouse_position = base.mouseWatcherNode.getMouse()
			self.collision_ray.setFromLens(base.camNode, self.mouse_position.getX(), self.mouse_position.getY())
			self.near_point = render.getRelativePoint(self.camera, self.collision_ray.getOrigin())
			self.near_vector = render.getRelativeVector(self.camera, self.collision_ray.getDirection())
			self.traverser.traverse(render)
			if self.handler.getNumEntries() > 0:
				self.handler.sortEntries()
				hex = self.handler.getEntry(0).getIntoNodePath()
				hex = hex.findNetTag("hex");
				self.combat_sonatu.setPos( hex.get_x_position, hex.get_y_position, 1)

			#relative_point = self.PointAtZ(.5, self.near_point, self.near_vector)
			#self.combat_sonatu.setPos(relative_point)

	def combat_camera_task(self, task):
		self.camera.setPos(20*sin(pi/3)*7.5, 225, 225)
		self.camera.lookAt(20*sin(pi/3)*7.5, -15*6.5, 0)
		self.camera.setHpr(self.camera, 0, -pi, 0)
		return Task.cont

	def limbo_camera_task(self, task):
		self.camera.setPos(-71.832, -170.0494, -14.609)
		self.camera.setHpr(32.399, 0.875, -0.152)
		return Task.cont

	def combat_collision_detection(self):
		self.traverser = CollisionTraverser()
		self.handler = CollisionHandlerQueue()
		self.collision_node = CollisionNode( "mouse_ray")
		self.collision_camera = self.camera.attachNewNode(self.collision_node)
		self.collision_node.setFromCollideMask(BitMask32.bit(1))
		self.collision_ray = CollisionRay()
		self.collision_node.addSolid(self.collision_ray)
		self.traverser.addCollider(self.collision_camera, self.handler)
		#self.traverser.showCollisions(render)

game = PIRATES()
game.run()
