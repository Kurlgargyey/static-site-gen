import unittest

from functions import *

class TestFunctions(unittest.TestCase):
	def test_markdown_to_blocks(self):
		markdown = (
		"# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item")
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# This is a heading",
			"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
			"* This is the first list item in a list block\n* This is a list item\n* This is another list item"
		])
	def test_block_extract_strips_ws(self):
		markdown = (
		"# This is a heading\n\n   This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item")
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# This is a heading",
			"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
			"* This is the first list item in a list block\n* This is a list item\n* This is another list item"
		])
	def test_block_extract_drops_empty_blocks(self):
		markdown = (
		"# This is a heading\n\n\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is the first list item in a list block\n* This is a list item\n* This is another list item")
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# This is a heading",
			"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
			"* This is the first list item in a list block\n* This is a list item\n* This is another list item"
		])
	def test_blocktypes(self):
		cases = {
		"heading": "# This is a heading",
		"heading": "### This is also a heading",
		"code": "```This is code```",
		"quote": ">This\n>is\n>a\n>multiline\n>quote",
		"unordered_list": "* These\n- are\n* items\n* in\n- an unordered list",
		"ordered_list": "1. This is a list\n2. With two items",
		"paragraph": "This is just an ordinary paragraph"
		}
		for case in cases.items():
			with self.subTest(block=case[1], type=case[0]):
				self.assertEqual(block_to_blocktype(case[1]), case[0])

	def test_multiple_newlines(self):
		markdown = "# Heading\n\n\nParagraph"
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# Heading",
			"Paragraph"
		])

	def test_preserve_internal_newlines(self):
		markdown = "# Heading\n\n* Item 1\n* Item 2\n* Item 3"
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# Heading",
			"* Item 1\n* Item 2\n* Item 3"
		])

	def test_empty_string(self):
		markdown = ""
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [])

	def test_only_whitespace(self):
		markdown = "    \n\n   \n"
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [])

	def test_trailing_newlines(self):
		markdown = "# Heading\n\nParagraph\n\n\n"
		blocks = markdown_to_blocks(markdown)
		self.assertEqual(blocks, [
			"# Heading",
			"Paragraph"
		])


class TestMarkdownConversion(unittest.TestCase):

	def test_single_heading(self):
		markdown = "# Heading 1"
		node = markdown_to_html_node(markdown)
		self.assertEqual(node.children[0].tag, "h1")
		self.assertEqual(node.children[0].children[0].value, "Heading 1")

	def test_multiple_headings(self):
		markdown = "## Heading 2\n\n### Heading 3"
		node = markdown_to_html_node(markdown)
		self.assertEqual(node.children[0].tag, "h2")
		self.assertEqual(node.children[0].children[0].value, "Heading 2")
		self.assertEqual(node.children[1].tag, "h3")
		self.assertEqual(node.children[1].children[0].value, "Heading 3")
		self.assertEqual(node.tag, "div")
		self.assertEqual(len(node.children), 2)

	def test_single_line_code_block(self):
		markdown = "```\nprint('Hello')\n```"
		node = markdown_to_html_node(markdown)
		self.assertEqual(node.children[0].tag, "pre")
		self.assertEqual(node.children[0].children[0].tag, "code")
		self.assertEqual(node.children[0].children[0].children[0].value, "print('Hello')")

	def test_multi_line_code_block(self):
		markdown = "```\ndef foo():\n    return 'bar'\n```"
		node = markdown_to_html_node(markdown)
		self.assertEqual(node.children[0].tag, "pre")
		self.assertEqual(node.children[0].children[0].tag, "code")
		self.assertEqual(node.children[0].children[0].children[0].value, "def foo():\n    return 'bar'")

	def test_empty_ordered_list(self):
		markdown = "1. \n2. "

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)
		self.assertEqual(html_node.children[0].tag, "ol")
		self.assertEqual(len(html_node.children[0].children), 2)
		self.assertEqual(html_node.children[0].children[0].children[0].value, "")
		self.assertEqual(html_node.children[0].children[1].children[0].value, "")

	def test_non_sequential_ordered_list(self):
		markdown = "3. Item three\n5. Item five"

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)
		self.assertEqual(html_node.children[0].tag, "ol")
		self.assertEqual(html_node.children[0].children[0].children[0].value, "Item three")
		self.assertEqual(html_node.children[0].children[1].children[0].value, "Item five")

	def test_mixed_symbols_unordered_list(self):
		markdown = "- First item\n* Second item\n+ Third item"

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)
		self.assertEqual(html_node.children[0].tag, "ul")
		self.assertEqual(html_node.children[0].children[0].children[0].value, "First item")
		self.assertEqual(html_node.children[0].children[1].children[0].value, "Second item")
		self.assertEqual(html_node.children[0].children[2].children[0].value, "Third item")

	def test_unordered_list_with_empty_items(self):
		markdown = "- \n* Second item\n+ "

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)  # One parent UL node
		self.assertEqual(html_node.children[0].tag, "ul")

		self.assertEqual(len(html_node.children[0].children), 3)  # Three list items
		self.assertEqual(html_node.children[0].children[0].children[0].value, "")  # First item is empty
		self.assertEqual(html_node.children[0].children[1].children[0].value, "Second item")  # Second item has text
		self.assertEqual(html_node.children[0].children[2].children[0].value, "")  # Third item is empty

	def test_basic_paragraph(self):
		markdown = "This is a simple paragraph."

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)  # One parent div node
		self.assertEqual(html_node.children[0].tag, "p")  # Paragraph tag
		self.assertEqual(html_node.children[0].children[0].value, "This is a simple paragraph.")

	def test_empty_paragraph(self):
		markdown = ""

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 0)  # No children as there's no content

	def test_multiple_consecutive_paragraphs(self):
		markdown = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 3)  # Three paragraph nodes
		self.assertEqual(html_node.children[0].tag, "p")
		self.assertEqual(html_node.children[0].children[0].value, "First paragraph.")
		self.assertEqual(html_node.children[1].children[0].value, "Second paragraph.")
		self.assertEqual(html_node.children[2].children[0].value, "Third paragraph.")

	def test_paragraph_with_line_breaks(self):
		markdown = "This is a paragraph\nwith a line break."

		html_node = markdown_to_html_node(markdown)

		self.assertEqual(len(html_node.children), 1)  # One paragraph despite the line break
		self.assertEqual(html_node.children[0].tag, "p")
		self.assertEqual(html_node.children[0].children[0].value, "This is a paragraph\nwith a line break.")

class TestHeaderExtraction(unittest.TestCase):
	def test_standard_case(self):
		markdown = "# This is a heading"

		heading = extract_title(markdown)

		self.assertEqual(heading, "This is a heading")

	def test_multiple_headings(self):
		markdown = "# This is a heading\n\n# This, too is a heading"

		heading = extract_title(markdown)

		self.assertEqual(heading, "This is a heading")

if __name__ == "__main__":
	unittest.main()