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
import nltk
import re


## methods
def extract_date(timestamp):
    date = timestamp[0:10];
    return date;

## parse arguments
parser = argparse.ArgumentParser(description='Analyze News');
parser.add_argument('path_news', help='Path to Normalized News Data');
args = parser.parse_args();


## get news data
print("loading data");
data = pd.read_csv(args.path_news);
data = data.drop('URL', 1)
data = data.drop('Catagory', 1)

## extract Date  and Time from Timestamp
print("extracting `Date` field")
data["Date"] = data["TimeStamp"].apply(lambda x: extract_date(x));

## tokenize each title
def tokenize_title(title):
    letters_only = re.sub("[^0-9a-zA-Z\.]", " ", title) # remove non alphanumeric
    tokens = nltk.word_tokenize(letters_only);
    return tokens;
print("extracting `Tokens` from title")
data["Tokens"] = data["Title"].apply(tokenize_title)

## output the normalized data
file_name = args.path_news.split("/")[-1];
dir_path = "/".join(args.path_news.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, "tokens");
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;
data.to_csv(file_path, columns=["Date", "Tokens", "URL"], index=False)
