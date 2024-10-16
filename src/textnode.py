from enum import Enum

class TextType(Enum):
	NORMAL = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMG = "img"

class TextNode:
	def __init__(self, content, type, url = None):
		self.text = content
		self.type = type.value
		self.url = url

	def __eq__(self, other):
		return (self.text == other.text
		and self.type == other.type
		and self.url == other.url)

	def __repr__(self):
		return f"TextNode({self.text}, {self.type}, {self.url})"