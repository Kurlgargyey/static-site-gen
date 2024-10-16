import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD, url = "dummy")
		node2 = TextNode("This is a text node", TextType.BOLD, url = "dummy")
		self.assertEqual(node, node2)

	def test_text_types(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		node = TextNode("This is a text node", TextType.BOLD)
		node = TextNode("This is a text node", TextType.ITALIC)
		node = TextNode("This is a text node", TextType.CODE)
		node = TextNode("This is a text node", TextType.LINK)
		node = TextNode("This is a text node", TextType.IMG)
		pass

	def test_ne_type(self):
		node = TextNode("This is a text node", TextType.IMG)
		node2 = TextNode("This is a text node", TextType.LINK)
		self.assertNotEqual(node, node2)

	def test_ne_content(self):
		node = TextNode("This is a text nodes", TextType.LINK)
		node2 = TextNode("This is a text node", TextType.LINK)
		self.assertNotEqual(node, node2)

	def test_ne_url(self):
		node = TextNode("This is a text node", TextType.LINK, url="lol")
		node2 = TextNode("This is a text node", TextType.LINK, url="lmao")
		self.assertNotEqual(node, node2)

	def test_repr(self):
		node = TextNode("This is a text node", TextType.LINK, url="lol")
		self.assertEqual(f"{node}", "TextNode(This is a text node, link, lol)")

	def test_repr(self):
		node = TextNode("This is a text node", TextType.LINK)
		self.assertEqual(f"{node}", "TextNode(This is a text node, link, None)")

if __name__ == "__main__":
	unittest.main()