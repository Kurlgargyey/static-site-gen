class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		return " " + " ".join(map(lambda pair: f"{pair[0]}=\"{pair[1]}\"", self.props.items()))

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
	def __init__(self, tag=None, value=None, children=None, props=None):
		super().__init__(tag, value, None, props)

	def to_html(self):
		if self.value is None:
			raise ValueError("leaf nodes must have a value")
		if self.tag is None:
			return self.value

		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
	def __init__(self, tag=None, value=None, children=None, props=None):
		super().__init__(tag, None, children, props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("parent nodes must have a tag")
		if self.children is None or len(self.children) == 0:
			raise ValueError("parent nodes must have children")

		children_html = "".join(map(lambda child: child.to_html(), self.children))
		return f"<{self.tag}>{children_html}</{self.tag}>"
