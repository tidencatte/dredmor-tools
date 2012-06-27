import xml.etree.ElementTree as etree

def items(filename):
	items = etree.parse(filename)
	bufftypes = set(["primarybuff", "secondarybuff", "resistbuff", "damagebuff"])

	for item in items.findall("item"):
		_item = {}

		for attr in item:
			if (attr.tag in bufftypes):
				_item[attr.tag] = {}

			if (attr.tag in bufftypes):
				_item[attr.tag].update(attr.attrib)

			if (attr.tag == "price"):
				_item[attr.tag] = int(attr.attrib["amount"])

			if (attr.tag == "description"):
				_item[attr.tag] = attr.attrib["text"]

		yield _item
