from inverted_index import InvertedIndex
from math import log

class Ranker:
    corpus = None
    inverted_index = None
    document_vectors = {}

    def __init__(self, inverted_index, corpus):
        self.corpus = corpus
        self.inverted_index = inverted_index
        self.__calculate_document_vectors()

    def __calculate_document_vectors(self):
        for document in self.corpus:
            document_name = document[0]
            document_words = document[1]
            self.document_vectors[document_name] = __calculate_document_tfidf(document_name)

    def __calculate_document_tfidf(self, document_name):
        document_vector = len(self.inverted_index.term_documents.keys) * [0]

        for term in self.inverted_index.term_documents:
            (term_frequency, documents) = self.inverted_index.term_documents[term]
            tf = documents[document_name] / term_frequency # term frequency on document / total term frequency
            idf = log(len(self.corpus) / len(documents))
            document_vector[self.inverted_index.term_indexer[term]] = tf * idf

        return document_vector

    def __calculate_query_tfidf(self, query_terms):
        query_vector = len(self.inverted_index.term_documents.keys) * [0]

        query_inverted_index = InvertedIndex([('query', query_terms)])

        for term in query_inverted_index.term_documents:
            if term not in self.inverted_index.term_documents.keys:
                continue

            (query_term_frequency, _) = query_inverted_index.term_documents[term]            
            (term_frequency, documents) = self.inverted_index.term_documents[term]

            tf = query_term_frequency / term_frequency
            idf = log(len(self.corpus) / len(documents))

            query_vector[self.inverted_index.term_indexer[term]] = tf * idf

        return query_vector

    def search(self, query):
        #aplica transf
        #calcula tfidf
        pass
        
        