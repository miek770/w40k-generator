from enum import Enum


class Unit(Enum):
    HQ = 0
    Troop = 1
    Elite = 2
    Fast_Attack = 3
    Heavy_Support = 4
    Flyer = 5
    Dedicated_Transport = 6
    Lord_of_War = 7
    Fortification = 8
    Other = 9


class Verbose(Enum):
    Error = 0
    Info = 1
    Debug = 2
