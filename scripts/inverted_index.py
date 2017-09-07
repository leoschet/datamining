class InvertedIndex:
    """
    Inverted index of the received docs.

    Contains the following fields:

    :clean_func: used to clean and filter the received corpus doc terms
    :proc_corpus: resultant corpus from applying clean_func in the original corpus
    :term_docs: dict of term -> (term_frequency, {doc: [term_doc_indices]})
    """

    def __init__(self, corpus, clean_func=None):
        """
        Initializes the inverted index with the received corpus.

        :param corpus: docs to terms dict
        :param clean_func: function the process a list of words
        """
        self.clean_func = clean_func if clean_func is not None else lambda x: x
        self.proc_corpus = {doc: self.clean_func(corpus[doc]) for doc in corpus}
        self.term_docs = self._build_term_docs(self.proc_corpus)

    @staticmethod
    def _build_term_docs(corpus):
        """
        Creates the term_docs dict based on the received corpus.

        :param corpus: docs to terms dict
        """
        term_docs = {}
        for doc in corpus:
            terms = corpus[doc]
            for index, term in enumerate(terms):
                if term not in term_docs:
                    term_docs[term] = (0, {})
                if doc not in term_docs[term][1]:
                    term_docs[term][1][doc] = []
                term_docs[term] = (term_docs[term][0] + 1, term_docs[term][1])
                term_docs[term][1][doc].append(index)
        return term_docs
