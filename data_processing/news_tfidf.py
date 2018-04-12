'''
    normalization:
    1. load all data into pandas
    2. cast "date" field into readable date
    3. extract "catagory" from url of reuters news
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

## methods
def extract_date(timestamp):
    date = timestamp[0:10];
    return date;
def reduce_to_requested_date_range(data, date_to_start, date_to_end):
    ## reduce date range to requested range
    data = data[data.Date >= date_to_start]
    data = data[data.Date <= date_to_end];
    return data;

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_news', help='Path to Normalized News Data');
parser.add_argument('-d', '--dimensionality', metavar="D", type=int, default=300);
parser.add_argument('-m', '--min_freq', metavar="D", type=int, default=3);
parser.add_argument('-r', '--readable_output', action='store_true');
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "2018");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
args = parser.parse_args();

## get news data
print("loading data");
data = pd.read_csv(args.path_news);
data = data.drop('URL', 1)
data = data.drop('Catagory', 1)

## extract Date  and Time from Timestamp
print("extracting `Date` field")
data["Date"] = data["TimeStamp"].apply(lambda x: extract_date(x));

## filter news by date
date_to_start = (args.start_year+"-01-01"); # first day of the year
date_to_end = (args.end_year+"-12-31"); # last day of the year
data = reduce_to_requested_date_range(data, date_to_start, date_to_end);

# documents : 2730187 - 2014
# documents : 106438 - 2018

## remove rows with null
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
filt_len = len(data.index);
print("n/a dates filtered out: " + str(orig_len - filt_len));

## reset index so that now index of dataframe correlates with index of corpus output in next part
data = data.reset_index(drop=True)

## extract corpus from data
corpus = data["Title"].tolist();
print("documents : " + str(len(corpus)));

## calculate tf-idf for corpus
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = args.min_freq, stop_words = 'english'); # dont consider words that occur less than 3 times
print("fitting tfidf to corpus");
tfidf_matrix =  tfidf.fit_transform(corpus)
feature_names = tfidf.get_feature_names()
print("features : " + str(len(feature_names)))
# features : 114790
# features : 829147 p 2o16


## reduce dimensionality with SVD (- this results in us running LSA since LSA = TF-IDF + SVD)
print("reducing dimensionality");
svd = TruncatedSVD(n_components=args.dimensionality, n_iter=7);
lsa_matrix = svd.fit_transform(tfidf_matrix)

## append the vector of each row to the data
def grab_vector_for_row(row):
    vector = (lsa_matrix[row.name, :]);
    vector = list(vector);
    #print(vector);
    return vector;
data["Vector"] = data.apply(grab_vector_for_row, axis = 1);

## drop the title from dataframe
data = data.drop("Title", axis=1);

## output the vectorized data
file_name = args.path_news.split("/")[-1];
dir_path = "/".join(args.path_news.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, "tfidf.svd.dim_"+str(args.dimensionality)+"."+args.start_year+"_to_"+ args.end_year);
name_parts = name_parts[:-1]; # drop extension
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;

data.to_hdf(file_path + ".hdf", "data", mode="w");
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
