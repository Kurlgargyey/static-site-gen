import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links, text_to_text_nodes
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

	def test_extract_image(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)
		images = extract_markdown_images(node.text)
		self.assertEqual(images, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

	def test_extract_images_does_not_extract_links(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
		links = extract_markdown_images(node.text)
		self.assertNotEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


	def test_extract_link(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)
		links = extract_markdown_links(node.text)
		self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

	def test_extract_link_does_not_extract_images(self):
		node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)
		images = extract_markdown_links(node.text)
		self.assertNotEqual(images, [('rick roll', 'https://i.imgur.com/aKaOqIh.gif'),('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')])

	def test_split_images(self):
		old_nodes = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.NORMAL)]
		new_nodes = split_nodes_images(old_nodes)
		self.assertEqual(new_nodes, [
			TextNode("This is text with a ", TextType.NORMAL, None),
  			TextNode("rick roll", TextType.IMG, "https://i.imgur.com/aKaOqIh.gif"),
  			TextNode(" and ", TextType.NORMAL, None),
  			TextNode("obi wan", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg")
  			])
	def test_split_links(self):
		old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.NORMAL)]
		new_nodes = split_nodes_links(old_nodes)
		self.assertEqual(new_nodes, [
			TextNode("This is text with a link ", TextType.NORMAL, None),
  			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
  			TextNode(" and ", TextType.NORMAL, None),
  			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
  			])

	def test_text_to_textnodes(self):
		text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		nodes = text_to_text_nodes(text)
		self.assertEqual(nodes, [TextNode("This is ", TextType.NORMAL, None),
  TextNode("text", TextType.BOLD, None),
  TextNode(" with an ", TextType.NORMAL, None),
  TextNode("italic", TextType.ITALIC, None),
  TextNode(" word and a ", TextType.NORMAL, None),
  TextNode("code block", TextType.CODE, None),
  TextNode(" and an ", TextType.NORMAL, None),
  TextNode("obi wan image", TextType.IMG, "https://i.imgur.com/fJRm4Vk.jpeg"),
  TextNode(" and a ", TextType.NORMAL, None),
  TextNode("link", TextType.LINK, "https://boot.dev")])

if __name__ == "__main__":
	unittest.main()