def build_inverted_index(document_list):
	inverted_index_list = {}
	for document in document_list:
		for word in document[1]:
			if word not in inverted_index_list:
				inverted_index_list[word] = {}
			if document[0] not in inverted_index_list[word]:
				inverted_index_list[word][document[0]] = 0
			inverted_index_list[word][document[0]] += 1
	return inverted_index_list

# doc1 = "eu amo comer".split(" ")
# doc2 = "eu eu amo beber".split(" ")

# docs = [("doc1",doc1),("doc2",doc2)]
# print(build_inverted_index(docs))