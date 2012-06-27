import xml.etree.ElementTree as etree

SECONDARY_STATS = ["HITPOINTS", "SPELLPOINTS", "MELEE_POWER", "MAGIC_POWER",
"CRITICAL", "HAYWIRE", "DODGE", "BLOCK", "COUNTER", "ENEMY_DODGE_REDUCTION",
"ARMOR_ABSORPTION", "RESIST", "SNEAKINESS", "LIFE_REGEN", "MANA_REGEN",
"WAND_BURNOUT_REDUCTION", "TRAP_SENSE_LEVEL", "TRAP_SIGHT_RADIUS", "SIGHT_RADIUS",
"SMITHING", "TINKERING", "ALCHEMY", "MAGIC_REFLECT", "WANDCRAFTING"]

PRIMARY_STATS = ["BURLINESS", "SAGACITY", "NIMBLENESS", "CADDISHNESS", "STUBBORNNESS", "SAVVY"]

def items(filename):
	items = etree.parse(filename)
	bufftypes = set(["primarybuff", "secondarybuff", "resistbuff", "damagebuff"])
	itemtypes = set(["food", "armour", "weapon"])

	for item in items.findall("item"):
		_item = {}

		for attr in item:
			attrib = attr.attrib
			if (attr.tag in itemtypes):
				if (attr.tag in ["armour", "weapon"]):
					_item["type"] = attr.tag
					# armour and weapon both have damage values
					# for resist and damage, respectively
					if (attr.tag == "weapon"):
						_item["damage"] = attrib

					if (attr.tag == "armour"):
						_item["subtype"] = attrib["type"]

			if (attr.tag in bufftypes):
				if (not _item.has_key(attr.tag)):
					_item[attr.tag] = {}

				if (attr.tag == "primarybuff"):
					_item[attr.tag][PRIMARY_STATS[int(attrib["id"])]] = attrib["amount"]

				if (attr.tag == "secondarybuff"):
					_item[attr.tag][SECONDARY_STATS[int(attrib["id"])]] = attrib["amount"]

				if (attr.tag in ["damagebuff", "resistbuff"]):
					_item[attr.tag].update(attrib)

			if (attr.tag == "price"):
				_item[attr.tag] = int(attr.attrib["amount"])

			if (attr.tag == "description"):
				_item[attr.tag] = attr.attrib["text"]

		yield _item
