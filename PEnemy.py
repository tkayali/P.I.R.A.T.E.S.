from PUnit import Unit

class Enemy(Unit):
	"""
	This class will serve to build an enemy.
	This class inherits from Unit.
	"""
	
	__damage = 0
	__accuracy = 0
	__gridspace = None
	__name = None

	def __init__ (self, gridspace=0, _unit_range=0):
		Unit.__init__(self, 10, 2, gridspace, True, False, _unit_range)
		self.__gridspace = gridspace

		if _unit_range == 1:
			self.__damage = 8
			self.__accuracy = .90
			self.__name = "Melee"

		elif _unit_range == 2:
			self.__damage = 5
			self.__accuracy = .85
			self.__name = "Short"

		elif _unit_range == 4:
			self.__damage = 3
			self.__accuracy = .80
			self.__name = "Long"

		else:
			print "WHAT THE HECK ARE YOU DOING?!"
			print "THIS IS TOTES AN INVALID RANGE!!"
	
	def end_turn(self):
		Unit.setAP(self, 2)

	def get_name(self):
		return self.__name
	
	def get_damage(self):
		return self.__damage
	
	def to_string(self):
		Unit.to_string(self)
