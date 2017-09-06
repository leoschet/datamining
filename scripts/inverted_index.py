class InvertedIndex:
    """
    Inverted index of the received documents.
    """

    def __init__(self, corpus, clean_function=None):
        """
        Initializes the inverted index with the received corpus.

        :param corpus: dict of document names to document words list
        :param clean_function: function the process a list of words
        """
        self.processed_corpus = {}
        self.term_documents = {}
        self.clean_function = clean_function
        self._build_inverted_index(corpus)

    def _build_inverted_index(self, corpus):
        """
        Creates the term_documents dict based on the processed_corpus that is generated using the clean_function.

        :param corpus: list of document names and words
        """
        for document_name in corpus:
            document_words = self.clean_function(corpus[document_name]) \
                if self.clean_function is not None else corpus[document_name]
            self.processed_corpus[document_name] = document_words
            for index, word in enumerate(document_words):
                if word not in self.term_documents:
                    self.term_documents[word] = (0, {})
                if document_name not in self.term_documents[word][1]:
                    self.term_documents[word][1][document_name] = (0, [])
                self.term_documents[word] = (
                    self.term_documents[word][0] + 1,
                    self.term_documents[word][1]
                )
                self.term_documents[word][1][document_name] = (
                    self.term_documents[word][1][document_name][0] + 1,
                    self.term_documents[word][1][document_name][1]
                )
                self.term_documents[word][1][document_name][1].append(index)
