# W40k Army List Generator

This is a pet project whose purpose is to generate valid random lists per Warhammer 40,000's 9th edition. It currently supports:

* Necrons (other factions can be added);
* Single patrol detachment per list.

## Development status

This was only intended to be a fun project for my summer vacation. It works, but I don't expect to continue development unless others appear interested. If I do, I would start by restructuring the code in an object oriented style; the code is getting a bit confusing and I like to encapsulate my variables and functions in classes.

I would also like to make it easier to configure a collection. It doesn't really matter if the codices definition are in Python and thus somewhat complex to write for non-coders, but the collection should ideally be a simple configuration. The relevant class should thus have a parser to handle configuration file interpretation, and should work for any faction.

## Potential improvement

* Roll unit type before rolling unit, to better represent sparse categories (ex.: Dedicated Transport);
* Add more optional preferences, ex.: max units, prioritise painted models, identify proxies, etc.
