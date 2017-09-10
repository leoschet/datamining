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


def read_corpus(corpus_dir):
    """
    Read de corpus html files from the received directory.
    :param corpus_dir: corpus directory
    :return: {doc_name:[doc_terms]}
    """
    LOGGER.info('Reading corpus')
    corpus = {}
    for _, _, files in os.walk(corpus_dir):
        for file in files:
            content = open(corpus_dir + '/' + file, mode='r', encoding='utf-8').read()
            corpus[file] = split_html_doc(content)
    LOGGER.info('Corpus loaded, document count: %d' % len(corpus))
    return corpus


def build_rankers(corpus, configs):
    """
    build the inverted indexes and rankers with the received corpus and configurations.
    :param corpus: the corpus dict {doc_name:[doc_terms]}
    :param configs: the configurations [{'name':'ranker_name', 'clean_func':func(['x']):['x'']}]
    :return: {ranker_name:ranker}
    """
    LOGGER.info('Creating indexes and rankers')
    rankers = {}
    for config in configs:
        LOGGER.debug('Creating inverted index %s' % config['name'])
        inverted_index = InvertedIndex(corpus, config['clean_func'])
        LOGGER.debug('Creating ranker %s' % config['name'])
        rankers[config['name']] = Ranker(inverted_index)
    LOGGER.info('Indexers and Rankers created')
    return rankers


# Default rankers configurations
DEFAULT_CONFIGS = [
    {'name': 'clean',
     'clean_func': lambda terms: filter_terms(terms, remove_stopwords=False, apply_stemming=False)},
    {'name': 'stop', 'clean_func': lambda terms: filter_terms(terms, apply_stemming=False)},
    {'name': 'stem', 'clean_func': lambda terms: filter_terms(terms, remove_stopwords=False)},
    {'name': 'stop_stem', 'clean_func': lambda terms: filter_terms(terms)}
]


def get_default_rankers():
    """
    Returns the default 4 rankers of the local corpus ('clean', 'stop', 'stem', 'stop_stem').
    :return: {ranker_name:ranker}
    """
    corpus_dir = '../res/corpus'
    corpus = read_corpus(corpus_dir)
    return build_rankers(corpus, DEFAULT_CONFIGS)


def search_query(query, rankers, all_docs=False):
    """
    Search the received query in the rankers.
    :param query: a str with the query
    :param rankers: {ranker_name:ranker}
    :return: ({ranker_name:[(document, similarity$dec_ord)]}, {(ranker1, ranker2):correlation})
    """
    LOGGER.info('Running query: %s, all_docs: %s' % (query, all_docs))
    results = {ranker_name: rankers[ranker_name].search(query, all_docs) for ranker_name in rankers}
    """
    for ranker_name in results:
        result = results[ranker_name]
        print (ranker_name)
        for doc, similarity in result:
            print(doc)
        print()
    """
    correlations = {}
    """
    LOGGER.info('Calculating correlations')
    for i, ranker_name1 in enumerate(results):
        for j, ranker_name2 in enumerate(results):
            if i >= j:
                continue
            correlation = spearman_correlation(
                map(lambda tup: tup[0], results[ranker_name1]),
                map(lambda tup: tup[0], results[ranker_name2])
            )
            LOGGER.info('Correlation between %s and %s: %d' % (ranker_name1, ranker_name2, correlation))
            correlations[(ranker_name1, ranker_name2)] = correlation
            correlations[(ranker_name2, ranker_name1)] = correlation
    """
    return results, correlations


# Queries
"""
queries = [
    'virtual reality overview',
    '"virtual reality overview"',
    # 'webgl and player settings',
    # 'the networked state of the game'
]
"""
