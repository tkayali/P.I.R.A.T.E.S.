#First we need all the import statements for our lovely classes to work.
from PUnit import Unit
from PEnemy import Enemy
from PSonatu import Sonatu
from PGridspace import Gridspace
from PMap import Map

from math import pi, sin, cos
import random, sys

from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from pandac.PandaModules import TextureStage, TransparencyAttrib, DirectionalLight, AmbientLight, VBase4, CollisionTraverser, CollisionHandlerQueue, CollisionNode, BitMask32, CollisionRay, NodePath, CollisionSphere, MovieTexture
from panda3d.core import loadPrcFile, ConfigVariableString, TextNode, Point3, PandaNode, LightRampAttrib, Vec3
from direct.interval.MetaInterval import Sequence
from direct.interval.FunctionInterval import Wait
from pandac.PandaModules import CInterval
from direct.filter.CommonFilters import CommonFilters
from direct.gui.DirectGui import *

#Second we need the config variables. We'll ignore these for now.
loadPrcFile("Config/Config.prc")

##Now let's begin with some lovely Panda code!
class PIRATES(ShowBase):
	__in_combat = False
        __in_limbo = False
        __in_dialogue = False
	__player_turn = True
	__number_enemies_alive = 0
	sonatu_end_turn = False
        
        #Import dialogue from associated files
        dialogue_checkers_l_crew = open('Config/checkers_l_1.txt').readlines()
        dialogue_checkers_l_status = open('Config/checkers_l_2.txt').readlines()
        dialogue_checkers_l_fun = open('Config/checkers_l_3.txt').readlines()
        dialogue_checkers_l_future = open('Config/checkers_l_4.txt').readlines()
        dialogue_checkers_l_situation = open('Config/checkers_l_s.txt').readlines()
        dialogue_farthing_l_hobby = open('Config/farthing_l_1.txt').readlines()
        dialogue_farthing_l_inspiration = open('Config/farthing_l_2.txt').readlines()
        dialogue_farthing_l_past = open('Config/farthing_l_3.txt').readlines()
        dialogue_farthing_l_status = open('Config/farthing_l_4.txt').readlines()
        dialogue_farthing_l_situation = open('Config/farthing_l_s.txt').readlines()
        dialogue_ivan_l_moot = open('Config/ivan_l_1.txt').readlines()
        dialogue_ivan_l_status = open('Config/ivan_l_2.txt').readlines()
        dialogue_ivan_l_past = open('Config/ivan_l_3.txt').readlines()
        dialogue_ivan_l_pirates = open('Config/ivan_l_4.txt').readlines()
        dialogue_ivan_l_situation = open('Config/ivan_l_s.txt').readlines()
        dialogue_michael = open('Config/michael.txt').readlines()
        dialogue_mission_1 = open('Config/mission_1.txt').readlines()
        dialogue_mission_2 = open('Config/mission_2.txt').readlines()
        dialogue_mission_3 = open('Config/mission_3.txt').readlines()
        dialogue_mission_4 = open('Config/mission_4.txt').readlines()
        dialogue_mission_5 = open('Config/mission_5.txt').readlines()
        dialogue_mission_6 = open('Config/mission_6.txt').readlines()

	def __init__(self):
		ShowBase.__init__(self)
		base.disableMouse()	

		self.collision_detection()
		self.limbo()

		mouseTask = taskMgr.add(self.mouse_task, 'mouse_task')
		taskMgr.add(self.end_turn_task, "end_turn")

		self.accept("arrow_down", self.display_line )
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
                self.__in_limbo = True
                
		#Set up the camera
		self.taskMgr.add(self.limbo_camera_task, "Limbo Camera")

		#Set up the Limbo Sonatu
		self.limbo_sonatu = self.loader.loadModel("Models\Limbo\Limbo.egg")
		#self.limbo_sonatu = self.loader.loadModel("Models\Sonatu\Sonatu.egg")
		self.limbo_sonatu.setPos(0, 0, 0)
		self.limbo_sonatu.setHpr(-90, 0, 0)
		self.limbo_sonatu.reparentTo(self.render)

		#Set up the background sky
		self.sky = self.loader.loadModel("square.egg")
		self.sky.setSx(4800)	 	
		self.sky.setSy(2400)
		self.sky.setPos(-800, 1400, 80)
		self.sky.setHpr(45, 90, 0)
		ts = TextureStage('ts')
		self.sky.setTexture(ts,loader.loadTexture("Models\Limbo\Sky.jpg"))
		self.sky.setTexRotate(ts, 180)
		self.sky.reparentTo(self.render)
		
		#Set up water!!!
		self.water_limbo = self.loader.loadModel("square.egg")
		self.water_limbo.setSx(2400)
		self.water_limbo.setSy(2400)
		self.water_limbo.setPos(self.limbo_sonatu, 0, 0, 50)
		#ts = TextureStage('ts')
		#self.waterTexture = loader.loadTexture("Textures\Water.jpg")
		self.waterTexture2 = loader.loadTexture("Textures\Sea.mpg")
		self.waterTexture2.setLoop(True)
		self.waterTexture2.setPlayRate(2)
		#self.water.setTexture(ts, self.waterTexture)
		#self.water_limbo.setTexScale(ts, 4)
		self.water_limbo.setTexture(self.waterTexture2)
		self.water_limbo.reparentTo(self.render)

		#Set up a lights
		self.sunlight = DirectionalLight('limbo_sunlight')
		self.sunlight.setColor(VBase4(0.8, 0.8, 0.5, 1))
		self.sunlight_nodepath = render.attachNewNode(self.sunlight)
		self.sunlight_nodepath.setPos(937, -1386, 242) #1063, -1050, 555 || -12, -1625, 62
		self.sunlight_nodepath.lookAt(self.limbo_sonatu)
		render.setLight(self.sunlight_nodepath)

		self.waterlight = DirectionalLight('limbo_sunlight')
		self.waterlight.setColor(VBase4(1, 1, 1, 1))
		self.waterlight_nodepath = render.attachNewNode(self.waterlight)
		self.waterlight_nodepath.setPos(-129, 585, 645) #1063, -1050, 555 || -12, -1625, 62
		self.waterlight_nodepath.lookAt(self.water_limbo)
		self.water_limbo.setLight(self.waterlight_nodepath)

		self.ambientlight = AmbientLight("limbo_ambient")
		self.ambientlight.setColor(VBase4(0.2, 0.2, 0.2, 1))
		self.ambientlight_nodepath = render.attachNewNode(self.ambientlight)
		render.setLight(self.ambientlight_nodepath)
		
		#Set up shadows
		#tempnode = NodePath(PandaNode("temp node"))
        	#tempnode.setAttrib(LightRampAttrib.makeDoubleThreshold(0.3, 0.7, 0.4, 0.8)) #np.setAttrib(LightRampAttrib.makeDoubleThreshold(t0, l0, t1, l1)
        	#tempnode.setShaderAuto()
        	#base.cam.node().setInitialState(tempnode.getState())	
        	self.filters = CommonFilters(base.win, base.cam)
        	self.blur_sharpen = self.filters.setBlurSharpen(.8)
		self.cartoon_ink = self.filters.setCartoonInk(0.5)

		#Set up the characters
		#Farthing
		self.farthing = self.limbo_sonatu.find("**/Farthing1")
		self.farthing_csphere = CollisionSphere(-70, -175, 125, 15)
		self.farthing_node = self.farthing.attachNewNode(CollisionNode("farthing"))
		self.farthing_node.node().addSolid(self.farthing_csphere)
		#self.farthing_node.show()
		self.farthing_node.setTag("name", "Farthing")

		#Checkers
		self.checkers = self.limbo_sonatu.find("**/Checkers")
		self.checkers_csphere = CollisionSphere(7, -55, 95, 15)
		self.checkers_node = self.checkers.attachNewNode(CollisionNode("checkers"))
		self.checkers_node.node().addSolid(self.checkers_csphere)
		#self.checkers_node.show()
		self.checkers_node.setTag("name", "Checkers")
		
		#Ivan
		self.ivan = self.limbo_sonatu.find("**/Ironhide1")
		self.ivan_csphere = CollisionSphere(-45, -42, 95, 15)
		self.ivan_node = self.ivan.attachNewNode(CollisionNode("checkers"))
		self.ivan_node.node().addSolid(self.ivan_csphere)
		#self.ivan_node.show()
		self.ivan_node.setTag("name", "Ivan")

		#Michael
		self.michael = self.limbo_sonatu.find("**/Michael1")
		self.michael_csphere = CollisionSphere(18, 22, 100, 15)
		self.michael_node = self.michael.attachNewNode(CollisionNode("checkers"))
		self.michael_node.node().addSolid(self.michael_csphere)
		#self.michael_node.show()
		self.michael_node.setTag("name", "Michael")

		#Set up instructions
		self.calibri_font = loader.loadFont('Config/calibri.ttf')
		self.instructions_text = OnscreenText( text = "Interact with the characters!\nPress ESC to exit!", pos = (-1, .95), scale = 0.04, fg = (0, 0, 0, .8), shadow = (0, 0, 0, 1), align = TextNode.ALeft, font = self.calibri_font, mayChange = True)
		self.instructions_text.reparentTo(render2d)

	def reset_combat(self):
		#Reset up attributes
		self.__player_turn = True

		self.combat_hide_all()
		self.setup_combat()
		
	def setup_combat(self):
		#Set up attributes
                self.__in_limbo = False
		self.__in_combat = True
		self.__number_enemies_alive = 3

		#Remove blursharpen and cartoon ink
        	self.filters.delCartoonInk()
		self.filters.delBlurSharpen()

		#Set up the camera for the Combat Menu
		self.taskMgr.add(self.combat_camera_task, "Combat Camera")

		#Set up CombatUI
		self.combatHUD = OnscreenImage( image = 'Textures\hud.png', pos = (0, 0, -0.8))		
		self.combatHUD.setSz(.2)
		self.combatHUD.reparentTo(render2d)
		self.end_turn_button = DirectButton( text = ( "END TURN"), text_scale = 0.2, pos = Vec3(1.0, 0, -0.8), text_align=TextNode.ACenter, scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL , command = self.set_sonatu_end_turn, extraArgs = [True], relief = DGG.RIDGE, frameColor = (.6235, .4353, .2471, 1))

		#Set up collision detection
		#self.combat_collision_detection()

		#Set up sequences
		self.melee_monster_sequence = Sequence()
		self.short_monster_sequence = Sequence()
		self.long_monster_sequence = Sequence()

		#Combat water
		self.water = self.loader.loadModel("square.egg")
		self.water.setSx(600)
		self.water.setSy(600)
		self.water.setPos(150, -150, -1)
		ts = TextureStage('ts')
		#self.waterTexture = loader.loadTexture("Textures\Water.jpg")
		self.waterTexture = loader.loadTexture("Textures\Sea.mpg")
		self.waterTexture.setLoop(True)
		#self.waterTexture.setPlayRate(4)
		#self.water.setTexture(ts, self.waterTexture)
		#self.water.setTexScale(ts, 1.5)
		self.water.setTexture(self.waterTexture)
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
		
		#Our lovely lists
		self.monster_list = []
		self.monster_model_list = []
		self.gridspace_list = []

		#Monster - Melee
		self.melee_monster = self.loader.loadModel("Models\Monsters\octopus.egg")
		self.melee_monster.setSx(0.35)
		self.melee_monster.setSy(0.35)
		self.melee_monster.setSz(0.35)
		self.melee_monster.lookAt(-1000, 0, 0)
		self.melee_monster.setPos(17.321, -90, 1)
		self.melee_monster.reparentTo(self.render)
		self.melee = Enemy(94, 1)
		self.monster_list.append(self.melee)
		self.monster_model_list.append(self.melee_monster)

		#Monster - Short
		self.short_monster = self.loader.loadModel("Models\Monsters\conch.egg")
		self.short_monster.setSx(0.35)
		self.short_monster.setSy(0.35)
		self.short_monster.setSz(0.35)
		self.short_monster.lookAt(-1000, 0, 0)
		self.short_monster.setPos(17.321, -120, 0)
		self.short_monster.reparentTo(self.render)
		self.short = Enemy(125, 2)
		self.monster_list.append(self.short)
		self.monster_model_list.append(self.short_monster)

		#Monster - Long
		self.long_monster = self.loader.loadModel("Models\Monsters\serpent.egg")
		self.long_monster.setSx(0.35)
		self.long_monster.setSy(0.35)
		self.long_monster.setSz(0.35)
		self.long_monster.lookAt(1000, 0, 0)
		self.long_monster.setPos(17.321, -60, 0)
		self.long_monster.reparentTo(self.render)
		self.long = Enemy(63, 4)
		self.monster_list.append(self.long)
		self.monster_model_list.append(self.long_monster)
		
		#Create the hex grid
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
		self.water_limbo.clearLight(self.waterlight_nodepath)

		self.sunlight = DirectionalLight('combat_sunlight')
		self.sunlight.setColor(VBase4(1, 1, 1, 1))
		self.sunlight_nodepath = render.attachNewNode(self.sunlight)
		self.sunlight_nodepath.setPos(129, -75, 2)
		self.sunlight_nodepath.lookAt(129, -75, 1)
		self.melee_monster.setLight(self.sunlight_nodepath)
		self.short_monster.setLight(self.sunlight_nodepath)
		self.long_monster.setLight(self.sunlight_nodepath)
		self.combat_sonatu.setLight(self.sunlight_nodepath)
		self.water.setLight(self.sunlight_nodepath)

		self.ambientlight = AmbientLight("combat_ambient")
		self.ambientlight.setColor(VBase4(0.2, 0.2, 0.2, 1))
		self.ambientlight_nodepath = render.attachNewNode(self.ambientlight)
		self.melee_monster.setLight(self.ambientlight_nodepath)
		self.short_monster.setLight(self.ambientlight_nodepath)
		self.long_monster.setLight(self.ambientlight_nodepath)
		self.combat_sonatu.setLight(self.ambientlight_nodepath)
		self.water.setLight(self.ambientlight_nodepath)

	def limbo_hide_all(self):
		self.limbo_sonatu.hide()
		self.sky.hide()
		self.farthing.hide()
		self.checkers.hide()
		self.ivan.hide()
		self.water_limbo.hide()
		self.dialogue_box.hide()
		self.instructions_text.hide()
		render.clearLight(self.sunlight_nodepath)
		render.clearLight(self.ambientlight_nodepath)
	
	def combat_hide_all(self):
		for i in range(len(self.monster_list)):
			if self.monster_list[i].get_alive():
				self.monster_model_list[i].hide()

		self.map_grid.hide()
		self.water.hide()
		self.combat_sonatu.hide()
		render.clearLight(self.sunlight_nodepath)
		render.clearLight(self.ambientlight_nodepath)
		self.turn_text.hide()
		self.sonatu_health_text.hide()
		self.sonatu_ap_text.hide()
		self.attack_type_text.hide()
		self.game_over_text.hide()
		self.game_win_text.hide()
		self.combatHUD.hide()

	def mouse_task(self, task):
		if base.mouseWatcherNode.hasMouse():
			if self.__in_combat:
				self.accept("mouse1", self.combat_mouse_task)

			elif self.__in_limbo:
				self.accept("mouse1", self.limbo_mouse_task)
		return Task.cont
	
	def combat_mouse_task(self):
		if self.__player_turn:
			if self.__number_enemies_alive > 0:
				self.sonatu_turn()
				self.update_text( self.__player_turn )
				if self.__number_enemies_alive < 1:
					self.game_win_text.setText("YOU WIN!!! REJOICE!")

	def limbo_mouse_task(self):
		if base.mouseWatcherNode.hasMouse() and not self.__in_dialogue:
			self.mouse_position = base.mouseWatcherNode.getMouse()
			self.collision_ray.setFromLens(base.camNode, self.mouse_position.getX(), self.mouse_position.getY())
			self.traverser.traverse(render)
			if self.handler.getNumEntries() > 0:
				self.handler.sortEntries()
				#self.current_speaker = self.handler.getEntry(0).getIntoNodePath().getTag("name")
				self.begin_dialogue(self.handler.getEntry(0).getIntoNodePath().getTag("name"))
				

	def sonatu_turn(self):
		starting_gridspace = self.sonatu.get_gridspace()
		if base.mouseWatcherNode.hasMouse() and not self.melee_monster_sequence.isPlaying() and not self.short_monster_sequence.isPlaying() and not self.long_monster_sequence.isPlaying():
			self.mouse_position = base.mouseWatcherNode.getMouse()
			self.collision_ray.setFromLens(base.camNode, self.mouse_position.getX(), self.mouse_position.getY())
			self.traverser.traverse(render)
			if self.handler.getNumEntries() > 0:
				self.handler.sortEntries()
				ending_gridspace = int(self.handler.getEntry(0).getIntoNodePath().getTag("hex"))

				#Check to see if empty hex is clicked
				if self.gridspace_list[ending_gridspace].get_occupiable() and starting_gridspace is not ending_gridspace:
					path = self.combat_map.calculate_path(starting_gridspace, ending_gridspace)
					if len(path) <= self.sonatu.getAP()+1:
						#switch statement goes here
						#must account for 1 hex away, 2 hexes away, 3 hexes away
						self.sonatu_interval1 = self.combat_sonatu.posInterval(0.5, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.gridspace_list[starting_gridspace].get_x_position(), self.gridspace_list[starting_gridspace].get_y_position(), 1), "sonatuMove1")
						self.sonatu_sequence = Sequence( self.sonatu_interval1 )
						if len(path) > 2:
							self.sonatu_interval2 = self.combat_sonatu.posInterval(0.5, Point3(self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1), Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), "sonatuMove1")
							self.sonatu_sequence.append( self.sonatu_interval2 )
						if len(path) > 3:
							self.sonatu_interval3 = self.combat_sonatu.posInterval(0.5, Point3(self.gridspace_list[path[3]].get_x_position(), self.gridspace_list[path[3]].get_y_position(), 1), Point3(self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1), "sonatuMove1")
							self.sonatu_sequence.append( self.sonatu_interval3 )
						self.sonatu_sequence.start()

						#self.combat_sonatu.setPos( self.gridspace_list[ending_gridspace].get_x_position(), self.gridspace_list[ending_gridspace].get_y_position(), 1)
						self.sonatu.set_gridspace(ending_gridspace)
						self.gridspace_list[ending_gridspace].set_occupiable(False)
						self.gridspace_list[starting_gridspace].set_occupiable(True)
						self.gridspace_list[starting_gridspace].set_occupying_unit(None)
						self.gridspace_list[ending_gridspace].set_occupying_unit(self.sonatu)
						self.sonatu.setAP(self.sonatu.getAP()-len(path)+1)

				#Check to see if enemy is clicked
				elif self.gridspace_list[ending_gridspace].get_occupying_unit() is not None and starting_gridspace is not ending_gridspace:
					distance = len(self.combat_map.calculate_crow_path(starting_gridspace, ending_gridspace))-1
					if self.sonatu.getAP() > 1:
						unit_attacked = self.gridspace_list[ending_gridspace].get_occupying_unit()

						if distance == 1:
							self.attack_type_text.setText("Attack with melee!")
							if random.randint(1, 100) <= 90:
								unit_attacked.setHP(unit_attacked.getHP() - 10)
							else:
								self.attack_type_text.setText("Attack missed! DOH")

						elif distance == 2:
							self.attack_type_text.setText("Attack with short!")
							if random.randint(1, 100) <= 85:
								unit_attacked.setHP(unit_attacked.getHP() - 6 )
							else:
								self.attack_type_text.setText("Attack missed! DOH")

						elif distance <=4:
							self.attack_type_text.setText("Attack with long!")
							if random.randint(1, 100) <= 80:
								unit_attacked.setHP(unit_attacked.getHP() - 4 )
							else:
								self.attack_type_text.setText("Attack missed! DOH")
						else:
							return	
						
						self.sonatu.setAP(self.sonatu.getAP()-2)
						if unit_attacked.getHP() <= 0:
							if unit_attacked.get_name() == "Melee":
								self.melee_monster.removeNode()
							elif unit_attacked.get_name() == "Short":
								self.short_monster.removeNode()
							elif unit_attacked.get_name() == "Long":
								self.long_monster.removeNode()
							
							self.gridspace_list[ending_gridspace].set_occupying_unit(None)
							self.gridspace_list[ending_gridspace].set_occupiable(True)
							unit_attacked.set_alive(False)
							self.__number_enemies_alive -= 1

	def begin_dialogue(self, character):
		self.current_speaker = character
                self.__in_dialogue = True
		self.taskMgr.remove("Limbo Camera")
		self.dialogue_font = loader.loadFont("Config/King Luau.ttf")
		self.dialogue_box = OnscreenImage( image = 'Textures/DialogueBox.png', pos = (0, 0, -0.65 ), scale = (1, 1, .35) )	
		self.dialogue_box.setTransparency(TransparencyAttrib.MAlpha)
		self.dialogue_box.setAlphaScale(0.7)
		self.dialogue_box.reparentTo(render2d)
		self.dialogue_line_number = 0
		self.current_dialogue = None
		self.line = OnscreenText(pos = (0, 0.5, 0), scale = (0.08, 0.18), fg = (0, 0, 0, 1), shadow = (0, 0, 0, 1), align = TextNode.ACenter, wordwrap = 20, font = self.dialogue_font, parent = self.dialogue_box, mayChange = 1)

		#Dialogue greeting to be changed for each individual
		self.dialogue_greeting = OnscreenText( text = "", pos = (0, 0.5, 0), scale = (0.1, 0.2), fg = (0, 0, 0, 1), shadow = (0, 0, 0, 1), align = TextNode.ACenter, wordwrap = 20, font = self.dialogue_font, parent = self.dialogue_box, mayChange = 1)

		#Back button for each dialogue menu
                self.dialogue_back_button = DirectButton(pos = Vec3(0.8, 0, -0.70), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, command = self.end_dialogue, extraArgs = [character], relief = DGG.GROOVE, frameColor = (.8, .867, .933, 1), pad = (0.7, 0.08))
		self.dialogue_back_button["text"] = "Back"
		self.dialogue_back_button["text_scale"] = 0.15
		self.dialogue_back_button["text_pos"] = (0, -.03)
		self.dialogue_back_button["text_align"] = TextNode.ACenter	

		self.dialogue_personal_button1 = DirectButton(pos = Vec3(-0.8, 0, -0.70), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, relief = DGG.GROOVE, frameColor = (.6235, .4353, .2471, 1), pad = (0.7, 0.08))
		self.dialogue_personal_button2 = DirectButton(pos = Vec3(-0.8, 0, -0.88), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, relief = DGG.GROOVE, frameColor = (.6235, .4353, .2471, 1), pad = (0.7, 0.08))
		self.dialogue_personal_button3 = DirectButton(pos = Vec3( 0.8, 0, -0.88), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, relief = DGG.GROOVE, frameColor = (.6235, .4353, .2471, 1), pad = (0.7, 0.08))
		self.dialogue_personal_button4 = DirectButton(pos = Vec3( 0, 0, -0.88), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, relief = DGG.GROOVE, frameColor = (.6235, .4353, .2471, 1), pad = (0.7, 0.08))
		self.dialogue_situation_button = DirectButton(pos = Vec3( 0, 0, -0.70), scale = 0.4, pressEffect = 1, textMayChange = 1, state = DGG.NORMAL, relief = DGG.GROOVE, frameColor = (.6235, .4353, .2471, 1), pad = (0.7, 0.08))

		
		if character == "Farthing":
			#Add the personalized text
			self.dialogue_greeting.setText("Farthing: Oh! Hello Captain!")
			self.dialogue_personal_button1["text"] = "Hobby"
			self.dialogue_personal_button1["text_scale"] = 0.15
			self.dialogue_personal_button1["text_pos"] = (0, -.03)
			self.dialogue_personal_button1["text_align"] = TextNode.ACenter
			self.dialogue_personal_button1['command'] = self.display_dialogue
			self.dialogue_personal_button1['extraArgs'] = [self.dialogue_farthing_l_hobby]
			self.dialogue_personal_button2["text"] = "Inspiration"
			self.dialogue_personal_button2["text_scale"] = 0.15
			self.dialogue_personal_button2["text_pos"] = (0, -.03)
			self.dialogue_personal_button2["text_align"] = TextNode.ACenter
			self.dialogue_personal_button2['command'] = self.display_dialogue
			self.dialogue_personal_button2['extraArgs'] = [self.dialogue_farthing_l_inspiration]
			self.dialogue_personal_button3['text'] = "Past"
			self.dialogue_personal_button3['text_scale'] = 0.15
			self.dialogue_personal_button3['text_pos'] = (0, -.03)
			self.dialogue_personal_button3['text_align'] = TextNode.ACenter
			self.dialogue_personal_button3['command'] = self.display_dialogue
			self.dialogue_personal_button3['extraArgs'] = [self.dialogue_farthing_l_past]
			self.dialogue_personal_button4['text'] = "Status"
			self.dialogue_personal_button4['text_scale'] = 0.15
			self.dialogue_personal_button4['text_pos'] = (0, -.03)
			self.dialogue_personal_button4['text_align'] = TextNode.ACenter
			self.dialogue_personal_button4['command'] = self.display_dialogue
			self.dialogue_personal_button4['extraArgs'] = [self.dialogue_farthing_l_status]
			self.dialogue_situation_button['text'] = "Situation"
			self.dialogue_situation_button['text_scale'] = 0.15
			self.dialogue_situation_button['text_pos'] = (0, -.03)
			self.dialogue_situation_button['text_align'] = TextNode.ACenter
			self.dialogue_situation_button['command'] = self.display_dialogue
			self.dialogue_situation_button['extraArgs'] = [self.dialogue_farthing_l_situation]
			self.current_speaker = "Farthing"

			self.taskMgr.add(self.limbo_camera_task_farthing, "Farthing Camera")
			return

		elif character == "Ivan":
			#Add the personalized text
			self.dialogue_greeting.setText("Ivan: Cap'")
			self.dialogue_personal_button1["text"] = "Moot"
			self.dialogue_personal_button1["text_scale"] = 0.15
			self.dialogue_personal_button1["text_pos"] = (0, -.03)
			self.dialogue_personal_button1["text_align"] = TextNode.ACenter
			self.dialogue_personal_button1['command'] = self.display_dialogue
			self.dialogue_personal_button1['extraArgs'] = [self.dialogue_ivan_l_moot]
			self.dialogue_personal_button2["text"] = "P.I.R.A.T.E.S"
			self.dialogue_personal_button2["text_scale"] = 0.15
			self.dialogue_personal_button2["text_pos"] = (0, -.03)
			self.dialogue_personal_button2["text_align"] = TextNode.ACenter
			self.dialogue_personal_button2['command'] = self.display_dialogue
			self.dialogue_personal_button2['extraArgs'] = [self.dialogue_ivan_l_pirates]
			self.dialogue_personal_button3['text'] = "Past"
			self.dialogue_personal_button3['text_scale'] = 0.15
			self.dialogue_personal_button3['text_pos'] = (0, -.03)
			self.dialogue_personal_button3['text_align'] = TextNode.ACenter
			self.dialogue_personal_button3['command'] = self.display_dialogue
			self.dialogue_personal_button3['extraArgs'] = [self.dialogue_ivan_l_past]
			self.dialogue_personal_button4['text'] = "Status"
			self.dialogue_personal_button4['text_scale'] = 0.15
			self.dialogue_personal_button4['text_pos'] = (0, -.03)
			self.dialogue_personal_button4['text_align'] = TextNode.ACenter
			self.dialogue_personal_button4['command'] = self.display_dialogue
			self.dialogue_personal_button4['extraArgs'] = [self.dialogue_ivan_l_status]
			self.dialogue_situation_button['text'] = "Situation"
			self.dialogue_situation_button['text_scale'] = 0.15
			self.dialogue_situation_button['text_pos'] = (0, -.03)
			self.dialogue_situation_button['text_align'] = TextNode.ACenter
			self.dialogue_situation_button['command'] = self.display_dialogue
			self.dialogue_situation_button['extraArgs'] = [self.dialogue_ivan_l_situation]

			self.taskMgr.add(self.limbo_camera_task_ivan, "Ivan Camera")
			return

		elif character == "Checkers":
			#Add the personalized text
			self.dialogue_greeting.setText("Checkers: Heya Captain, how's it going?")
			self.dialogue_personal_button1["text"] = "Fun"
			self.dialogue_personal_button1["text_scale"] = 0.15
			self.dialogue_personal_button1["text_pos"] = (0, -.03)
			self.dialogue_personal_button1["text_align"] = TextNode.ACenter
			self.dialogue_personal_button1['command'] = self.display_dialogue
			self.dialogue_personal_button1['extraArgs'] = [self.dialogue_checkers_l_fun]
			self.dialogue_personal_button2["text"] = "Crew"
			self.dialogue_personal_button2["text_scale"] = 0.15
			self.dialogue_personal_button2["text_pos"] = (0, -.03)
			self.dialogue_personal_button2["text_align"] = TextNode.ACenter
			self.dialogue_personal_button2['command'] = self.display_dialogue
			self.dialogue_personal_button2['extraArgs'] = [self.dialogue_checkers_l_crew]
			self.dialogue_personal_button3['text'] = "Future"
			self.dialogue_personal_button3['text_scale'] = 0.15
			self.dialogue_personal_button3['text_pos'] = (0, -.03)
			self.dialogue_personal_button3['text_align'] = TextNode.ACenter
			self.dialogue_personal_button3['command'] = self.display_dialogue
			self.dialogue_personal_button3['extraArgs'] = [self.dialogue_checkers_l_future]
			self.dialogue_personal_button4['text'] = "Status"
			self.dialogue_personal_button4['text_scale'] = 0.15
			self.dialogue_personal_button4['text_pos'] = (0, -.03)
			self.dialogue_personal_button4['text_align'] = TextNode.ACenter
			self.dialogue_personal_button4['command'] = self.display_dialogue
			self.dialogue_personal_button4['extraArgs'] = [self.dialogue_checkers_l_status]
			self.dialogue_situation_button['text'] = "Situation"
			self.dialogue_situation_button['text_scale'] = 0.15
			self.dialogue_situation_button['text_pos'] = (0, -.03)
			self.dialogue_situation_button['text_align'] = TextNode.ACenter
			self.dialogue_situation_button['command'] = self.display_dialogue
			self.dialogue_situation_button['extraArgs'] = [self.dialogue_checkers_l_situation]

			self.taskMgr.add(self.limbo_camera_task_checkers, "Checkers Camera")
			return

		elif character == "Michael":
			#Add the personalized text and delete unnecessary buttons
			self.dialogue_greeting.setText("Ready for your mission?")
			self.dialogue_personal_button1['text'] = "Yes"
			self.dialogue_personal_button1['text_scale'] = 0.15
			self.dialogue_personal_button1['text_pos'] = (0, -.03)
			self.dialogue_personal_button1['text_align'] = TextNode.ACenter
			self.dialogue_personal_button1['command'] = self.display_dialogue
			self.dialogue_personal_button1['extraArgs'] = [self.dialogue_michael]
			self.dialogue_back_button['text'] = "No"
			self.dialogue_personal_button2.destroy()
			self.dialogue_personal_button3.destroy()
			self.dialogue_personal_button4.destroy()
			self.dialogue_situation_button.destroy()

			self.taskMgr.add(self.limbo_camera_task_michael, "Michael Camera")

			#self.limbo_hide_all()
			#self.setup_combat()

	def display_dialogue(self, dialogue):
		if self.current_speaker is not "Michael":
			self.dialogue_personal_button2.destroy()
			self.dialogue_personal_button3.destroy()
			self.dialogue_personal_button4.destroy()
			self.dialogue_situation_button.destroy()
		
		self.dialogue_personal_button1.destroy()
		self.dialogue_back_button.destroy()
		self.current_dialogue = dialogue
		self.dialogue_line_number = 0
		self.display_line()
	
	def display_line(self):
		if self.current_dialogue is None:
			return
		
		elif len(self.current_dialogue) == self.dialogue_line_number:
			if self.current_speaker == "Michael":
				self.limbo_hide_all()
				self.setup_combat()
				self.current_dialogue = None
				self.dialogue_line_number = 0
				self.current_speaker = None
			else:
				self.dialogue_box.hide()
				self.begin_dialogue(self.current_speaker)
				self.current_dialogue = None
				self.dialogue_line_number = 0
				self.dialogue_greeting.show()



		else:
			self.dialogue_greeting.hide()
			self.line.setText(text = self.current_dialogue[self.dialogue_line_number])
			self.dialogue_line_number += 1
        
        def end_dialogue(self, character):
                self.__in_dialogue = False

		#Remove zoomed in cameras and add regular limbo camera
                if character == "Farthing":
			self.taskMgr.remove("Farthing Camera")
		elif character == "Ivan":
			self.taskMgr.remove("Ivan Camera")
		elif character == "Checkers":
			self.taskMgr.remove("Checkers Camera")
		elif character == "Michael":
			self.taskMgr.remove("Michael Camera")

                self.taskMgr.add(self.limbo_camera_task, "Limbo Camera")

		#Hide dialogue_box and destroy direct buttons
	        self.dialogue_box.hide()
		self.dialogue_back_button.destroy()
		self.dialogue_personal_button1.destroy()

		if character is not "Michael":
	 		self.dialogue_personal_button2.destroy()
			self.dialogue_personal_button3.destroy()
			self.dialogue_personal_button4.destroy()
			self.dialogue_situation_button.destroy()        

	def enemy_turn(self, enemy):		
		starting_gridspace = enemy.get_gridspace()
		sonatu_position = self.sonatu.get_gridspace()
		path = self.combat_map.calculate_path(starting_gridspace, sonatu_position)
		distance = len(path) - 1

		if distance <= enemy.get_unit_range():
			if random.randint(1, 100) <= enemy.get_accuracy():
				self.sonatu.setHP(self.sonatu.getHP() - enemy.get_damage())
				self.sonatu_health_text.setText( "HP: " + str(self.sonatu.getHP()))

			if random.randint(1, 100) <= enemy.get_accuracy():
				self.sonatu.setHP(self.sonatu.getHP() - enemy.get_damage())
				self.sonatu_health_text.setText( "HP: " + str(self.sonatu.getHP()))

			enemy.setAP(0)
			return True

		elif distance == enemy.get_unit_range() + 1:
			if enemy.get_name() == "Melee":
				self.melee_interval1 = self.melee_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.melee_monster.getX(), self.melee_monster.getY(), 1), "meleeMove1")
				self.melee_monster_sequence = Sequence(	self.melee_interval1 )
				self.melee_monster_sequence.start()
			elif enemy.get_name() == "Short":
				self.short_interval1 = self.short_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.short_monster.getX(), self.short_monster.getY(), 1), "shortMove1")
				self.short_monster_sequence = Sequence( self.short_interval1 )
				self.short_monster_sequence.start()
			elif enemy.get_name() == "Long":
				self.long_interval1 = self.long_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.long_monster.getX(), self.long_monster.getY(), 1), "shortMove1")
				self.long_monster_sequence = Sequence( self.long_interval1 )
				self.long_monster_sequence.start()

			if random.randint(1, 100) <= enemy.get_accuracy():
				self.sonatu.setHP(self.sonatu.getHP() - enemy.get_damage())
				self.sonatu_health_text.setText( "HP: " + str(self.sonatu.getHP()))

			self.gridspace_list[starting_gridspace].set_occupiable(True)
			self.gridspace_list[starting_gridspace].set_occupying_unit(None)
			self.gridspace_list[path[1]].set_occupiable(False)
			self.gridspace_list[path[1]].set_occupying_unit(enemy)
			enemy.set_gridspace(path[1])
			enemy.setAP(0)
			return True
		else:
			if enemy.get_name() == "Melee":
				self.melee_interval1 = self.melee_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.melee_monster.getX(), self.melee_monster.getY(), 1), "meleeMove1")
				self.melee_interval2 = self.melee_monster.posInterval( 0.7, Point3(self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1), Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), "meleeMove2")
				self.melee_monster_sequence = Sequence(self.melee_interval1, self.melee_interval2)
				self.melee_monster_sequence.start()

			elif enemy.get_name() == "Short":
				self.short_interval1 = self.short_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.short_monster.getX(), self.short_monster.getY(), 1), "shortMove1")
				self.short_interval2 = self.short_monster.posInterval( 0.7, Point3(self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1), Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), "shortMove2")
				self.short_monster_sequence = Sequence(self.short_interval1, self.short_interval2)
				self.short_monster_sequence.start()

			elif enemy.get_name() == "Long":
				self.long_interval1 = self.long_monster.posInterval(0.7, Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), Point3(self.long_monster.getX(), self.long_monster.getY(), 1), "longMove1")
				self.long_interval2 = self.long_monster.posInterval( 0.7, Point3(self.gridspace_list[path[2]].get_x_position(), self.gridspace_list[path[2]].get_y_position(), 1), Point3(self.gridspace_list[path[1]].get_x_position(), self.gridspace_list[path[1]].get_y_position(), 1), "longMove2")
				self.long_monster_sequence = Sequence(self.long_interval1, self.long_interval2)
				self.long_monster_sequence.start()

			self.gridspace_list[starting_gridspace].set_occupiable(True)
			self.gridspace_list[starting_gridspace].set_occupying_unit(None)
			self.gridspace_list[path[2]].set_occupiable(False)
			self.gridspace_list[path[2]].set_occupying_unit(enemy)
			enemy.setAP(0)
			enemy.set_gridspace(path[2])
			return True

	def begin_enemy_turn(self):
		self.update_text( self.__player_turn )
		
		for monster in self.monster_list:
			if monster.get_alive():
				self.enemy_turn(monster)
				monster.end_turn()

		if self.sonatu.getHP() <= 0:
			self.game_over_text.setText("GAME OVER! DEAL WITH IT!")
			self.reset_combat()
		
		else:
			self.__player_turn = True

	def setup_text(self):
		self.turn_text = OnscreenText( text = "Your turn!", pos = (0, .9, 0), scale = 0.065, fg = (1, 1, 1, 1) ) 
		self.sonatu_health_text = OnscreenText( text= "HP: " + str(self.sonatu.getHP()), pos = (-.5, -.9, 0), scale = 0.05, fg = (1, 1, 1, 1) )
		self.sonatu_ap_text = OnscreenText( text= "AP: " + str(self.sonatu.getAP()), pos = (-.5, -.8, 0), scale = 0.05, fg = (1, 1, 1, 1) )
		self.attack_type_text = OnscreenText( text= "", pos = (0, .8, 0), scale = 0.06, fg = (1, 1, 1, 1) )
		self.game_over_text = OnscreenText( text= "", pos = (0, 0, 0), scale = 0.1, fg = (1, 1, 1, 1), align = TextNode.ACenter )
		self.game_win_text = OnscreenText( scale = 0.1, fg = (1, 1, 1, 1), align = TextNode.ACenter)
		self.turn_text.reparentTo(render2d)
		self.sonatu_health_text.reparentTo(render2d)
		self.sonatu_ap_text.reparentTo(render2d)
		self.attack_type_text.reparentTo(render2d)
		self.game_over_text.reparentTo(render2d)
		self.game_win_text.reparentTo(render2d)

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
		self.camera.setPos(50.732, -130.826, 112.665)
		self.camera.setHpr(32.99, 0.875, -0.152)
		return Task.cont

	def limbo_camera_task_michael(self, task):
		self.camera.setPos(22.742, -64.037, 108.925)
		self.camera.lookAt(22.742, -64.037, 108.925)
		return Task.cont

	def limbo_camera_task_farthing(self, task):
		self.camera.setPos(-138.687, 62.531, 127.466)
		self.camera.lookAt(-138.687, 62.531, 127.466)		
		self.camera.setHpr(75, 5, 0)
		return Task.cont
	
	def limbo_camera_task_ivan(self, task):
		self.camera.setPos(-41.456, -13.393, 100.245)
		self.camera.lookAt(-41.456, -13.393, 100.245)		
		return Task.cont

	def limbo_camera_task_checkers(self, task):
		self.camera.setPos(-54.347, -52.173, 103.392)
		self.camera.lookAt(-54.347, -52.173, 103.392)		
		return Task.cont

	def collision_detection(self):
		self.traverser = CollisionTraverser()
		self.handler = CollisionHandlerQueue()
		self.collision_node = CollisionNode( "mouse_ray")
		self.collision_camera = self.camera.attachNewNode(self.collision_node)
		self.collision_node.setFromCollideMask(BitMask32.bit(1))
		self.collision_ray = CollisionRay()
		self.collision_node.addSolid(self.collision_ray)
		self.traverser.addCollider(self.collision_camera, self.handler)
	
	def set_sonatu_end_turn(self, turn):
		self.sonatu_end_turn = turn
	
	def end_turn_task(self, task):
		if self.sonatu_end_turn:
			self.sonatu_end_turn = False
               	        self.sonatu.end_turn()
			self.begin_enemy_turn()
		        #elf.__player_turn = False
		       
		return Task.cont
	

game = PIRATES()
game.run()
