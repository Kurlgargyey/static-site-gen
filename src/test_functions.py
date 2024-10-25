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