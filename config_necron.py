from composition import Detachments

default = {
    "name": None,
    "qty": 0,
    "painted": False,
}

models = []

faction = "necron"
army_size = 500
margin = 0
detachment = Detachments.Patrol

# model = (quantity [int], painted [bool])
overlord = default.copy()
overlord["name"] = "Overlord"
overlord["qty"] = 1
overlord["painted"] = True
models.append(overlord)

destroyer_lord = default.copy()
destroyer_lord["name"] = "Destroyer Lord"
destroyer_lord["qty"] = 1
destroyer_lord["painted"] = True
models.append(destroyer_lord)

warrior = default.copy()
warrior["name"] = "Warrior"
warrior["qty"] = 40
models.append(warrior)

destroyer = default.copy()
destroyer["name"] = "Destroyer"
destroyer["qty"] = 6
destroyer["painted"] = True
models.append(destroyer)
