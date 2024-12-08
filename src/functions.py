import re

from htmlnode import HTMLNode, ParentNode
from textnode import text_to_text_nodes, TextNode

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
		case ul if all(line[:2]=="- " or line[:2]=="* " for line in ul.split("\n")):
			return "unordered_list"
		case li if all(re.match(r"(\d+)\. .*", line) for line in li.split("\n")):
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
				root.children.append(HTMLNode("pre", children=[HTMLNode(tag, children=text_to_children(text))]))
			case "quote":
				tag = "quote"
				text = map(lambda line: line.lstrip(">", block.split("\n"))).join()
				root.children.append(HTMLNode(tag, children=text_to_children(text)))
			case "unordered_list":
				continue
			case "ordered_list":
				continue
			case "paragraph":
				continue
	return root

def text_to_children(markdown):
	text_nodes = text_to_text_nodes(markdown)
	children = []
	for node in text_nodes:
		children.append(node.text_node_to_html_node())
	return children