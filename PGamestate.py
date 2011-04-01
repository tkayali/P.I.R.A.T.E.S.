#First we need all the import statements for our lovely classes to work.
from PUnit import Unit
from PEnemy import Enemy
from PSonatu import Sonatu
from PGridspace import Gridspace
from PMap import Map

from math import pi, sin, cos
import random, sys, os

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import TextureStage, TransparencyAttrib, DirectionalLight, AmbientLight, VBase4, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, CollisionRay
from panda3d.core import loadPrcFile, ConfigVariableString

#Second we need the config variables. We'll ignore these for now.
loadPrcFile("Config/Config.prc")

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	__in_combat = True
	__player_turn = True

	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()	
		
		self.limbo()
		self.mouseTask = taskMgr.add(self.mouse_task, 'mouse_task')
		self.accept("escape", sys.exit)
		self.accept("h", self.limbo_hide_all )
		self.accept("c", self.setup_combat )
		self.accept("a", self.combat_hide_all )
		self.accept("z", self.limbo )
		self.accept("g", self.printCamera )
		
	def printCamera(self):	
		print self.camera.getX()
		print self.camera.getY()
		print self.camera.getZ()


	def limbo(self):
		#Change attributes
		self.__in_combat = False

		#Set up the camera
		self.taskMgr.add(self.limbo_camera_task, "Limbo Camera")

		#Set up the Limbo Sonatu
		#self.limbo_sonatu = self.loader.loadModel("Models\Limbo\Limbo.egg")
		self.limbo_sonatu = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.limbo_sonatu.setPos(0, 0, 0)
		self.limbo_sonatu.setHpr(-90, 0, 0)
		self.limbo_sonatu.reparentTo(self.render)

		#Set up the background sky
		self.sky = self.loader.loadModel("square.egg")
		self.sky.setSx(1000)
		self.sky.setSy(600)
		self.sky.setPos(-607.695, 436.47, 15.257)
		self.sky.setHpr(self.camera, 0, 90, 0)
		ts = TextureStage('ts')
		self.sky.setTexture(ts,loader.loadTexture("Textures\Sky.png"))
		self.sky.setTexRotate(ts, 180)
		self.sky.reparentTo(self.render)

		#Set up a lights
		self.sunlight = DirectionalLight('limbo_sunlight')
		self.sunlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
		self.sunlight_nodepath = render.attachNewNode(self.sunlight)
		self.sunlight_nodepath.setPos(937, -1386, 242) #1063, -1050, 555 || -12, -1625, 62
		self.sunlight_nodepath.lookAt(self.limbo_sonatu)
		render.setLight(self.sunlight_nodepath)

		self.ambientlight = AmbientLight("limbo_ambient")
		self.ambientlight.setColor(VBase4(0.2, 0.2, 0.2, 1))
		self.ambientlight_nodepath = render.attachNewNode(self.ambientlight)
		render.setLight(self.ambientlight_nodepath)

		#Set up the characters
		#Farthing
		self.farthing = self.loader.loadModel("Models\Characters\Farthing\Farthing.egg")
		self.farthing.setPos(-310.762, -3.750, -24.114)
		self.farthing.setHpr(0, 0, 0)
		self.farthing.setSx(.85)
		self.farthing.setSy(.85)
		self.farthing.setSz(.85)
		self.farthing.reparentTo(self.render)

		#Checkers
		self.checkers = self.loader.loadModel("Models\Characters\Farthing\Farthing.egg")
		self.checkers.setPos(-210.892, 35.105, -41.475)
		self.checkers.setHpr(-45, 0, 0)
		self.checkers.setSx(.85)
		self.checkers.setSy(.85)
		self.checkers.setSz(.85)
		self.checkers.reparentTo(self.render)

		#Ivan
		self.ivan = self.loader.loadModel("Models\Characters\Farthing\Farthing.egg")
		self.ivan.setPos(-150, 20, -70)
		self.ivan.setHpr(-45, 0, 0)
		self.ivan.setSx(.85)
		self.ivan.setSy(.85)
		self.ivan.setSz(.85)
		self.ivan.reparentTo(self.render)
		
	def setup_combat(self):
		#Set up attributes
		self.__in_combat = True

		#Set up the camera for the Combat Menu
		self.taskMgr.add(self.combat_camera_task, "Combat Camera")

		#Set up CombatUI
		self.combatHUD = OnscreenImage( image = 'Textures\hud.png', pos = (0, 0, -0.8))		
		self.combatHUD.setSz(.2)
		self.combatHUD.reparentTo(render2d)

		#Set up collision detection
		self.combat_collision_detection()

		#Combat water
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(1000)
		self.water.setSy(1000)
		self.water.setPos(0,0,-1)
		ts = TextureStage('ts')
		self.water.setTexture(ts,loader.loadTexture("Textures\Water.jpg"))
		self.water.setTexScale(ts,4)
		self.water.reparentTo(self.render)

		#Combat Sonatu
		self.combat_sonatu = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.combat_sonatu.setSx(.022)
		self.combat_sonatu.setSy(.022)
		self.combat_sonatu.setSz(.022)
		self.combat_sonatu.setPos(242.487, -90, 1)
		self.combat_sonatu.lookAt(-1000, 0, 0)
		self.combat_sonatu.reparentTo(self.render)
		self.sonatu = Sonatu(107, 0)

		#Monster - Melee
		self.melee_monster = self.loader.loadModel("Models\Monsters\octopus.egg")
		self.melee_monster.setSx(0.35)
		self.melee_monster.setSy(0.35)
		self.melee_monster.setSz(0.35)
		self.melee_monster.lookAt(-1000, 0, 0)
		self.melee_monster.setPos(17.321, -90, 1)
		self.melee_monster.reparentTo(self.render)
		self.melee = Enemy(94, 1)

		#Monster - Short
		self.short_monster = self.loader.loadModel("Models\Monsters\conch.egg")
		self.short_monster.setSx(0.35)
		self.short_monster.setSy(0.35)
		self.short_monster.setSz(0.35)
		self.short_monster.lookAt(-1000, 0, 0)
		self.short_monster.setPos(17.321, -120, 0)
		self.short_monster.reparentTo(self.render)
		self.short = Enemy(125, 2)

		#Monster - Long
		self.long_monster = self.loader.loadModel("Models\Monsters\serpent.egg")
		self.long_monster.setSx(0.35)
		self.long_monster.setSy(0.35)
		self.long_monster.setSz(0.35)
		self.long_monster.lookAt(1000, 0, 0)
		self.long_monster.setPos(17.321, -60, 0)
		self.long_monster.reparentTo(self.render)
		self.long = Enemy(63, 3)
		
		#Create the hex grid
		self.gridspace_list = []
		y_counter = 0
		hex_radius = 10
		for j in range(6):
			x_counter1 = 0
			x_counter2 = 10*sin(pi/3)
			for i in range(16):
				self.gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius, j*31+i))
				x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)
			
			y_counter = y_counter - 3/2.0*hex_radius
			for i in range(15):
				self.gridspace_list.append(Gridspace(None, True, x_counter2, y_counter, hex_radius, j*31+i+16))
				x_counter2 = x_counter2 + 2*hex_radius*sin(pi/3)
			y_counter = y_counter - 3/2.0*hex_radius
			if j == 5: 
				x_counter1 = 0
				for i in range (16):
					self.gridspace_list.append(Gridspace(None, True, x_counter1, y_counter, hex_radius, 31*6+i))
					x_counter1 = x_counter1 + 2*hex_radius*sin(pi/3)

		#Create map to hold the gridspaces
		self.combat_map = Map(self.gridspace_list, False)

		#Add a hex grid texture
		self.map_grid = self.loader.loadModel("square.egg")
		self.map_grid.setTexture(ts, loader.loadTexture("textures\HexGrid.png"))	
		self.map_grid.setPos(20*sin(pi/3)*7.5, -15*6, 0)
		self.map_grid.setSx(16*20*sin(pi/3)+5)
		self.map_grid.setSy(13.5*15+4)
		self.map_grid.setTransparency(TransparencyAttrib.MAlpha)
		self.map_grid.reparentTo(self.render)				

		#Set up all text
		self.setup_text()

		#Set up combat lighting
		render.clearLight(self.sunlight_nodepath)
		render.clearLight(self.ambientlight_nodepath)

		self.sunlight = DirectionalLight('combat_sunlight')
		self.sunlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
		self.sunlight_nodepath = render.attachNewNode(self.sunlight)
		self.sunlight_nodepath.setPos(129, -75, 2)
		self.sunlight_nodepath.lookAt(129, -75, 1)
		self.melee_monster.setLight(self.sunlight_nodepath)
		self.short_monster.setLight(self.sunlight_nodepath)
		self.long_monster.setLight(self.sunlight_nodepath)
		self.combat_sonatu.setLight(self.sunlight_nodepath)

		self.ambientlight = AmbientLight("combat_ambient")
		self.ambientlight.setColor(VBase4(0.2, 0.2, 0.2, 1))
		self.ambientlight_nodepath = render.attachNewNode(self.ambientlight)
		self.melee_monster.setLight(self.ambientlight_nodepath)
		self.short_monster.setLight(self.ambientlight_nodepath)
		self.long_monster.setLight(self.ambientlight_nodepath)
		self.combat_sonatu.setLight(self.ambientlight_nodepath)

	def limbo_hide_all(self):
		self.limbo_sonatu.hide()
		self.sky.hide()
		self.farthing.hide()
		self.checkers.hide()
		self.ivan.hide()
		render.clearLight(self.sunlight_nodepath)
		render.clearLight(self.ambientlight_nodepath)

	
	def combat_hide_all(self):
		self.map_grid.hide()
		self.water.hide()
		self.combat_sonatu.hide()
		self.melee_monster.hide()
		render.clearLight(self.sunlight_nodepath)
		render.clearLight(self.ambientlight_nodepath)

	def mouse_task(self, task):
		if base.mouseWatcherNode.hasMouse():
			if self.__in_combat:
				self.accept("mouse1", self.combat_mouse_task)
			else:
				self.accept("mouse1", self.limbo_mouse_task)
		return Task.cont

	def combat_mouse_task(self):
		if self.__player_turn:
			self.move_sonatu()
			self.update_text( self.__player_turn )
			#print "Player turn begins"
			#print "Sonatu's AP is .... : " + str(self.sonatu.getAP() )
			if self.sonatu.getAP() < 1:
				self.__player_turn = False
				self.sonatu.end_turn()
				#print "Player turn ends"
				#print "After the end of Sonatu's turn, the AP is now ... : " + str(self.sonatu.getAP())
				self.begin_enemy_turn()
		
	def limbo_mouse_task(self):
		print "Limbo"

	def move_sonatu(self):
		starting_gridspace = self.sonatu.get_gridspace()
		if base.mouseWatcherNode.hasMouse():
			self.mouse_position = base.mouseWatcherNode.getMouse()
			self.collision_ray.setFromLens(base.camNode, self.mouse_position.getX(), self.mouse_position.getY())
			self.traverser.traverse(render)
			if self.handler.getNumEntries() > 0:
				self.handler.sortEntries()
				ending_gridspace = int(self.handler.getEntry(0).getIntoNodePath().getTag("hex"))
				if self.gridspace_list[ending_gridspace].get_occupiable and starting_gridspace is not ending_gridspace:
					#print "Starting: " + str(starting_gridspace)
					#print "Ending: " + str(ending_gridspace)
					#print "Ending X: " + str(self.gridspace_list[ending_gridspace].get_x_position())
					#print "Ending Y: " + str(self.gridspace_list[ending_gridspace].get_y_position())
					path = self.combat_map.calculate_path(starting_gridspace, ending_gridspace)
					#print "Path: " + str(path)
					#print "Distance in hexes: " + str(len(path))
					if len(path) <= self.sonatu.getAP()+1:
						self.combat_sonatu.setPos( self.gridspace_list[ending_gridspace].get_x_position(), self.gridspace_list[ending_gridspace].get_y_position(), 1)
						self.sonatu.set_gridspace(ending_gridspace)
						self.gridspace_list[ending_gridspace].set_occupiable(False)
						self.gridspace_list[starting_gridspace].set_occupiable(True)
						self.sonatu.setAP(self.sonatu.getAP()-len(path)+1)

	def move_enemy(self, enemy):		
		starting_gridspace = enemy.get_gridspace()
		sonatu_position = self.sonatu.get_gridspace()
		path = self.combat_map.calculate_path(starting_gridspace, sonatu_position)
		distance = len(path) - 1
		#print "Starting: " + str(starting_gridspace)
		#print "Sonatu's position: " + str(sonatu_position)
		#print "Path: " + str(path)
		#print "Distance in hexes: " + str(len(path))
		#print "Unit range: " + str(enemy.get_unit_range())
		#print "AP Before: " + str(enemy.getAP())
		
		if distance == enemy.get_unit_range():
			#print "Attack"
			#print "Attack"
			enemy.setAP(0)
			return True

		elif distance == enemy.get_unit_range() + 1:
			if enemy.get_name() == "Melee":
				self.melee_monster.setPos( self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1)
			elif enemy.get_name() == "Short":
				self.short_monster.setPos( self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1)
			elif enemy.get_name() == "Long":
				self.long_monster.setPos( self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1)

			#print "Ending: " + str(path[1])
			#print "Ending: " + str(self.gridspace_list[path[1]])
			self.gridspace_list[starting_gridspace].set_occupiable(True)
			self.gridspace_list[path[1]].set_occupiable(False)
			enemy.set_gridspace(path[1])
			enemy.setAP(0)
			return True
		else:
			if enemy.get_name() == "Melee":
				self.melee_monster.setPos( self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1)
			elif enemy.get_name() == "Short":
				self.short_monster.setPos( self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1)
			elif enemy.get_name() == "Long":
				self.long_monster.setPos( self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1)

			#self.melee_monster.setPos( self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1)
			#print "Ending: " + str(path[2])
			#print "Ending: " + str(path[2])
			self.gridspace_list[starting_gridspace].set_occupiable(True)
			self.gridspace_list[path[2]].set_occupiable(False)
			enemy.setAP(0)
			enemy.set_gridspace(path[2])
			return True

		#print "AP After: " + str(enemy.getAP())
	
	def begin_enemy_turn(self):
		#print "Enemy begins"
		self.update_text( self.__player_turn )
		melee_check = self.move_enemy(self.melee)
		short_check = self.move_enemy(self.short)
		long_check = self.move_enemy(self.long)
		if melee_check and short_check and long_check:
			#print "Entered here"
			self.__player_turn = True
			self.melee.end_turn()
			self.short.end_turn()
			self.long.end_turn()
			#print "After the end of the turn the melee's AP is ... : " + str(self.melee.getAP())
			#print "Enemy ends"

			#Don't add the code below until timed events have been figured out
			#self.turn_text.setText("Your turn!")
	
	def setup_text(self):
		self.turn_text = OnscreenText( text = "Your turn!", pos = (0, .9, 0), scale = 0.065, fg = (1, 1, 1, 1) ) 
		self.sonatu_health_text = OnscreenText( text= "HP: " + str(self.sonatu.getHP()), pos = (-.5, -.9, 0), scale = 0.05, fg = (1, 1, 1, 1) )
		self.sonatu_ap_text = OnscreenText( text= "AP: " + str(self.sonatu.getAP()), pos = (-.5, -.8, 0), scale = 0.05, fg = (1, 1, 1, 1) )
		self.turn_text.reparentTo(render2d)
		self.sonatu_health_text.reparentTo(render2d)
		self.sonatu_ap_text.reparentTo(render2d)

	def update_text(self, player_turn):
		if player_turn:
			self.turn_text.setText("Your turn!")
		else:
			self.turn_text.setText("Enemy turn!")

		self.sonatu_health_text.setText( "HP: " + str(self.sonatu.getHP()) )
		self.sonatu_ap_text.setText("AP: " + str(self.sonatu.getAP()) )

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

game = PIRATES()
game.run()
