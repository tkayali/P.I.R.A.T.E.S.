from PUnit import Unit

class Sonatu(Unit):
	"""
	This class will serve to build Sonatu, the player's ship.
	This class inherits from Unit.
	"""

	__special = 0
	damage = 0
	accuracy = 0

	def __init__ (self, _x_pos=0, _y_pos=0, _z_pos=0, _model = None,
	special=0):
		Unit.__init__(self, 30, 3, _x_pos, _y_pos, _z_pos, 
		True, _model, True, 4)
		self.__special = special

	def get_special(self):
		return __special
	
	def set_special(self, special):
		self.__special = special

	def move(self):
		#HOLDER METHODS
		self._pos_x += 1
		self._pos_y += 1
		self._pos_z += 1
		self._AP -= 1
	
	def attack(self, range):
		if range == 1:
			damage = 10
			accuracy = .9

		elif range == 2:
			damage = 6
			accuracy = .85

		elif range < 5:
			damage = 4
			accuracy = .8

		else:
			#Do absolutely nothing
			return 1

		self._AP -= 2

		print "Damage: " + str(damage) + " Accuracy: " + str(accuracy)
		return 0
		
	def end_turn():
		self.AP = 3

	def to_string(self):
		Unit.to_string(self)
		print "Special: " + str(self.__special)
