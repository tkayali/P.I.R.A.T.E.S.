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

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)
		self.environ = self.loader.loadModel("/c/Panda3D-1.7.0/models/environment")
		self.environ.reparentTo(self.render)
		self.environ.setScale(0.25, 0.25, 0.25)
		self.environ.setPos(-8, 42, 0)
		
		self.taskMgr.add(self.camera_task, "Camera")

	def camera_task(self, task):
		self.camera.setPos(0, -200, 100)
		self.camera.lookAt(0, 0, 0)
		return Task.cont




game = PIRATES()
game.run()


