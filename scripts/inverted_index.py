"""
Inverted index of the received documents.

Contains 2 attributes to be used externally:
    term_documents: {str: (int, {str:int})}
    term_documents has as key a term (word) in the 

    term_indexer: {str: int}
"""


class InvertedIndex:
    term_documents = {}
    term_indexer = {}

    """
    Initializes the inverted index with the received corpus.

    :param corpus: [(str, [str])] list of document names and words
    """

    def __init__(self, corpus):
        self.__build_term_documents(corpus)
        self.__build_term_indexer()

    """
    Creates the term_document dict based on the document_list.
    
    :param corpus: [(str, [str])] list of document names and words
    """

    def __build_term_documents(self, corpus):
        for document in corpus:
            document_name = document[0]
            document_words = document[1]
            for word in document_words:
                if word not in self.term_documents:
                    self.term_documents[word] = (0, {})
                if document_name not in self.term_documents[word][1]:
                    self.term_documents[word][1][document_name] = 0
                self.term_documents[word] = (
                    self.term_documents[word][0] + 1,
                    self.term_documents[word][1]
                )
                self.term_documents[word][1][document_name] += 1

    """
    Creates the term_indexer, that is a map of each term to its respective index
    """

    def __build_term_indexer(self):
        index = 0
        for term in self.term_documents:
            self.term_indexer[term] = index
            index += 1
