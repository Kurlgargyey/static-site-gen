import re
from enum import Enum
from itertools import cycle
from htmlnode import LeafNode, ParentNode

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

	def text_node_to_html_node(self):
		match TextType(self.type):
			case TextType.NORMAL:
				return LeafNode(value=self.text)
			case TextType.BOLD:
				return LeafNode(tag="b", value=self.text)
			case TextType.ITALIC:
				return LeafNode(tag="i", value=self.text)
			case TextType.CODE:
				return LeafNode(tag="code", value=self.text)
			case TextType.LINK:
				if self.url is None or len(self.url) == 0:
					raise ValueError("links should have an associated url")
				return LeafNode(tag="a", value=self.text, props={"href": self.url})
			case TextType.IMG:
				if self.url is None or len(self.url) == 0:
					raise ValueError("images should have an associated url")
				return LeafNode(tag="img", value="", props={"src": self.url, "alt": self.text})
			case _:
				raise Exception("texttype should be known")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	nodes = []
	if not [delimiter, text_type] in [
		["*", TextType.ITALIC],
		["**", TextType.BOLD],
		["`", TextType.CODE],
	]:
		raise ValueError("delimiter should match text type")
	for node in old_nodes:
		if node.text.count(delimiter)%2 != 0:
			raise Exception("invalid markdown syntax")
		if TextType(node.type) != TextType.NORMAL:
			nodes.append(node)
			continue
		split = node.text.split(delimiter)
		type_cycle = cycle([TextType.NORMAL, text_type])
		def map_leaf(text):
			return TextNode(content=text, type=next(type_cycle))
		nodes.extend(map(map_leaf, split))
	return nodes

def extract_regex(regex, text):
	matches = regex.findall(text)
	result = []
	result.extend(map(lambda match: (match[0], match[1]),matches))
	return result
IMAGE_REGEX = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
def extract_markdown_images(text):
	return extract_regex(IMAGE_REGEX, text)
LINK_REGEX = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
def extract_markdown_links(text):
	return extract_regex(LINK_REGEX, text)

def split_nodes_regex(old_nodes, regex):
	delim = "<-split->"
	type = (lambda regex: TextType.IMG if regex == IMAGE_REGEX else TextType.LINK)(regex)
	nodes = []
	for node in old_nodes:
		if TextType(node.type) != TextType.NORMAL:
			nodes.append(node)
			continue
		ressources = extract_regex(regex, node.text)
		splitter_text = re.sub(regex, delim, node.text)
		split = re.split(delim, splitter_text)
		ressource_nodes = list(map(lambda image: TextNode(content=image[0], type= type, url=image[1]), ressources))
		text_nodes = list(map(lambda text: TextNode(content=text, type=TextType.NORMAL), filter(None,split)))
		result = ressource_nodes + text_nodes
		match regex.match(node.text):
			case None:
				result[::2] = text_nodes
				result[1::2] = ressource_nodes
				nodes.extend(result)
			case _:
				result[::2] = ressource_nodes
				result[1::2] = text_nodes
				nodes.extend(result)

	return nodes
def split_nodes_images(old_nodes):
	return split_nodes_regex(old_nodes, IMAGE_REGEX)
def split_nodes_links(old_nodes):
	return split_nodes_regex(old_nodes, LINK_REGEX)

def text_to_text_nodes(text):
	old_nodes = [TextNode(content=text, type=TextType.NORMAL)]
	bold_nodes = split_nodes_delimiter(old_nodes, delimiter="**", text_type=TextType.BOLD)
	italic_nodes = split_nodes_delimiter(bold_nodes, delimiter="*", text_type=TextType.ITALIC)
	code_nodes = split_nodes_delimiter(italic_nodes, delimiter="`", text_type=TextType.CODE)
	img_nodes = split_nodes_images(code_nodes)
	link_nodes = split_nodes_links(img_nodes)
	return link_nodes