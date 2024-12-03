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