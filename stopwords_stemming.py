import nltk

english_stopwords = nltk.corpus.stopwords.words('english')
porter_stemmer = nltk.stem.PorterStemmer()

def stopwords_stemming(s, remove_stopwords, do_stemming):
	s = [word.lower() for word in s]
	if (remove_stopwords):
		s = [word for word in s if word not in english_stopwords]
	if (do_stemming):
		s = [porter_stemmer.stem(word) for word in s]
	return s