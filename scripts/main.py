import logging
import os
import sys

from scripts.inverted_index import InvertedIndex
from scripts.text_operators import clear_html_document, clear_words

# -- Logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)
HANDLER.setFormatter(logging.Formatter('[%(asctime)s]::%(message)s'))
LOGGER.addHandler(HANDLER)

# -- Corpus generation from documents
corpus_dir = '../resources/corpus'
corpus = {}

LOGGER.info('Reading corpus from dir: %s' % corpus_dir)

for _, _, files in os.walk(corpus_dir):
    for file in files:
        LOGGER.debug('Reading corpus file %s' % file)
        document = open(corpus_dir + '/' + file, mode='r', encoding='utf-8').read()
        document_name = file
        document_terms = clear_html_document(document)
        corpus[document_name] = document_terms

LOGGER.info('Corpus loaded, document count: %d' % len(corpus))

# -- Inverted index creation
LOGGER.info('Creating inverted indexes')
#
LOGGER.debug('Creating inverted index 1')
ii_clean = InvertedIndex(
    corpus,
    lambda words: clear_words(words, remove_stopwords=False, apply_stemming=False)
)
LOGGER.debug('Inverted index 1 created')
#
LOGGER.debug('Creating inverted index 2')
ii_stop = InvertedIndex(
    corpus,
    lambda words: clear_words(words, apply_stemming=False)
)
LOGGER.debug('Inverted index 2 created')
#
LOGGER.debug('Creating inverted index 3')
ii_stem = InvertedIndex(
    corpus,
    lambda words: clear_words(words, remove_stopwords=False)
)
LOGGER.debug('Inverted index 3 created')
#
LOGGER.debug('Creating inverted index 4')
ii_stop_stem = InvertedIndex(
    corpus,
    lambda words: clear_words(words)
)
LOGGER.debug('Inverted index 4 created')
#
LOGGER.info('Inverted indexes created')
