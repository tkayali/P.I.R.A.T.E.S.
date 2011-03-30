from PUnit import Unit

class Enemy(Unit):
	"""
	This class will serve to build an enemy.
	This class inherits from Unit.
	"""
	
	__damage = 0
	__accuracy = 0
	__gridspace = None

	def __init__ (self, gridspace=94, _unit_range=0):
		Unit.__init__(self, 10, 2, gridspace, True, False, _unit_range)
		self.__gridspace = gridspace

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
	
	def begin_enemy_turn(self):
		print "HI"
	
	def end_turn(self):
		Unit.setAP(self, 2)
	
	def to_string(self):
		Unit.to_string(self)
