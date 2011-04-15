from PUnit import Unit

class Queen(Unit):
	"""
	This class will function as the sea monster queen's class.
	"""
	__damage = 0
	__accuracy = 0
	__name = "Queen"

	def __init__(self, gridspace=None, picture=None):
		Unit.__init__(self, 30, 2, gridspace, True, False, 4, picture)

	def set_attributes(self, range):
		if range == 1:
			self.__damage = 8
			self.__accuracy = 90

		elif range == 2:
			self.__damage = 4
			self.__accuracy = 85

		elif range < 5:
			self.__damage = 2
			self.__accuracy = 80

		else:
			print "What are you doing!?!?!?!\nYou should not see this!!!"

	def end_turn(self):
		Unit.setAP(self, 2)

	def get_damage(self):
		return self.__damage
	
	def set_damage(self, damage):
		self.__damage = damage
	
	def get_accuracy(self):
		return self.__accuracy
	
	def set_accuracy(self, accuracy):
		self.__accuracy = accuracy
	
	def get_name(self):
		return self.__name

