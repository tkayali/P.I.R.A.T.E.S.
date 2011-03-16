class Environment:
	"""
	This class will create the environment of the game.
	"""
	__visual_assets = []
	__sound_assets = []
	__dialogue_assets= []

	def __init__ (self, __visual_assets = [], __sound_assets = [],
	__dialogue_assets = [] ):
		self.__visual_assets = __visual_assets
		self.__sound_assets = __sound_assets
		self.__dialogue_assets = __dialogue_assets
		
	def to_string (self):
		print str(self.__visual_assets) + "\n" + str(self.__sound_assets) + "\n" + str(self.__dialogue_assets)
