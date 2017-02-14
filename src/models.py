import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from nltk.corpus import stopwords
from nltk.stem.snowball import DutchStemmer
from nltk import word_tokenize


class PartyClassifier:

    def __init__(self):

        self.estimator = None
        self.stemmer = DutchStemmer()

    def fit(self, X, y):

        n_labels = len(np.unique(y))
        equal_priors = 1. * np.ones(n_labels) / n_labels

        estimator = Pipeline(steps=[('vectorizer', CountVectorizer(encoding='utf-8', decode_error='strict',
                                                                   strip_accents=None, lowercase=True,
                                                                   preprocessor=None,
                                                                   tokenizer=self.__tokenize,
                                                                   stop_words=stopwords.words('dutch'),
                                                                   ngram_range=(1, 2), analyzer='word', max_df=0.1,
                                                                   min_df=2,
                                                                   max_features=100000, vocabulary=None, binary=False,
                                                                   dtype=np.int64)),
                                    ('classifier', MultinomialNB(class_prior=equal_priors))])

        self.estimator = estimator.fit(X, y)

        return self

    def predict(self, X):

        return self.predict_proba(X)

    def predict_proba(self, X):

        return self.estimator.predict_proba(X)

    def __tokenize(self, text):
        """Converts text to tokens."""
        tokens = word_tokenize(text, language='dutch')
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))

        return stemmed