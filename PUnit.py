class Unit:
	"""
	THIS IS A TEST STRING
	This class will act as a generalied Unit template.
	This class also supports 3 sub-classes:
		class: Sonatu
		class: Enemy
		class: Queen
	"""

	_HP = 0
	_AP = 0
	_pos_x = 0
	_pos_y = 0
	_pos_z = 0
	_alive = False
	_model = None
	_player = False
	_unit_range = 0

	def __init__ (self, _HP=0, _AP=0, _pos_x=0, _pos_y=0, _pos_z=0,
	_alive=False, _model=None, _player=False, _unit_range=0):
		self._HP = _HP
		self._AP = _AP
		self._pos_x = _pos_x
		self._pos_y = _pos_y
		self._pos_z = _pos_z
		self._alive = _alive
		self._unit_range = _unit_range
		self._model = _model
		self._player = _player

	def to_string(self):
		print "HP: " + str(self._HP) + " AP: " + str(self._AP) + " Model: " + str(self._model) + "\nX Position: " + str(self._pos_x) + " Y Position: " + str(self._pos_y) + " Z Position: " + str(self._pos_z) + "\nIs the unit the player's? " + str(self._player) + "\nIs the unit alive? " + str(self._alive)
