# W40k Army List Generator

Are you:

* Tired of your winning streak?
* Interested in trying combinations you haven't even thought of?
* Looking for non-optimized lists to introduce new players?

If so, then you might be interested in this library! This is a pet project whose purpose is to randomly generate valid lists for Warhammer 40,000's 9th edition, based on your personal model collection. It currently supports:

* Necrons (other factions can be added with ease - see [Codex](#codex));
* Single patrol detachment per list (other detachment types can be added with ease - see [Detachments](#detachments); more than one detachment per list would require some code modification);
* Flexible unit limits for dedicated transports and other special cases (ex.: Necron Cryptothralls) - see [Codex](#codex).

## Content

- [W40k Army List Generator](#w40k-army-list-generator)
  - [Content](#content)
  - [Under development](#under-development)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Configuration](#configuration)
    - [List generation](#list-generation)
  - [Codex](#codex)
  - [Detachments](#detachments)
  - [Philosophy](#philosophy)
  - [Contributing](#contributing)

## Under development

* Add named characters to the Necron codex;
* Add more optional preferences (ex.: max units, prioritise painted models, custom percentages, etc.);
* Add `proxy` and `proxied_from` options to the models configuration (and handle those options);
* Handle bad configuration (ex.: wrong unit name);
* Use `click` to parse arguments.

## Installation

No **PyPI** package has been developped yet, so installation must be made from source. You might want to create a virtual environment, but the steps below assume you don't:

    git clone *URL*
    cd w40k-generator
    pip install -r requirements.txt

## Usage

That will change when `click` is integrated, but for now the faction is hardcoded to the Necrons in `main.py`.

### Configuration

Your personal collection for a specific faction must be configured in the `config_<faction>.py` file. For example, `config_necron.py` contains my personal collection. This file is a **Python** file structured thusly:

* **General configuration**: Typical for any faction, could be replaced with a single import, but I find it useful to have the defaults shown on top of the file (as a reminder).

```
from codex import Detachments, Factions

default = {
    "name": None,
    "qty": 1,
    "painted": False,
}

models = []
```

> The `painted` option currently has no impact whatsoever.

* **Army generation options**: Those define what type of army will be generated when using this faction (i.e.: this configuration file).

```
faction = Factions.Necron
army_size = 2000
margin = 0
detachment = Detachments.Patrol
msu = False
```

* **Model configuration**: At least one of these is required per model type in your collection. This is a dictionary based on the defaults (see **General configuration** above); only the keys that differ need to be overwritten. For example, leave `model["qty"] = 1` out if that's the case for this unit; it already defaults to `1`.

  Other options are expected to be added later, such as `model["proxy"]` and `model["proxied_from"]`.

```
model = default.copy()
model["name"] = "Catacomb Command Barge"
model["qty"] = 2
models.append(model)
```

### List generation

For now (until `click` is integarted), usage is quite straightforward:

    python3 main.py

As mentioned above, the faction is currently hardcoded to the Necrons. The output should thus look something like this:

    michel@galliumos ~/g/w/w40k-generator> python3 main.py
    Between 1 and 2 HQ are required in a Patrol detachment.
     * Choosing a HQ unit of at most 500 points...
     * Adding 1 Plasmancer to the army list.
    Between 1 and 3 Troop are required in a Patrol detachment.
     * Choosing a Troop unit of at most 420 points...
     * Adding 10 Warrior to the army list.
    Current army size: 200 / 500
     * Choosing a unit type with at least 1 available unit of at most 300 points...
     * Choosing a HQ unit of at most 300 points...
     * Adding 1 Royal Warden to the army list.
    Current army size: 280 / 500
     * Choosing a unit type with at least 1 available unit of at most 220 points...
     * Choosing a Flyer unit of at most 220 points...
     * Adding 1 Doom Scythe to the army list.
    Current army size: 450 / 500
     * Choosing a unit type with at least 1 available unit of at most 50 points...
     * Choosing a Heavy_Support unit of at most 50 points...
     * Adding 1 Heavy Destroyer to the army list.
    Current army size: 490 / 500
    The smallest remaining unit is bigger than the remaining points.

    Flyer:
     - 1 Doom Scythe (170 pts)
    HQ:
     - 1 Plasmancer (80 pts)
     - 1 Royal Warden (80 pts)
    Heavy_Support:
     - 1 Heavy Destroyer (40 pts)
    Troop:
     - 10 Warrior (120 pts)

    Total: 490

Feel free to run the script a few times until you get a list that sounds good enough for your purpose.

## Codex

The units definition for a specific faction must be configured in the `codex_<faction>.py` file. Other factions can be added by creating the relevant file and integrating it in a few other places:

* `army.py`: The codex needs to be added to the imports and to the class `Army`'s initiation;
* `codex.py`: The codex needs to be added to the imports, to the `Enum` class `Faction` and to the class `Codex`'s initiation;
* `collection.py`: The codex needs to be added to the imports and to the class `Collection`'s initiation;
* `main.py`: The faction-specific codex isn't actually referenced here, but the Necron faction is currently hardcoded in this file.

> Your personal collection must also be configured in a `config_<faction>.py` file for this codex to be used in an army list generation.

For example, `codex_necron.py` contains all Necron units, except the named characters (should be added soon). This file is a **Python** file structured thusly:

* **General configuration**: Typical for any faction, could be replaced with a single import, but I find it useful to have the defaults shown on top of the file (as a reminder).

```
from unit import Unit

default = {
    "name": None,
    "ppm": 0,
    "min": 1,
    "max": 1,
    "cat": Unit.HQ,
    "units": None,
}

codex = []
```

* **Unit configuration**: One of these is required per unit type in this faction. This is a dictionary based on the defaults (see **General configuration** above); only the keys that differ need to be overwritten. For example, leave `model["cat"] = Unit.HQ` out if that's the case for this unit; it already defaults to `Unit.HQ`.

  The `model["units"]` option is special; it is by default set to `None`, but setting it to a tuple of model names (ex.: `model["units"] = ("Warrior", )`) tells the program to allow up to one unit of the current model per unit of each of those other units. This is useful for dedicated transports and special cases such as the Necron Cryptothralls.

  The `model["ppm"]` option (points per model) is intended to match the cheapest options for this model; one might want to add margin in the configuration file to leave room for more expensive options, or set the `ppm` to the desired default directly in the faction codex file.

```
model = default.copy()
model["name"] = "Warrior"
model["ppm"] = 12
model["min"] = 10
model["max"] = 20
model["cat"] = Unit.Troop
codex.append(model)
```

## Detachments

The detachments definition are (perhaps awkwardly) located in the `codex.py` file. To add a new detachment, on must:

* `codex.py`: Create the `<Detachment>_Composition` dictionary with the relevant limits (all unit types must be defined here - even those unallowed or with no limit), and add the dictionary to the `Enum` class `Detachments`;
* `army.py`: Add the detachment to the class `Army`'s initiation.

> This detachment must also be configured in a `config_<faction>.py` file to be used in an army list generation.

## Philosophy

Well, *philosophy* might not be the right term, but here is how the library builds a list:

* Set your `codex`, `collection` and `army` up based on the relevant configuration;
* Meet the detachment's minimum requirements (ex.: for a patrol detachment, add an HQ and a troop);
* Until either the army is full or there is no valid unit remaining:
  * Roll a ***valid*** unit type from your collection;
  * Roll a ***valid*** unit of that type;
  * Add that unit to your army, and remove the models from your collection:
    * If `msu` is enforced (i.e.: set to `True` in the configuration file), add/remove the minimum amount of models to form this unit;
    * Otherwise, add/remove the minimum amount 50% of the time, and add/remove a random amount between the minimum and either the maximum or the remaining models the rest of the time.

The term ***valid*** is a bit vague, but the relevant checks are performed. For a unit:

* Are there sufficient models to build a `msu` (minimum size unit)?
* Does the `msu` cost less than the remaining points?

> The cheapest options are intented to be entered in each faction codex file; one might want to add margin in the configuration file to leave room for more expensive options, or set the `ppm` (points per model) to the desired default directly in the faction codex file.

For a unit type:

* Are all slots for this unit type in this detachment already taken?
* Is there at least one valid unit remaining in this unit type?

## Contributing

All contributions are welcome. I don't intend to support any other codex than the Necrons', but others are more than welcome to jump in and I'll help integrate it to the library if required.
