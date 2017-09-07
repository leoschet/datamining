import math

from scripts.inverted_index import InvertedIndex
from scripts.text_operators import WHITESPACE_REGEX


class Ranker:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        self.term_indexer = {term: index for index, term in enumerate(self.inverted_index.term_documents)}
        self.document_vectors = {document: self._calculate_document_vector(document)
                                 for document in self.inverted_index.processed_corpus}

    def _calculate_document_vector(self, document):
        document_vector = len(self.inverted_index.term_documents) * [0]
        document_vector_mag2 = 0
        for term in self.inverted_index.processed_corpus[document]:
            term_frequency, documents = self.inverted_index.term_documents[term]
            tf = documents[document][0] / term_frequency
            idf = math.log(len(self.inverted_index.processed_corpus) / len(documents))
            tf_idf = tf * idf
            document_vector[self.term_indexer[term]] = tf_idf
            document_vector_mag2 += tf_idf ** 2
        return document_vector, math.sqrt(document_vector_mag2)

    def _calculate_query_vector(self, terms):
        query_vector = len(self.inverted_index.term_documents) * [0]
        query_vector_mag2 = 0
        query_inverted_index = InvertedIndex({'query': terms})
        for term in query_inverted_index.term_documents:
            if term not in self.inverted_index.term_documents:
                continue
            query_term_frequency, _ = query_inverted_index.term_documents[term]
            term_frequency, documents = self.inverted_index.term_documents[term]
            tf = query_term_frequency / term_frequency
            idf = math.log(len(self.inverted_index.processed_corpus) / len(documents))
            tf_idf = tf * idf
            query_vector[self.term_indexer[term]] = tf_idf
            query_vector_mag2 += tf_idf ** 2
        return query_vector, math.sqrt(query_vector_mag2)

    @staticmethod
    def _calculate_similarity(query_vector_and_mag, document_vector_and_mag):
        vector1 = query_vector_and_mag[0]
        vector1_mag = query_vector_and_mag[1]
        vector2 = document_vector_and_mag[0]
        vector2_mag = document_vector_and_mag[1]
        if vector1_mag == 0 or vector2_mag == 0:
            return 0
        return sum([x * y for x, y in zip(vector1, vector2)]) / (vector1_mag * vector2_mag)

    def search(self, query):
        query_terms = self.inverted_index.clean_function(WHITESPACE_REGEX.sub(' ', query).split(' '))
        query_vector_and_mag = self._calculate_query_vector(query_terms)
        similarities = [(document, self._calculate_similarity(query_vector_and_mag, self.document_vectors[document]))
                        for document in self.document_vectors]
        return sorted(similarities, key=lambda tup: tup[1], reverse=True)
