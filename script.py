import os
import re

# DIRS
rootdir ='UnityDocumentation/en/Manual'

# REGEX
script_tag_regex = re.compile(r'<script>(.|\n)*</script>')
html_tags_regex = re.compile(r'<[^>]*>')
whitespace_regex = re.compile(r'( |\n|[^A-Za-z0-9])+')

# FUNCTIONS
def printu (str):
	print (str.encode ('utf-8'))


def clear_split_document (document):
	document = script_tag_regex.sub(' ', document)
	document = html_tags_regex.sub(' ', document)
	document = whitespace_regex.sub(' ', document)

	# printu (document)

	return document.split(' ')


# SCRIPT
for _, _, files in os.walk (rootdir):
	for file in files:
		document = open (rootdir + '/' + file, mode='r', encoding='utf-8').read()
		document_terms = clear_split_document (document)
		
		# print (document_terms)

		break

inverted_index = {}