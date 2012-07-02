import xml.etree.ElementTree as etree
import platform
import os.path
import itertools
import collections

defaultdict = collections.defaultdict
SECONDARY_STATS = ["HITPOINTS", "SPELLPOINTS", "MELEE_POWER", "MAGIC_POWER",
"CRITICAL", "HAYWIRE", "DODGE", "BLOCK", "COUNTER", "ENEMY_DODGE_REDUCTION",
"ARMOR_ABSORPTION", "RESIST", "SNEAKINESS", "LIFE_REGEN", "MANA_REGEN",
"WAND_BURNOUT_REDUCTION", "TRAP_SENSE_LEVEL", "TRAP_SIGHT_RADIUS", "SIGHT_RADIUS",
"SMITHING", "TINKERING", "ALCHEMY", "MAGIC_REFLECT", "WANDCRAFTING"]

PRIMARY_STATS = ["BURLINESS", "SAGACITY", "NIMBLENESS", "CADDISHNESS", "STUBBORNNESS", "SAVVY"]

class _dredwrap(object):
	def __init__(self, fn):
		self.fn = fn
		
		mach = platform.machine()
		_os   = platform.system()

		if (mach == "AMD64"):
			if (_os == "Windows"):
				base_path = ("C:", "\Program Files (x86)", "steam\steamapps\common\dungeons of dredmor")

		elif (mach == "i386"):
			if (_os == "Windows"):
				base_path = ("C:", "\Program Files (x86)", "steam\steamapps\common\dungeons of dredmor")

		self.filename = {"crafts": "craftDB.xml",
			"monsters": "monDB.xml",
			"items": "itemDB.xml"}

		self.base_path = base_path

		# TODO: better handling of mods, alternate install paths
		# XXX the above could be done with variable keyword args
		self.fn.func_defaults = ("filename",
			os.path.join(*itertools.chain(base_path, ("game", self.filename[fn.func_name]),)))
	

	def __call__(self, **miscargs):
		# transform the default parameters before (re-)calling our decorated function
		
		# TODO: find a clean way of handling alternate steam install paths
		# TODO: handle Desura/<other> installs
		mod = None

		if (miscargs.has_key("mod")):
			if (type(miscargs["mod"]) is int):
				if (int(miscargs["mod"]) in (1,2)):
					# DLCs should be referred to by their release order
					# community mods are a different story...
					mod = "expansion{0}/game".format((miscargs["mod"] if miscargs["mod"] > 1 else ""))
		else:
			mod = "game"

		self.fn.func_defaults = ("filename",
			os.path.join(*itertools.chain(self.base_path, (mod, self.filename[self.fn.func_name]))))

		return self.fn()

@_dredwrap
def crafts(filename):
	crafts = etree.parse(filename)

	for craft in crafts.findall("craft"):
		_craft = defaultdict(list)

		for attrib in craft:
			# TODO: make crafts that have varying outputs have a list of names to access
			if (attrib.tag == "output"):
				_craft["output"].append(attrib.attrib)

			if (attrib.tag == "input"):
				_craft["ingredients"].append(attrib.attrib["name"])

			if (attrib.tag == "tool"):
				_craft["tool"] = attrib.attrib["tag"]

		yield _craft

@_dredwrap
def items(filename):
	items = etree.parse(filename)
	bufftypes = set(["primarybuff", "secondarybuff", "resistbuff", "damagebuff"])
	itemtypes = set(["food", "armour", "weapon"])

	for item in items.findall("item"):
		_item = defaultdict(dict)
		_item["name"] = item.attrib["name"]
		for attr in item:
			attrib = attr.attrib
			if (attr.tag in itemtypes):
				# the categorization of items is a bit inconsistent
				# armour has a subtype in the <armour> tag
				# weapons (and other items?) have it in the <item> tag
				if (attr.tag in ["armour", "weapon"]):
					_item["type"] = attr.tag
					# armour and weapon both have damage values
					# for resist and damage, respectively
					if (attr.tag == "weapon"):
						_item["damage"] = attrib

					elif (attr.tag == "armour"):
						_item["subtype"] = attrib["type"]

				elif (attr.tag == "food"):
					_item["subtype"] = attrib.get("meat", None)

			elif (attr.tag in bufftypes):
				if (attr.tag == "primarybuff"):
					_item[attr.tag][PRIMARY_STATS[int(attrib["id"])]] = attrib["amount"]

				elif (attr.tag == "secondarybuff"):
					_item[attr.tag][SECONDARY_STATS[int(attrib["id"])]] = attrib["amount"]

				elif (attr.tag in ["damagebuff", "resistbuff"]):
					_item[attr.tag].update(attrib)

			elif (attr.tag == "price"):
				_item[attr.tag] = int(attr.attrib["amount"])

			elif (attr.tag == "description"):
				_item[attr.tag] = attr.attrib["text"]

		yield _item

@_dredwrap
def monsters(filename):
	monsters = etree.parse(filename)
	datum = set(["ai", "onhit", "stats", "damage", "secondarybuff",
		"resistances", "info", "palette"])

	def monster(mon):
		# TODO: Figure out a way to recursively extract monster variants!
		for mob in mon: 
			monsterdata = {}
			for mobdata in mob:
				if (not monsterdata.has_key(mobdata.tag)):
					if (mobdata.tag in datum):
						monsterdata[mobdata.tag] = {}
				
				if (mobdata.tag in datum):
					monsterdata[mobdata.tag].update(mobdata.attrib)

			yield monsterdata

	return monster(monsters.findall("monster"))
