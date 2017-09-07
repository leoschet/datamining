import logging
import os
import sys

from scripts.inverted_index import InvertedIndex
from scripts.ranker import Ranker
from scripts.text_operators import clear_html_document, clear_words

# -- Logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)
HANDLER.setFormatter(logging.Formatter('[%(asctime)s]::%(message)s'))
LOGGER.addHandler(HANDLER)

# -- Corpus generation from documents
LOGGER.info('Reading corpus')
corpus_dir = '../resources/corpus'
corpus = {}
for _, _, files in os.walk(corpus_dir):
    for file in files:
        LOGGER.debug('Reading corpus file %s' % file)
        content = open(corpus_dir + '/' + file, mode='r', encoding='utf-8').read()
        corpus[file] = clear_html_document(content)
LOGGER.info('Corpus loaded, document count: %d' % len(corpus))

# -- Creating indexers and rankers
LOGGER.info('Creating indexes and rankers')
inverted_index_configurations = [
    {'name': 'clean', 'clean_function': lambda words: clear_words(words, remove_stopwords=False, apply_stemming=False)},
    {'name': 'stop', 'clean_function': lambda words: clear_words(words, apply_stemming=False)},
    {'name': 'stem', 'clean_function': lambda words: clear_words(words, remove_stopwords=False)},
    {'name': 'stop_stem', 'clean_function': lambda words: clear_words(words)}
]
rankers = {}
for configuration in inverted_index_configurations:
    LOGGER.debug('Creating inverted index %s' % configuration['name'])
    inverted_index = InvertedIndex(corpus, configuration['clean_function'])
    LOGGER.debug('Creating ranker %s' % configuration['name'])
    rankers[configuration['name']] = Ranker(inverted_index)
LOGGER.info('Indexers and Rankers created')

LOGGER.info('Running queries')
search_results = {}
for ranker in rankers:
    search_results[ranker] = rankers[ranker].search('virtual reality overview')

searches = zip(*[search_results[search_result] for search_result in search_results])
for documents in searches:
    print(documents)
