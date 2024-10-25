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
		heading = "# This is a heading"
		code = "```This is code```"
		quote = ">This\n>is\n>a\n>multiline\n>quote"
		ul = "*These\n-are\n*items\n*in\n-an unordered list"
		li = "1. This is a list\n2. With two items"
		p = "This is just an ordinary paragraph"
		self.assertEqual(block_to_blocktype(heading), "heading")
		self.assertEqual(block_to_blocktype(code), "code")
		self.assertEqual(block_to_blocktype(quote), "quote")
		self.assertEqual(block_to_blocktype(ul), "unordered_list")
		self.assertEqual(block_to_blocktype(li), "ordered_list")
		self.assertEqual(block_to_blocktype(p), "paragraph")