import unittest

from htmlnode import HTMLNode, LeafNode

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

	def test_leaf(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		self.assertTrue(test_leaf.children is None)

	def test_leaf_repr(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		self.assertEqual(f"{test_leaf}", "LeafNode(a, A link, {'href': 'lololol', 'target': '_blank'})")

	def test_leaf_needs_value(self):
		test_leaf = LeafNode(value= None)
		self.assertRaises(ValueError)

if __name__ == "__main__":
	unittest.main()