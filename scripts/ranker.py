from inverted_index import InvertedIndex
from math import log, sqrt

class Ranker:
    inverted_index = None
    term_indexer = {}
    document_vectors = {}

    _whitespace_regex = re.compile(r'( |\n|[^A-Za-z0-9])+')

    def __init__(self, inverted_index):
        self.inverted_index = inverted_index
        self.__build_term_indexer()
        self.__calculate_document_vectors()
    
    def __build_term_indexer(self):
        index = 0
        for term in self.inverted_index.term_documents:
            self.term_indexer[term] = index
            index += 1
            
    def __calculate_document_vectors(self):
        for document_name in self.inverted_index.processed_corpus:
            self.document_vectors[document_name] = __calculate_document_vector(document_name)

    def __calculate_document_vector(self, document_name):
        document_vector_mag2 = 0
        document_vector = len(self.inverted_index.term_documents.keys) * [0]

        for term in self.inverted_index.term_documents:
            (term_frequency, documents) = self.inverted_index.term_documents[term]
            tf = documents[document_name] / term_frequency # term frequency on document / total term frequency
            idf = log(len(self.inverted_index.processed_corpus) / len(documents))
            tfidf = tf * idf
            document_vector[self.term_indexer[term]] = tfidf
            document_vector_mag2 += tfidf * tfidf

        return (sqrt(document_vector_mag2), document_vector)

    def __calculate_query_vector(self, query_terms):
        query_vector = len(self.inverted_index.term_documents.keys) * [0]

        query_inverted_index = InvertedIndex([('query', query_terms)])

        for term in query_inverted_index.term_documents:
            if term not in self.inverted_index.term_documents.keys:
                continue

            (query_term_frequency, _) = query_inverted_index.term_documents[term]            
            (term_frequency, documents) = self.inverted_index.term_documents[term]

            tf = query_term_frequency / term_frequency
            idf = log(len(self.inverted_index.processed_corpus) / len(documents))

            query_vector[self.term_indexer[term]] = tf * idf

        return query_vector

    def search(self, query):
        query terms = self.inverted_index.clean_function(whitespace_regex.sub(' ', query).split(' '))
        query_vector = __calculate_query_vector(query terms)

        # compute similarity
        similarities = []
        for document_name in self.document_vectors:
            (document_vector_mag, document_vector) = document_vectors[document_name]
            similarity = self.list_similarity(query_vector, document_vector, document_vector_mag)
            similarities.append((document_name, similarity))

        similarities.sort(key = lambda tuple: tuple[1])
        return similarities

    def list_similarity(self, query_vector, document_vector, document_vector_mag):
        dot_product = 0

        for i in range(0, len(query_vector)):
            dot_product += query_vector[i] * document_vector[i]

        return dot_product / document_vector_mag