import logging
import os
import sys

from ranker.inverted_index import InvertedIndex
from ranker.ranker import Ranker
from ranker.text_operators import split_html_doc, filter_terms
from spearman_correlation import spearman_correlation

# Logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setLevel(logging.DEBUG)
HANDLER.setFormatter(logging.Formatter('[%(asctime)s]::%(message)s'))
LOGGER.addHandler(HANDLER)

# Corpus generation
LOGGER.info('Reading corpus')
corpus_dir = '../res/corpus'
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
LOGGER.info('Running queries and calculating ranker results correlation')
queries = [
    'virtual reality overview',
    '"virtual reality overview"',
    # 'webgl and player settings',
    # 'the networked state of the game'
]
for query in queries:
    search_results = {ranker_name: rankers[ranker_name].search(query) for ranker_name in rankers}
    print('Query result comparative')
    ranker_names = [*search_results.keys()]
    print(ranker_names)
    merged_ranker_results = [*zip(*search_results.values())]
    for merged_ranker_result in merged_ranker_results:
        print(merged_ranker_result)
    print('Correlation between search results for query: %s' % query)
    for i in range(len(search_results)):
        for j in range(len(search_results)):
            if i >= j:
                continue
            correlation = spearman_correlation(
                map(lambda tup: tup[0], search_results[configs[i]['name']]),
                map(lambda tup: tup[0], search_results[configs[j]['name']])
            )
            print('Correlation between %s and %s: %d' % (configs[i]['name'], configs[j]['name'], correlation))
