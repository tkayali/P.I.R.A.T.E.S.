class CombatUI:
	"""
	This class will hold all the user interface elements of combat.
	"""
	__combat_info_box = None
	__unit_picture_box = None
	__combat_info_text = None
	__unit_name_text = None

	def __init__(self, __combat_info_box = None, __unit_picture_box = None,
	__combat_info_text = None, __unit_name_text = None):
		self.__combat_info_box = __combat_info_box
		self.__unit_picture_box = __unit_picture_box
		self.__combat_info_text = __combat_info_text
		self.__unit_name_text = __unit_name_text

	def get_combat_info_box(self):
		return self.__combat_info_box

	def set_combat_info_box(self, __combat_info_box):
		self.__combat_info_box = __combat_info_box

	def get_unit_picture_box(self):
		return self.__unit_picture_box
	
	def set_unit_picture_box(self, __unit_picture_box):
		self.__unit_picture_box = __unit_picture_box

	def get_combat_info_text(self):
		return self.__combat_info_text

	def set_combat_info_text(self, __combat_info_text):
		self.__combat_info_text = __combat_info_text

	def get_unit_name_text(self):
		return self.__unit_name_text

	def set_unit_name_text(self, __unit_name_text):
		self.__unit_name_text = __unit_name_text
