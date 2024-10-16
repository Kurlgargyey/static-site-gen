import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
	def test_fields(self):
		test_node = HTMLNode("a","A link",[],{"href": "lololol"})

	def test_props_to_html(self):
		test_node = HTMLNode("a","A link",[],{"href": "lololol", "target":"_blank"})
		self.assertEqual(test_node.props_to_html(), " href=\"lololol\" target=\"_blank\"")

	def test_repr(self):
		test_node = HTMLNode("a","A link",[],{"href": "lololol"})
		self.assertEqual(f"{test_node}", "HTMLNode(a, A link, [], {'href': 'lololol'})")

	def test_repr(self):
		test_node = HTMLNode("a","A link",[])
		self.assertEqual(f"{test_node}", "HTMLNode(a, A link, [], None)")
if __name__ == "__main__":
	unittest.main()