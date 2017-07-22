import textract

def parse_to_string(filename):
	return textract.process(filename)