from PUnit import Unit
from PSonatu import Sonatu
from PEnemy import Enemy
from PQueen import Queen
from PCombatUI import CombatUI
from PEnvironment import Environment
from PMap import Map

#print Unit.__doc__
#print Sonatu.__doc__
#print Enemy.__doc__

#unit = Unit()
#unit.to_string()
#print "\n"
#unit2 = Unit(8,50,123,125,-1,True,None,True,98)
#unit2.to_string()

#player = Sonatu(None, 0)
#melee = Enemy(0, 0, 0, 1, None)
#queen = Queen(None)

#player = Sonatu(0, 0, 0, None, 0)
#print player.__doc__

#combatui = CombatUI()
#print combatui.get_combat_info_box()
#combatui2 = CombatUI("Hi", None, None, None)
#print combatui2.get_combat_info_box()

#player.move()
#player.attack(3)
#player.to_string()

#melee.move()
#melee.to_string()

#queen.to_string()
#queen.move()
#queen.to_string()

#environment = Environment([1,0,0], [0,1,0], [0,0,1])
#environment2 = Environment()

#print environment.__doc__
#print environment.to_string()

map = Map()
map.get_gridspaces()[5][5]=1
print map.calculate_path(5,4,5,6)

