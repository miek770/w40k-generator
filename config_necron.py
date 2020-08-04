from codex import Detachments, Factions

default = {
    "name": None,
    "qty": 1,
    "painted": False,
}

models = []

#model = default.copy()
#model["name"] = ""
#model["qty"] =
#models.append(model)

faction = Factions.Necron
army_size = 2000
margin = 0
detachment = Detachments.Patrol
msu = False

# HQ

model = default.copy()
model["name"] = "Catacomb Command Barge"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Cryptek"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Destroyer Lord"
models.append(model)

model = default.copy()
model["name"] = "Lord"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Overlord"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Plasmancer"
models.append(model)

model = default.copy()
model["name"] = "Royal Warden"
models.append(model)

model = default.copy()
model["name"] = "Skorpekh Lord"
models.append(model)

# Troop

model = default.copy()
model["name"] = "Warrior"
model["qty"] = 40
models.append(model)

model = default.copy()
model["name"] = "Immortal"
model["qty"] = 30
models.append(model)

# Elite

model = default.copy()
model["name"] = "C'tan Shard of the Deceiver"
models.append(model)

model = default.copy()
model["name"] = "C'tan Shard of the Nightbringer"
models.append(model)

model = default.copy()
model["name"] = "Canoptek Reanimator"
models.append(model)

model = default.copy()
model["name"] = "Canoptek Tomb Stalker"
models.append(model)

model = default.copy()
model["name"] = "Cryptothrall"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Deathmark"
model["qty"] = 5
models.append(model)

model = default.copy()
model["name"] = "Flayed One"
model["qty"] = 40
models.append(model)

model = default.copy()
model["name"] = "Lychguard"
model["qty"] = 5
models.append(model)

model = default.copy()
model["name"] = "Skorpekh Destroyer"
model["qty"] = 3
models.append(model)

model = default.copy()
model["name"] = "Triarch Praetorian"
model["qty"] = 5
models.append(model)

model = default.copy()
model["name"] = "Triarch Stalker"
model["qty"] = 1
models.append(model)

# Fast Attack

model = default.copy()
model["name"] = "Canoptek Scarab Swarm"
model["qty"] = 12
models.append(model)

model = default.copy()
model["name"] = "Canoptek Tomb Sentinel"
models.append(model)

model = default.copy()
model["name"] = "Canoptek Wraith"
model["qty"] = 6
models.append(model)

model = default.copy()
model["name"] = "Destroyer"
model["qty"] = 6
models.append(model)

model = default.copy()
model["name"] = "Tomb Blade"
model["qty"] = 6
models.append(model)

# Heavy Support

model = default.copy()
model["name"] = "Annihilation Barge"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Doomsday Ark"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Heavy Destroyer"
model["qty"] = 6
models.append(model)

model = default.copy()
model["name"] = "Sentry Pylon"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Tesseract Ark"
model["qty"] = 3
models.append(model)

model = default.copy()
model["name"] = "Transcendent C'tan"
model["qty"] = 2
models.append(model)

# Flyer

model = default.copy()
model["name"] = "Doom Scythe"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Night Scythe"
model["qty"] = 2
models.append(model)

model = default.copy()
model["name"] = "Night Shroud"
model["qty"] = 2
models.append(model)

# Dedicated Transport

model = default.copy()
model["name"] = "Ghost Ark"
model["qty"] = 2
models.append(model)
