import unittest

from textnode import TextNode, TextType, split_nodes_delimiter
from htmlnode import LeafNode

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

	def test_text_to_html(self):
		node = TextNode("This is a text node", TextType.NORMAL)
		html_expected = LeafNode(value=node.text)
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_bold_to_html(self):
		node = TextNode("This is a text node", TextType.BOLD)
		html_expected = LeafNode(value=node.text, tag = "b")
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_ital_to_html(self):
		node = TextNode("This is a text node", TextType.ITALIC)
		html_expected = LeafNode(value=node.text, tag="i")
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_code_to_html(self):
		node = TextNode("This is a text node", TextType.CODE)
		html_expected = LeafNode(value=node.text, tag="code")
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_link_to_html(self):
		node = TextNode("This is a text node", TextType.LINK, url="url.url.com")
		html_expected = LeafNode(value=node.text, tag="a", props={"href":node.url})
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_img_to_html(self):
		node = TextNode("This is a text node", TextType.IMG, url="img.url.com")
		html_expected = LeafNode(value="", tag="img", props={"src": node.url, "alt": node.text})
		self.assertEqual(node.text_node_to_html_node(), html_expected)
	def test_links_require_url(self):
		node = TextNode("This is a text node", TextType.LINK)
		with self.assertRaises(ValueError):
			node.text_node_to_html_node()

	def test_images_require_url(self):
		node = TextNode("This is a text node", TextType.IMG)
		with self.assertRaises(ValueError):
			node.text_node_to_html_node()

	def test_basic_split(self):
		node = TextNode("This is a *text* node", TextType.NORMAL)
		splits = split_nodes_delimiter([node], "*", TextType.ITALIC)
		self.assertEqual(splits, [TextNode("This is a ", TextType.NORMAL), TextNode("text", TextType.ITALIC), TextNode(" node", TextType.NORMAL)])

	def test_raise_on_delim_mismatch(self):
		node = TextNode("This is a *text* node", TextType.NORMAL)
		with self.assertRaises(ValueError):
			split_nodes_delimiter([node], "**", TextType.ITALIC)

	def test_raise_on_odd_delim_count(self):
		node = TextNode("This is a *text** node", TextType.NORMAL)
		with self.assertRaises(Exception):
			split_nodes_delimiter([node], "*", TextType.ITALIC)


if __name__ == "__main__":
	unittest.main()