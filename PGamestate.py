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
		
		self.taskMgr.add(self.camera_task, "Camera")

		#Let's get some water in here!
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(1000)
		self.water.setSy(1000)
		self.water.setPos(0,0,0)
		ts = TextureStage('ts')
		self.water.setTexture(ts,loader.loadTexture("textures\water.jpg"))
		self.water.setTexScale(ts,3)
		self.water.reparentTo(self.render)

		#Sonatu!
		self.sonatu_model =
		self.loader.loadModel("Models\Sonatu\sonatu.egg")
		self.sonatu_model.setSx(.02)
		self.sonatu_model.setSy(.02)
		self.sonatu_model.setSz(.02)
		self.sonatu_model.setPos(-30, 0, 10)
		self.sonatu_model.setHpr(-90, 0, 0)
		#self.sonatu_model.setTexture(ts, 
		#loader.loadTexture("textures\LightBrown.jpg"))
		self.sonatu_model.reparentTo(self.render)
		sonatu = Sonatu(0, 0, 0, self.sonatu_model, 1)

		#Gridspace!

				

	def camera_task(self, task):
		self.camera.setPos(0, -160, 90)
		self.camera.lookAt(0, 0, 0)
		return Task.cont




game = PIRATES()
game.run()


