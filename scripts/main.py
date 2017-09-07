import logging
import os
import sys

from scripts.inverted_index import InvertedIndex
from scripts.ranker import Ranker
from scripts.text_operators import split_html_doc, filter_terms

# Logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)
HANDLER.setFormatter(logging.Formatter('[%(asctime)s]::%(message)s'))
LOGGER.addHandler(HANDLER)

# Corpus generation
LOGGER.info('Reading corpus')
corpus_dir = '../resources/corpus'
corpus = {}
for _, _, files in os.walk(corpus_dir):
    for file in files:
        content = open(corpus_dir + '/' + file, mode='r', encoding='utf-8').read()
        corpus[file] = split_html_doc(content)
LOGGER.info('Corpus loaded, document count: %d' % len(corpus))

# Indexers and rankers
LOGGER.info('Creating indexes and rankers')
configs = [
    {'name': 'clean', 'clean_func': lambda terms: filter_terms(terms, remove_stopwords=False, apply_stemming=False)},
    {'name': 'stop', 'clean_func': lambda terms: filter_terms(terms, apply_stemming=False)},
    {'name': 'stem', 'clean_func': lambda terms: filter_terms(terms, remove_stopwords=False)},
    {'name': 'stop_stem', 'clean_func': lambda terms: filter_terms(terms)}
]
rankers = {}
for config in configs:
    LOGGER.debug('Creating inverted index %s' % config['name'])
    inverted_index = InvertedIndex(corpus, config['clean_func'])
    LOGGER.debug('Creating ranker %s' % config['name'])
    rankers[config['name']] = Ranker(inverted_index)
LOGGER.info('Indexers and Rankers created')

# Queries
LOGGER.info('Running queries')
search_results = {}
for ranker in rankers:
    search_results[ranker] = rankers[ranker].search('virtual reality overview')

searches = zip(*[search_results[search_result] for search_result in search_results])
for documents in searches:
    print(documents)
