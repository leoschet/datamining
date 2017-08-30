import os
import re
import stopwords_stemming


# DIRS
rootdir ='../UnityDocumentation/en/Manual'


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
document_terms_list = []
document_terms_list_stop = []
document_terms_list_stem = []
document_terms_list_stop_stem = []

for _, _, files in os.walk (rootdir):
	for file in files:
		document = open (rootdir + '/' + file, mode='r', encoding='utf-8').read()
		document_terms_original = clear_split_document (document)
		
		# print (document_terms)
		document_terms = stopwords_stemming(document_terms_original, remove_stopwords = False, do_stemming = False)
		document_terms_list.append((file, document_terms))

		document_terms = stopwords_stemming(document_terms_original, remove_stopwords = True, do_stemming = False)
		document_terms_list_stop.append((file, document_terms))

		document_terms = stopwords_stemming(document_terms_original, remove_stopwords = False, do_stemming = True)
		document_terms_list_stem.append((file, document_terms))

		document_terms = stopwords_stemming(document_terms_original, remove_stopwords = True, do_stemming = True)
		document_terms_list_stop_stem.append((file, document_terms))
		
		# TODO: remove break
		break

# build_inverted_index