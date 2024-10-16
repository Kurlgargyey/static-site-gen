import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

	def test_parent_rejects_value(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", value="blabla", children=[test_leaf])
		self.assertTrue(test_parent.value is None)

	def test_parent_needs_children_len(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", value="blabla", children=[])
		self.assertRaises

	def test_parent_needs_children_some(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", value="blabla")
		self.assertRaises

	def test_parent_to_html(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", children=[test_leaf])
		self.assertEqual(test_parent.to_html(), "<p><a href=\"lololol\" target=\"_blank\">A link</a></p>")

	def test_nested_parents(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", children=[test_leaf])
		test_super_parent=(ParentNode("p", children=[test_parent]))
		self.assertEqual(test_super_parent.to_html(), "<p><p><a href=\"lololol\" target=\"_blank\">A link</a></p></p>")

	def test_multiple_children(self):
		test_leaf = LeafNode("a", "A link", [], {"href": "lololol", "target":"_blank"})
		test_parent = ParentNode("p", children=[test_leaf])
		test_super_parent=(ParentNode("p", children=[test_parent, test_leaf, test_leaf, test_parent]))
		self.assertEqual(test_super_parent.to_html(), "<p><p><a href=\"lololol\" target=\"_blank\">A link</a></p><a href=\"lololol\" target=\"_blank\">A link</a><a href=\"lololol\" target=\"_blank\">A link</a><p><a href=\"lololol\" target=\"_blank\">A link</a></p></p>")


if __name__ == "__main__":
	unittest.main()