import re

from htmlnode import HTMLNode
from textnode import text_to_text_nodes, TextNode, TextType

def markdown_to_blocks(markdown):
	return list(
			filter(lambda block: not len(block)==0,
		  		map(lambda block: block.strip(),
		  			markdown.split("\n\n"))))

def block_to_blocktype(block):
	match block:
		case heading if re.match(r"#+ ", heading):
			return "heading"
		case code if code[:3] == "```" and code[-3:] == "```":
			return "code"
		case quote if all(line[:1] == ">" for line in quote.split("\n")):
			return "quote"
		case ul if all(re.match(r"^(\*|\-|\+)\s*", line) for line in ul.split("\n")):
			return "unordered_list"
		case li if all(re.match(r"^\d+\.\s*", line) for line in li.split("\n")):
			return "ordered_list"
		case _:
			return "paragraph"

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	root = HTMLNode(tag="div", children=[])
	for block in blocks:
		match block_to_blocktype(block):
			case "heading":
				level = len(block) - len(block.lstrip("#"))
				text = block.lstrip("#")
				text = text.lstrip(" ")
				root.children.append(HTMLNode(f"h{level}", children = text_to_children(text)))
			case "code":
				tag = "code"
				text = block.strip("```")
				text = text.strip("\n")
				root.children.append(HTMLNode("pre", children=[HTMLNode(tag, children=text_to_children(text))]))
			case "quote":
				tag = "blockquote"
				text = map(lambda line: line.lstrip(">"), block.split("\n")).join()
				root.children.append(HTMLNode(tag, children=text_to_children(text)))
			case "unordered_list":
				list_node = HTMLNode("ul", children= [])
				for item in block.split("\n"):
					text = re.sub(r"^(\*|\+|\-)\s*", "", item)
					item_node = HTMLNode("li", children=[])
					item_node.children.append(HTMLNode("p", children=text_to_children(text) if text else [TextNode("", TextType.NORMAL, None).text_node_to_html_node()]))
					list_node.children.append(item_node)
				root.children.append(list_node)
			case "ordered_list":
				list_node = HTMLNode("ol", children= [])
				for item in block.split("\n"):
					text = re.sub(r"^\d+\.\s*", "", item)
					item_node = HTMLNode("li", children=[])
					item_node.children.append(HTMLNode("p", children=text_to_children(text) if text else [TextNode("", TextType.NORMAL, None).text_node_to_html_node()]))
					list_node.children.append(item_node)
				root.children.append(list_node)
			case "paragraph":
				tag = "p"
				root.children.append(HTMLNode("p", children=text_to_children(block)))
	return root

def publish_static():
	

def text_to_children(markdown):
	text_nodes = text_to_text_nodes(markdown)
	children = []
	for node in text_nodes:
		children.append(node.text_node_to_html_node())
	return children