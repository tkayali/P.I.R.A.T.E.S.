from PUnit import Unit

class Sonatu(Unit):
	"""
	This class will serve to build Sonatu, the player's ship.
	This class inherits from Unit.
	"""

	__special = 0

	def __init__ (self, gridspace=94, special=0):
		Unit.__init__(self, 30, 3, gridspace, True, True, 4)
		self.__special = special

	def get_special(self):
		return __special
	
	def set_special(self, special):
		self.__special = special

	def end_turn(self):
		Unit.setAP(self, 3)

	def to_string(self):
		Unit.to_string(self)
		print "Special: " + str(self.__special)
