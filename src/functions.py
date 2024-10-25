def markdown_to_blocks(markdown):
	return list(
			filter(lambda block: not len(block)==0,
		  		map(lambda block: block.strip(),
		  			markdown.split("\n\n"))))