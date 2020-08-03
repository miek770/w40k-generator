from enum import Enum


class Unit(Enum):
    HQ = 0
    Troop = 1
    Elite = 2
    Fast_Attack = 3
    Heavy_Support = 4
    Flyer = 5
    Dedicated_Transport = 6
    Lord_of_war = 7
    Fortification = 8


class Patrol_Composition(Enum):
    HQ = (1, 2)
    Troop = (1, 3)
    Elite = (0, 2)
    Fast_Attack = (0, 2)
    Heavy_Support  = (0, 2)
    Flyer = (0, 2)


class Detachments(Enum):
    Patrol = Patrol_Composition
