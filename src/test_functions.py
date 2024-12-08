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
        markdown = "## Heading 2\n### Heading 3"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "h2")
        self.assertEqual(node.children[0].children[0].value, "Heading 2")
        self.assertEqual(node.children[1].tag, "h3")
        self.assertEqual(node.children[1].children[0].value, "Heading 3")

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


if __name__ == "__main__":
    unittest.main()