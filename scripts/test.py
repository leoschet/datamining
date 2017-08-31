import inverted_index as ii
import tf_idf as ti

doc1 = "eu amo comer comer".split(" ")
doc2 = "eu eu eu amo beber".split(" ")
# doc3 = " ".split(" ")

docs = [("doc1",doc1),("doc2",doc2)]
# docs = [("doc1",doc1),("doc2",doc2),("doc3",doc3)]
inverted_index_list = ii.build_inverted_index(docs)
print(inverted_index_list)
document_occurences_list = ti.document_occurences_list([doc[0] for doc in docs], inverted_index_list)
print(document_occurences_list)
tf_idf_list = ti.tf_idf_list(document_occurences_list, inverted_index_list)
print(tf_idf_list)