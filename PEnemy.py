from PUnit import Unit

class Enemy(Unit):
	"""
	This class will serve to build an enemy.
	This class inherits from Unit.
	"""
	
	__damage = 0
	__accuracy = 0

	def __init__ (self, _pos_x=0, _pos_y=0, _pos_z=0, _unit_range=0,
		_model=None):
		Unit.__init__(self, 10, 2, _pos_x, _pos_y, _pos_z, True, _model,
		False, _unit_range)

		if range == 1:
			__damage = 8
			__accuracy = .90

		elif range == 2:
			__damage = 5
			__accuracy = .85

		elif range < 5:
			__damage = 3
			__accuracy = .80

		else:
			__damage = 0
			__accuracy = 0

	def move(self):
		#HOLDER METHODS
		self._pos_x += 1
		self._pos_y += 1
		self._pos_z += 1
		self._AP -= 1

	def to_string(self):
		Unit.to_string(self)



