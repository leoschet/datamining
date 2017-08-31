def build_inverted_index(document_list):
	inverted_index_list = {}
	for document in document_list:
		for word in document[1]:
			if word not in inverted_index_list:
				inverted_index_list[word] = (0, {})
			if document[0] not in inverted_index_list[word][1]:
				inverted_index_list[word][1][document[0]] = 0
			inverted_index_list[word] = (inverted_index_list[word][0] + 1, inverted_index_list[word][1])
			inverted_index_list[word][1][document[0]] += 1
	return inverted_index_list