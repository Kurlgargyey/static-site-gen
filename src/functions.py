def markdown_to_blocks(markdown):
	return list(
			filter(lambda block: not len(block)==0,
		  		map(lambda block: block.strip(),
		  			markdown.split("\n\n"))))

def block_to_blocktype(block):
	match block:
		case heading if heading[0:2] == "# ":
			return "heading"
		