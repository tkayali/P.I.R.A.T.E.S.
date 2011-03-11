from PUnit import Unit

class Queen(Unit):
	"""
	This class will function as the sea monster queen's class.
	"""

	def __init__(self, _model = None):
		Unit.__init__(self, 30, 3, 0, 0, 0, True, _model, False, 4)
	
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

	

