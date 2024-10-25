def markdown_to_blocks(markdown):
	return list(
			filter(lambda block: not len(block)==0,
		  		map(lambda block: block.strip(),
		  			markdown.split("\n\n"))))

def block_to_blocktype(block):
	match block:
		case heading if heading[:2] == "# ":
			return "heading"
		case code if code[:3] == "```" and code[-3:] == "```":
			return "code"
		case quote if all(line[:1] == ">" for line in quote.split("\n")):
			return "quote"
		case ul if all(line[:2]=="- " or line[:2]=="* " for line in ul.split("\n")):
			return "unordered_list"
		case _:
			return "paragraph"