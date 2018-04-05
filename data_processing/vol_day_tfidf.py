'''
    calculate frequency for each volatility day
        - removes word order
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt
import ast
import pandas_util.parallel as pandas_parallel
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD


## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_text', help='Path to vol_day/text...flat.hdf');
parser.add_argument('-w', '--workers', metavar="D", type=int, default=2);
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## retreive data
data = pd.read_hdf(args.path_text,'data');

## clean the data
data = data.drop("index", axis=1);

## remove rows with null
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len));

## reset index so that now index of dataframe correlates with index of corpus output in next part
data = data.reset_index(drop=True)

## extract corpus from data
corpus = data["Text"].tolist();
print("documents : " + str(len(corpus)));

## calculate tf-idf for corpus
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 3, stop_words = 'english'); # dont consider words that occur less than 3 times
print("fitting tfidf to corpus");
tfidf_matrix =  tfidf.fit_transform(corpus)
feature_names = tfidf.get_feature_names()

## reduce dimensionality with SVD (- this results in us running LSA since LSA = TF-IDF + SVD)
print("reducing dimensionality");
svd = TruncatedSVD(n_components=400, n_iter=7);
lsa_matrix = svd.fit_transform(tfidf_matrix)

## append the vector of each row to the data
def grab_vector_for_row(row):
    vector = (lsa_matrix[row.name, :]);
    vector = list(vector);
    print(vector);
    return vector;
data["Vector"] = data.apply(grab_vector_for_row, axis = 1);

## drop the text column
data = data.drop("Text", axis=1);

## output the normalized data
file_name = args.path_text.split("/")[-1];
dir_path = "/".join(args.path_text.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts[0] = "tfidf.svd"; # replace text w/ tfidf.svd
name_parts = name_parts[:-1]; # drop extension
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;

data.to_hdf(file_path + ".hdf", "data", mode="w");
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
