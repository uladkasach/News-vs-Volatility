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
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()
def extract_date(timestamp):
    date = timestamp[0:10];
    return date;
def reduce_to_requested_date_range(data):
    ## reduce date range to requested range
    if(args.start_year is not None):
        date_to_start = (args.start_year+"-01-01"); # first day of the year
        data = data[data.Date > date_to_start]
    if(args.end_year is not None):
        date_to_end = (args.end_year+"-12-31"); # last day of the year
        data = data[data.Date < date_to_end];
    return data;


## parse arguments
parser = argparse.ArgumentParser(description='Analyze News');
parser.add_argument('path_news', help='Path to Normalized News Data');
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
args = parser.parse_args();

## get news data
print("loading data");
data = pd.read_csv(args.path_news);


## reduce date range to requested range
print("filtering by date range")
data = reduce_to_requested_date_range(data);

## output the normalized data
file_name = args.path_news.split("/")[-1];
dir_path = "/".join(args.path_news.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, args.start_year + "_to_"+ args.end_year );
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;
data.to_csv(file_path, columns=["Date", "Tokens", "URL"], index=False)
