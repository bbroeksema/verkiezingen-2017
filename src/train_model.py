import pickle
import dill
import nltk

import json
import pandas as pd
import numpy as np

from src.models import PartyClassifier


def chunk_string(string, chunk_size=1000, overlap=0):
    return [string[i:i + chunk_size - overlap + 1] for i in range(0, len(string), chunk_size - overlap)]


def load_data():

    with open('../data/partijen-metadata.json', 'r') as f:
        meta = json.load(f)

    party_dict = {}
    for party_data in meta['partijen']:
        party_id = party_data['lijst']
        party_name = party_data['naam'].encode('utf-8')
        party_dict["{:02d}".format(party_id)] = party_name

    raw = pd.read_csv('../data/processed/dataframe.csv')
   # raw['file'] = raw['file'].replace(to_replace=party_dict, regex=True)
   # raw['file'] = map((lambda x: x.split('-')[1]), raw['file'])
    raw['file'].replace(to_replace=party_dict, regex=True).apply(lambda x: str(x).split("-")[0])
    raw.rename(columns={'file': 'party'}, inplace=True)

    return raw


def preprocess_data(raw):
    df = raw['text'].apply(lambda x: pd.Series(chunk_string(x, chunk_size=600, overlap=0))).stack().reset_index()
    df.rename(columns={0: 'text', 'level_0': 'party', 'level_1': 'snippet'}, inplace=True)

    print("\t{:d} text snippets".format(len(df)))
#    print("\t{:d} charachters in corpus".format(df['text'].apply(len).sum()))

    return df


if __name__ == "__main__":

    print("Downloading nltk data")
    nltk.download("stopwords")
    nltk.download("punkt")

    print("loading data")
    raw = load_data()

    party_labels = raw['party'].values

    print("creating snippets")
    df = preprocess_data(raw)

    X = df['text'].values
    y = np.array(df['party'])

    estimator = PartyClassifier(y_labels=party_labels)
    print("fitting estimator")
    estimator.fit(X, y)

    print("saving estimator")
    model_filename = '../models/PartyClassifier.pkl'
    pickle.dump(estimator, open(model_filename, "wb"), protocol=2)
