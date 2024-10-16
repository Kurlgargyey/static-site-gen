from textnode import NodeType, TextNode

def main():
    content = "blabla"
    type = NodeType.LEAF
    url = "https://bla.blabla.com"
    new_node = TextNode(content, type, url)
    print(new_node)

main()