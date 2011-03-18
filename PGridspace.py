class Gridspace:
    """
    This class contains information about an individual gridspace
    """
    __occupying_unit = None
    __occupiable = None
    
    def __init__(self, __occupying_unit = None, __occupiable = True):
        self.__occupying_unit = __occupying_unit
        self.__occupiable = __occupiable
        
    def get_occupying_unit(self):
        return self.__occupying_unit
    
    def set_occupying_unit(self, __occupying_unit):
        self.__occupying_unit = __occupying_unit
        
    def get_occupiable(self):
        return self.__occupiable
    
    def set_occupiable(self, __occupiable):
        self.__occupiable = __occupiable