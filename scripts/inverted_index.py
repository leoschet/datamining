class InvertedIndex:
    """
    Inverted index of the received documents.
    """

    def __init__(self, corpus, clean_function=None):
        """
        Initializes the inverted index with the received corpus.

        :param corpus: documents to terms dict
        :param clean_function: function the process a list of words
        """
        self.processed_corpus = {}
        self.term_documents = {}
        self.clean_function = clean_function
        self._build_inverted_index(corpus)

    def _build_inverted_index(self, corpus):
        """
        Creates the term_documents dict based on the processed_corpus that is generated using the clean_function.

        :param corpus: documents to terms dict
        """
        for document in corpus:
            terms = self.clean_function(corpus[document]) if self.clean_function is not None else corpus[document]
            self.processed_corpus[document] = terms
            for index, word in enumerate(terms):
                if word not in self.term_documents:
                    self.term_documents[word] = (0, {})
                if document not in self.term_documents[word][1]:
                    self.term_documents[word][1][document] = (0, [])
                self.term_documents[word] = (
                    self.term_documents[word][0] + 1,
                    self.term_documents[word][1]
                )
                self.term_documents[word][1][document] = (
                    self.term_documents[word][1][document][0] + 1,
                    self.term_documents[word][1][document][1]
                )
                self.term_documents[word][1][document][1].append(index)
