import re
import os
import shutil

from htmlnode import HTMLNode, ParentNode
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
		case ul if all(re.match(r"^(\*|\-|\+)\s+", line) for line in ul.split("\n")):
			return "unordered_list"
		case li if all(re.match(r"^\d+\.\s+", line) for line in li.split("\n")):
			return "ordered_list"
		case _:
			return "paragraph"

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	root = ParentNode(tag="div", children=[])
	for block in blocks:
		match block_to_blocktype(block):
			case "heading":
				level = len(block) - len(block.lstrip("#"))
				text = block.lstrip("#")
				text = text.lstrip(" ")
				root.children.append(ParentNode(f"h{level}", children = text_to_children(text)))
			case "code":
				tag = "code"
				text = block.strip("```")
				text = text.strip("\n")
				root.children.append(ParentNode("pre", children=[ParentNode(tag, children=text_to_children(text))]))
			case "quote":
				tag = "blockquote"
				text = " ".join(list(map(lambda line: line.lstrip(">"), block.split("\n"))))
				root.children.append(ParentNode(tag, children=text_to_children(text)))
			case "unordered_list":
				list_node = ParentNode("ul", children= [])
				for item in block.split("\n"):
					text = re.sub(r"^(\*|\+|\-)\s+", "", item)
					item_node = ParentNode("li", children=[])
					item_node.children.append(ParentNode("p", children=text_to_children(text) if text else [TextNode("", TextType.NORMAL, None).text_node_to_html_node()]))
					list_node.children.append(item_node)
				root.children.append(list_node)
			case "ordered_list":
				list_node = ParentNode("ol", children= [])
				for item in block.split("\n"):
					text = re.sub(r"^\d+\.\s+", "", item)
					item_node = ParentNode("li", children=[])
					item_node.children.append(ParentNode("p", children=text_to_children(text) if text else [TextNode("", TextType.NORMAL, None).text_node_to_html_node()]))
					list_node.children.append(item_node)
				root.children.append(list_node)
			case "paragraph":
				tag = "p"
				root.children.append(ParentNode("p", children=text_to_children(block)))
	return root

def text_to_children(markdown):
	text_nodes = text_to_text_nodes(markdown)
	children = []
	for node in text_nodes:
		children.append(node.text_node_to_html_node())
	return children

def publish_folder(source , dest):
	if os.path.exists(dest):
		shutil.rmtree(dest)
	os.mkdir(dest)
	if not os.path.isfile(source):
		for path in os.listdir(source):
			if os.path.isfile(path):
				shutil.copy(os.path.join(source, path), os.path.join(dest, path))
			else:
				publish_folder(os.path.join(source, path), os.path.join(dest, path))
	else:
		shutil.copy(source, dest)

def extract_title(markdown):
	for block in markdown_to_blocks(markdown):
		if re.match(r"^#\s+", block):
			return re.sub(r"^#\s+", "", block)

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")
	with open(from_path) as source:
		source_markdown = source.read()
		with open(template_path) as template:
			webpage = template.read()
			html_data = markdown_to_html_node(source_markdown)
			title = extract_title(source_markdown)
			webpage.replace("{{ Title }}", title)
			webpage.replace("{{ Content }}", html_data.to_html())

			if not os.path.exists(os.path.dirname(from_path)):
				os.mkdir(os.path.dirname(from_path))

			with open(dest_path) as dest:
				dest.write(webpage)
