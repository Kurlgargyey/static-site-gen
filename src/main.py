from textnode import TextType, TextNode
from functions import publish_folder, generate_pages_recursive
import os, shutil

def main():
	if os.path.exists(os.path.join(os.getcwd(), "public")):
		shutil.rmtree(os.path.join(os.getcwd(), "public"))
	publish_folder(os.path.join(os.getcwd(), "static"), os.path.join(os.getcwd(), "public"))
	generate_pages_recursive(os.path.join(os.getcwd(), "content/"), os.path.join(os.getcwd(), "template.html"), os.path.join(os.getcwd(), "public/"))

if __name__ == "__main__":
	main()