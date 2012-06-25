import xml.parsers.expat

SECONDARY_STATS = ["HITPOINTS", "SPELLPOINTS", "MELEE_POWER", "MAGIC_POWER",
"CRITICAL", "HAYWIRE", "DODGE", "BLOCK", "COUNTER", "ENEMY_DODGE_REDUCTION",
"ARMOR_ABSORPTION", "RESIST", "SNEAKINESS", "LIFE_REGEN", "MANA_REGEN",
"WAND_BURNOUT_REDUCTION", "TRAP_SENSE_LEVEL", "TRAP_SIGHT_RADIUS", "SIGHT_RADIUS",
"SMITHING", "TINKERING", "ALCHEMY", "MAGIC_REFLECT", "WANDCRAFTING"]

PRIMARY_STATS = ["BURLINESS", "SAGACITY", "NIMBLENESS", "CADDISHNESS", "STUBBORNNESS", "SAVVY"]
items = {}
	
itemStateName = ""

def start_element(name, attrs):
	global itemStateName
	
	if (name == "item"):
		itemStateName = attrs["name"]
		items[itemStateName] = {}

	if (name in ["primarybuff", "secondarybuff", "resistbuff"]):
		if (not items[itemStateName].has_key(name)):
			items[itemStateName][name] = []

		if (name == "secondarybuff"):
			items[itemStateName][name].append(
				{ SECONDARY_STATS[ int(attrs["id"]) ]: int(attrs["amount"]),
					"STAT_ID": int(attrs["id"])})

		elif (name == "primarybuff"):
			items[itemStateName][name].append(
				{ PRIMARY_STATS[ int(attrs["id"]) ]: int(attrs["amount"]),
					"STAT_ID": int(attrs["id"])})

		elif (name == "damagebuff"):
			if (not items[itemStateName].has_key("damagebuff")):
				items[itemStateName]["damagebuff"] = {}

			items[itemStateName]["damagebuff"].update(attrs)

		elif (name == "resistbuff"):
			if (not items[itemStateName].has_key("resists")):
				items[itemStateName]["resists"] = {}

			items[itemStateName]["resists"].update(attrs)

	if (name == "price"):
		items[itemStateName]["price"] = int(attrs["amount"])
	
	if (name in ["armour", "food", "weapon"]):
		items[itemStateName]["type"] = name

		if (name in ["armour", "weapon"]):
			if (not items[itemStateName].has_key("damage")):
				items[itemStateName]["damage"] = {}

			items[itemStateName]["damage"].update(attrs)

	if ("level" in attrs and name == "item"):
		items[itemStateName]["quality"] = int(attrs["level"])

	if (name == "description"):
		items[itemStateName]["description"] = attrs["text"]

def end_element(name):
	global itemStateName
	if (name == "item"):
		itemStateName = ""

def load_items(modid=0):
	if (modid == 0):
		itemParser = xml.parsers.expat.ParserCreate()
		itemParser.StartElementHandler = start_element
		itemParser.EndElementHandler = end_element
		itemParser.ParseFile(open("C:\Program Files (x86)\Steam\Steamapps\common\dungeons of dredmor\game\itemDB.xml", "r"))
