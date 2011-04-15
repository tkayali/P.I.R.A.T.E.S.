from PUnit import Unit

class Queen(Unit):
	"""
	This class will function as the sea monster queen's class.
	"""
	__damage = 0
	__accuracy = 0

	def __init__(self):
		Unit.__init__(self, 30, 2, None, True, False, 4)

	def set_attributes(self, range):
		if range == 1:
			self.__damage = 10
			self.__accuracy = 90

		elif range == 2:
			self.__damage = 6
			self.__accuracy = 85

		elif range < 5:
			self.__damage = 4
			self.__accuracy = 80

		else:
			print "What are you doing!?!?!?!\nYou should not see this!!!"

		#Unit.setAP(self, Unit.getAp()-1)

		print "Damage: " + str(damage) + " Accuracy: " + str(accuracy)

	def end_turn():
		Unit.setAP(self, 2)

	def get_damage(self):
		return self.__damage
	
	def set_damage(self, damage):
		self.__damage = damage
	
	def get_accuracy(self):
		return self.__accuracy
	
	def set_accuracy(self, accuracy):
		self.__accuracy = accuracy

