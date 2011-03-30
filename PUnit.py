class Unit:
	"""
	This class will act as a generalied Unit template.
	This class also supports 3 sub-classes:
		class: Sonatu
		class: Enemy
		class: Queen
	"""

	_HP = 0
	_AP = 0
	__gridspace = None
	_alive = False
	_player = False
	_unit_range = 0

	def __init__ (self, _HP=0, _AP=0, gridspace=None, _alive=False, _player=False, _unit_range=0):
		self._HP = _HP
		self._AP = _AP
		self.__gridspace = gridspace
		self._alive = _alive
		self._unit_range = _unit_range
		self._player = _player
	
	def getAP(self):
		return self._AP
	
	def setAP(self, AP):
		self._AP = AP
	
	def getHP(self):
		return self._HP

	def setHP(self, HP):
		self._HP = HP
	
	def get_alive(self):
		return self._alive
	
	def set_alive(self, alive):
		self._alive = alive
	
	def get_unit_range(self):
		return _unit_range
	
	def set_unit_range(self, unit_range):
		self._unit_range = unit_range
	
	def get_player(self):
		return self._player
	
	def set_player(self, player):
		self._player = player
	
	def get_gridspace(self):
		return self.__gridspace

	def set_gridspace(self, gridspace):
		self.__gridspace = gridspace

	def to_string(self):
		print "HP: " + str(self._HP) + " AP: " + str(self._AP) + " Model: " + str(self._model) + "\nX Position: " + str(self._pos_x) + " Y Position: " + str(self._pos_y) + " Z Position: " + str(self._pos_z) + "\nIs the unit the player's? " + str(self._player) + "\nIs the unit alive? " + str(self._alive)
