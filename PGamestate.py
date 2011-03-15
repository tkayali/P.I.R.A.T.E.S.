#This is the gamestate .py file
#Here goes all the config variables that Tarif will fill in later

#First we need the config variables. We'll ignore these for now.

#Second we need all the import statements for our lovely classes to work.
from PUnit import Unit
from PEnemy import Enemy
from PQueen import Queen
from PSonatu import Sonatu
from PCombatUI import CombatUI

from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from pandac.PandaModules import TextureStage

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	water = None

	def __init__(self):
		ShowBase.__init__(self)
		self.environ = self.loader.loadModel("/c/Panda3D-1.7.0/models/environment")
		self.environ.reparentTo(self.render)
		self.environ.setScale(0.25, 0.25, 0.25)
		self.environ.setPos(-8, 42, 0)
		
		self.taskMgr.add(self.camera_task, "Camera")

		#Let's get some water in here!
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(1000)
		self.water.setSy(1000)
		self.water.setPos(0,0,0)
		ts = TextureStage('ts')
		self.water.setTexture(ts,loader.loadTexture("water.png"))
		self.water.setTexScale(ts,4)
		self.water.reparentTo(self.render)
				

	def camera_task(self, task):
		self.camera.setPos(0, -200, 100)
		self.camera.lookAt(0, 0, 0)
		return Task.cont




game = PIRATES()
game.run()


