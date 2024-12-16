from textnode import TextType, TextNode
from functions import publish_folder
import os

def main():
	content = "blabla"
	type = TextType.ITALIC
	url = "https://bla.blabla.com"
	new_node = TextNode(content, type, url)
	print(new_node)
	publish_folder(os.path.join(os.getcwd(), "static"), os.path.join(os.getcwd(), "public"))

if __name__ == "__main__":
	main()