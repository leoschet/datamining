import re

import nltk

# Regex for html pages splitting
SCRIPT_TAG_REGEX = re.compile(r'<script>(.|\n)*</script>')
HTML_TAGS_REGEX = re.compile(r'<[^>]*>')
WHITESPACE_REGEX = re.compile(r'( |\n|[^A-Za-z0-9])+')

# English stopwords and stemmer
ENGLISH_STOPWORDS = {word: None for word in nltk.corpus.stopwords.words('english')}
PORTER_STEMMER = nltk.stem.PorterStemmer()


def split_html_doc(html):
    """
    Removes html scripts, tags and splits by whitespaces, retuning a list of terms.

    :param html: the html in a string
    :return: a list of terms of the html
    """
    return WHITESPACE_REGEX.split(HTML_TAGS_REGEX.sub(' ', SCRIPT_TAG_REGEX.sub(' ', html)))


def filter_terms(terms, remove_stopwords=True, apply_stemming=True):
    """
    Put terms in lower case and removing spaces and empty strings, if required, stopwords are removed and stemming is
    applied.

    :param terms: list of terms to process
    :param remove_stopwords: if should remove english stopwords
    :param apply_stemming: if should apply stemming in the terms
    :return: the processed list of terms, the original is not modified
    """
    terms = [word.lower() for word in terms if word != '' and word != ' ']
    if remove_stopwords:
        terms = [word for word in terms if word not in ENGLISH_STOPWORDS]
    if apply_stemming:
        terms = [PORTER_STEMMER.stem(word) for word in terms]
    return terms
