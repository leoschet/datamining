import re

import nltk

# Regex for html pages splitting
SCRIPT_TAG_REGEX = re.compile(r'<script>(.|\n)*</script>')
HTML_TAGS_REGEX = re.compile(r'<[^>]*>')
WHITESPACE_REGEX = re.compile(r'( |\n|[^A-Za-z0-9])+')

# English stopwords and stemmer
ENGLISH_STOPWORDS = {word: None for word in nltk.corpus.stopwords.words('english')}
PORTER_STEMMER = nltk.stem.PorterStemmer()


def clear_html_document(html):
    """
    Removes html scripts, tags and splits by whitespaces, retuning a list of words.

    :param html: the html in a string
    :return: a list of words of the html
    """
    return WHITESPACE_REGEX.split(HTML_TAGS_REGEX.sub(' ', SCRIPT_TAG_REGEX.sub(' ', html)))


def clear_words(words, remove_stopwords=True, apply_stemming=True):
    """
    Put words in lower case, removing stopwords and stemming if required.

    :param words: list of words to clear
    :param remove_stopwords: if should remove english stopwords
    :param apply_stemming: if should apply stemming in the words
    :return: the processed list of words, the original is not modified
    """
    words = [word.lower() for word in words]
    if remove_stopwords:
        words = [word for word in words if word not in ENGLISH_STOPWORDS and word != '' and word != ' ']
    if apply_stemming:
        words = [PORTER_STEMMER.stem(word) for word in words]
    return words
