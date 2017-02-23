import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD

from nltk.corpus import stopwords
from nltk.stem.snowball import DutchStemmer
from nltk import word_tokenize


class PartyClassifier:

    def __init__(self, y_labels=None):

        self.y_labels = y_labels
        self.vectorizer = None  # split vectorizer and estimator to catch zero matching tokens case
        self.estimator = None
        self.stemmer = DutchStemmer()  # initialize stemmer

    def fit(self, X, y):

        self.vectorizer = TfidfVectorizer(input='content', encoding='utf-8',
                                          decode_error='strict', strip_accents='unicode',
                                          lowercase=True, preprocessor=None, tokenizer=self.__tokenize,
                                          analyzer='word', stop_words=stopwords.words('dutch'),
                                          ngram_range=(1, 3), max_df=0.5, min_df=1, max_features=None,
                                          vocabulary=None, binary=False, dtype=np.int64,
                                          norm='l2', use_idf=True, smooth_idf=True, sublinear_tf=False)

        self.estimator = Pipeline(steps=[

            ('topic_model', TruncatedSVD(n_components=100, algorithm='randomized',
                                         n_iter=10, random_state=12, tol=0.0)),

            ('classifier', LogisticRegression(multi_class='multinomial', class_weight='balanced', solver='lbfgs'))

        ])

        self.estimator.fit(self.vectorizer.fit_transform(X), y)

        return self

    def predict(self, X):

        return self.predict_proba(X)

    def predict_proba(self, X):

        n_labels = len(self.y_labels)
        n_samples = len(X)

        X_vectorized = self.vectorizer.transform(X)

        # output equal probabilities in case of zero matching tokens
        if X_vectorized.getnnz() > 0:
            return self.estimator.predict_proba(X_vectorized)
        else:
            return np.ones([n_samples, n_labels]).astype(float) / n_labels

    def __tokenize(self, text):
        """Converts text to tokens."""
        tokens = word_tokenize(text, language='dutch')
        tokens = filter(lambda x: len(x) > 1, tokens)
        stemmed = []
        for item in tokens:
            stemmed.append(self.stemmer.stem(item))

        return stemmed