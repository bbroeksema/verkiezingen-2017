import pandas as pd
import os
import glob
from textract import process
import re


def read_pdf(file_names, verbose=False):
    data = {}
    for f in file_names:
        text = None
        try:
            text = process(f)
        except TypeError:
            print("Could not parse {:s}".format(f))
            pass

        if text is not None:
            data[f] = text
            if verbose:
                print("Successfully parsed program of party {:s}".format(f))

    return data


def clean_text(text):
    text = text.lower()
    text = re.sub('\n', ' ', text)  # remove line endings
    text = re.sub(r'[^\w\']', ' ', text)  # remove non-alpha numeric
    text = re.sub(r'[0-9 ]', ' ', text)  # remove numbers
    return text


def pdf_to_df(data_dir):

    files = glob.glob(os.path.join(data_dir, "*.pdf"))

    raw = read_pdf(files)

    df = pd.DataFrame.from_dict(raw, orient='index')
    df.reset_index(inplace=True)
    df.rename(columns={0: 'text', 'index': 'file'}, inplace=True)
    df['text'] = df['text'].str.normalize('NFKD').apply(clean_text)

    return df


