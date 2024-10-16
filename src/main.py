from textnode import TextType, TextNode

def main():
	content = "blabla"
	type = TextType.ITALIC
	url = "https://bla.blabla.com"
	new_node = TextNode(content, type, url)
	print(new_node)

if __name__ == "__main__":
	main()