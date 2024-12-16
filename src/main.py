from textnode import TextType, TextNode
from functions import publish_folder, generate_page
import os, shutil

def main():
	shutil.rmtree(os.path.join(os.getcwd(), "public"))
	publish_folder(os.path.join(os.getcwd(), "static"), os.path.join(os.getcwd(), "public"))
	generate_page(os.path.join(os.getcwd(), "content/index.md"), os.path.join(os.getcwd(), "template.html"), os.path.join(os.getcwd(), "public/index.html"))

if __name__ == "__main__":
	main()