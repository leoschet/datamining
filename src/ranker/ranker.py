import math
from functools import reduce

from ranker.inverted_index import InvertedIndex
from ranker.text_operators import WHITESPACE_REGEX


class Ranker:
    """
    Receives queries and ranks the documents based on the inverted index, using vector space with TF*IFD as term width
    calculation formula and cosine as similarity metric.
    """

    def __init__(self, inverted_index):
        """
        Initializes the ranker with the received inverted index.

        :param inverted_index: inverted index
        """
        self._inverted_index = inverted_index
        self._term_index = {term: index for index, term in enumerate(self._inverted_index.term_docs)}
        self._doc_vecs = {doc: self._calculate_doc_vec(doc) for doc in self._inverted_index.proc_corpus}

    def _calculate_doc_vec(self, doc):
        """
        Calculates the TF*IFD vector for the received document.

        :param doc: document name
        :return: document vector
        """
        doc_vec = len(self._inverted_index.term_docs) * [0]
        doc_vec_mag = 0
        for term in self._inverted_index.proc_corpus[doc]:
            term_freq, term_docs = self._inverted_index.term_docs[term]
            tf = len(term_docs[doc]) / term_freq
            idf = math.log(len(self._inverted_index.proc_corpus) / len(term_docs))
            tf_idf = tf * idf
            doc_vec[self._term_index[term]] = tf_idf
            doc_vec_mag += tf_idf ** 2
        return doc_vec, doc_vec_mag ** (1 / 2)

    def _calculate_query_vec(self, terms):
        """
        Calculates the TF*IDF vector to the received query terms

        :param terms: list of query terms
        :return: query vector
        """
        query_vec = len(self._inverted_index.term_docs) * [0]
        query_vec_mag = 0
        query_inverted_index = InvertedIndex({'query': terms})
        for term in query_inverted_index.proc_corpus['query']:
            if term not in self._inverted_index.term_docs:
                continue
            query_term_freq, _ = query_inverted_index.term_docs[term]
            term_freq, term_docs = self._inverted_index.term_docs[term]
            tf = query_term_freq / term_freq
            idf = math.log(len(self._inverted_index.proc_corpus) / len(term_docs))
            tf_idf = tf * idf
            query_vec[self._term_index[term]] = tf_idf
            query_vec_mag += tf_idf ** 2
        return query_vec, query_vec_mag ** (1 / 2)

    def _calculate_similarity(self, query_vec, query_vec_mag, doc):
        """
        Calculates the cosine similarity between the received query vector and the doc.

        :param query_vec: query vector
        :param query_vec_mag: query vector magnitude
        :param doc: document name
        :return: similarity between query and document
        """
        doc_vec, doc_vec_mag = self._doc_vecs[doc]
        denominator = query_vec_mag * doc_vec_mag
        return 0 if denominator == 0 else sum(map(lambda x, y: x * y, query_vec, doc_vec)) / denominator

    def search(self, query, all_docs=False):
        """
        Searches the query in documents of the ranker.

        :param query: query to search
        :param all_docs: if should check and return all documents
        :return: list of tuples with possible relevant documents ordered by similarity
        """
        query = query.strip()
        if query.startswith('"') and query.endswith('"'):
            return self._exact_search(query, all_docs)
        else:
            return self._default_search(query, all_docs)

    def _default_search(self, query, all_docs):
        """
        Runs a simple search with any document that contains any of the query terms.

        :param query: the query
        :param all_docs: if should check and return all documents
        :return: list of tuples with possible relevant documents ordered by similarity
        """
        terms = self._inverted_index.clean_func(WHITESPACE_REGEX.sub(' ', query).split(' '))
        terms = [term for term in terms if term in self._inverted_index.term_docs]
        common_term_docs = None
        if all_docs:
            common_term_docs = self._inverted_index.proc_corpus.keys()
        else:
            common_term_docs = {*[doc for term in terms for doc in self._inverted_index.term_docs[term][1]]}
        query_vec, query_vec_mag = self._calculate_query_vec(terms)
        similarities = [(doc, self._calculate_similarity(query_vec, query_vec_mag, doc)) for doc in common_term_docs]
        return sorted(similarities, key=lambda tup: tup[1], reverse=True)

    def _exact_search(self, query, all_docs):
        """
        Runs an exact search of the received query.
        :param query: the query
        :param all_docs: if should check and return all documents
        :return: list of tuples with exact matches
        """
        query = query[1:len(query) - 1]
        terms = self._inverted_index.clean_func(WHITESPACE_REGEX.sub(' ', query).split(' '))
        query_terms_len = len(terms)
        terms = [term for term in terms if term in self._inverted_index.term_docs]
        filtered_query_terms_len = len(terms)
        if query_terms_len != filtered_query_terms_len or query_terms_len == 0:
            return []  # some terms in query does not exits in the inverted index or terms is empty
        common_term_docs = reduce(lambda x, y: x & y, [{*self._inverted_index.term_docs[term][1]} for term in terms])
        if not common_term_docs:
            return []  # there is no document with all query terms
        common_sq_term_docs = []
        for doc in common_term_docs:
            doc_terms_positions = [self._inverted_index.term_docs[term][1][doc] for term in terms]
            if not reduce(self._find_consecutive_values, doc_terms_positions):
                common_sq_term_docs.append(doc)
        if not common_sq_term_docs:
            return []  # there is no document with all query terms in sequence
        query_vec, query_vec_mag = self._calculate_query_vec(terms)
        similarities = [(doc, self._calculate_similarity(query_vec, query_vec_mag, doc)) for doc in common_sq_term_docs]
        if all_docs:
            similarities_set = {doc for doc, similarity in similarities}
            other_docs = [(doc, 0) for doc in self._inverted_index.proc_corpus.keys() if doc not in similarities_set]
            similarities.extend(other_docs)
        return sorted(similarities, key=lambda tup: tup[1], reverse=True)

    @staticmethod
    def _find_consecutive_values(list1, list2):
        return [y for x in list1 for y in list2 if y > x and y - x <= 2]
