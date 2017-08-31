import math

def document_occurences(document_name, inverted_index_list):
	return [inverted_index_list[i][1][document_name] if document_name in inverted_index_list[i][1] else 0 for i in list(inverted_index_list)]

def document_occurences_list(document_name_list, inverted_index_list):
	document_occurences_list = {}
	for document_name in document_name_list:
		document_occurences_list[document_name] = document_occurences(document_name, inverted_index_list)
	return document_occurences_list

def tf_idf_list(document_occurences_list, inverted_index_list):
	total_documents_quantity = len(document_occurences_list)
	total_documents_per_word_quantity = [len(inverted_index_list[i][1]) for i in inverted_index_list]
	tf_idf_list = document_occurences_list
	for document in tf_idf_list:
		max_occurence_document = max(tf_idf_list[document])
		# calculating tf
		#	occurence: number of the occurences of the current word in the comprehension list
		#	max_occurence_document: number of occurences of the word that max occurs in the current document
		tf_idf_list[document] = [occurence/max_occurence_document for occurence in tf_idf_list[document]]
		# calculating tf-idf
		#	tf_result: tf obtained from tf operation for the current word in the comprehension list
		#	total_documents_quantity: total number of documents in the database
		#	documents_quantity_word: number of documents that contains the current word in the comprehension list
		tf_idf_list[document] = [tf_result * math.log(total_documents_quantity/documents_quantity_word) for tf_result, documents_quantity_word in zip(tf_idf_list[document], total_documents_per_word_quantity)]
	return tf_idf_list

# [a[i][1]['doc2'] if 'doc2' in a[i][1] else 0 for i in list(a)]