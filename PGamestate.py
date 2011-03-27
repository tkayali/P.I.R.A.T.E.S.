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

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import TextureStage, TransparencyAttrib
from panda3d.core import loadPrcFile, ConfigVariableString
 
loadPrcFile("Config/Config.prc")

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	water = None
	map_grid = None

	def __init__(self):
		ShowBase.__init__(self)
		
		self.taskMgr.add(self.camera_task, "Camera")
		#base.disableMouse()
		#if base.mouseWatcherNode.hasMouse():
  			#print str(base.mouseWatcherNode.getMouseX())
  			#print str(base.mouseWatcherNode.getMouseY())

		#Let's get some water in here!
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(1000)
		self.water.setSy(1000)
		self.water.setPos(0,0,-1)
		ts = TextureStage('ts')
		self.water.setTexture(ts,loader.loadTexture("textures\Water.jpg"))
		self.water.setTexScale(ts,4)
		self.water.reparentTo(self.render)
		#self.water.hide()

		#Sonatu!
		self.sonatu_model = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.sonatu_model.setSx(.02)
		self.sonatu_model.setSy(.02)
		self.sonatu_model.setSz(.02)
		self.sonatu_model.setPos(16*20*sin(pi/3), 13*15, 0)
		self.sonatu_model.lookAt(20*sin(pi/3)*7.5, -15*6.5, 0)
		self.sonatu_model.reparentTo(self.render)
		sonatu = Sonatu(0, 0, 0, self.sonatu_model, 1)

		#Gridspace!
		gridspace_list = []

		###.....................Create Hex Grid.....................###
		y_counter = 0
		hex_radius = 10
		for j in range(6):
			x_counter1 = 0
			x_counter2 = 10*sin(pi/3)
			for i in range(16):
				gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius))
				x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)
			
			y_counter = y_counter - 3/2.0*hex_radius
			for i in range(15):
				gridspace_list.append(Gridspace(None, True, x_counter2, y_counter, hex_radius))
				x_counter2 = x_counter2 + 2*hex_radius*sin(pi/3)
			y_counter = y_counter - 3/2.0*hex_radius
			if j == 5: 
				x_counter1 = 0
				for i in range (16):
					gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius))
					x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)
		###...................End Create Hex Grid....................###
		

		#Add a hex grid texture
		self.map_grid = self.loader.loadModel("square.egg")
		self.map_grid.setTexture(ts, loader.loadTexture("textures\HexGrid.png"))	
		self.map_grid.setPos(20*sin(pi/3)*7.5, -15*6, 1)
		self.map_grid.setSx(16*20*sin(pi/3))
		self.map_grid.setSy(13.5*15)
		self.map_grid.setTransparency(TransparencyAttrib.MAlpha)
		#self.map_grid.lookAt(20*sin(pi/3)*7.5, -15*6.5, 0)
		self.map_grid.reparentTo(self.render)				

	def camera_task(self, task):
		self.camera.setPos(20*sin(pi/3)*7.5, 225, 225)
		self.camera.lookAt(20*sin(pi/3)*7.5, -15*6.5, 0)
		self.camera.setHpr(self.camera, 0, -pi, 0)
		return Task.cont


game = PIRATES()
game.run()
