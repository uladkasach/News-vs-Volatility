'''
    assess whether certain words occur more often X days before each label
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt
import ast


## methods
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()
def reduce_to_requested_date_range(data, date_to_start, date_to_end):
    ## reduce date range to requested range
    data = data[data.Date >= date_to_start]
    data = data[data.Date <= date_to_end];
    return data;

## parse arguments
parser = argparse.ArgumentParser(description='Graph Volatility -vs- Price');
parser.add_argument('-l', '--path_labels', help='Path to Volatility Labels');
parser.add_argument('-n', '--path_news', metavar='PATH', help="Path to News Data")
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "2015");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
parser.add_argument('-p', '--period', metavar='DAYS', type=int, default=2);
args = parser.parse_args();

## get data - filter out by date as well
date_to_start = (args.start_year+"-01-01"); # first day of the year
date_to_end = (args.end_year+"-12-31"); # last day of the year
vol_data = pd.read_csv(args.path_labels);
vol_data = reduce_to_requested_date_range(vol_data, date_to_start, date_to_end);
news_data = pd.read_csv(args.path_news);
news_data = reduce_to_requested_date_range(news_data, date_to_start, date_to_end);

## methods
def extract_full_tokens(day, days_to_subtract, date_to_start, date_to_end):
    ## extract start and end date from
    target_date = convert_to_date_float(day);
    start_date = target_date - dt.timedelta(days=days_to_subtract)
    end_date = target_date - dt.timedelta(days=1); # day before, so we dont get news from the day we're predicting - only prior

    ## validate the date range
    if(start_date < date_to_start): return None; # start date is not after date to start - we wont have all data
    if(end_date > date_to_end): return None; # end date is not after date to end - we wont have all data

    # retreive all elements within this range
    relevant_news = reduce_to_requested_date_range(news_data, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'));

    # retreive all tokens from the relevant articles
    full_tokens = [];
    for tokens in relevant_news["Tokens"].tolist():
        tokens = ast.literal_eval(tokens);
        full_tokens.extend(tokens);

    return full_tokens;


## for each day in volatility data, create a bag of words dict for words/frequencies found in that period
data = vol_data; # rename dataframe now that we're going to be appending tokens for each date
date_to_start = convert_to_date_float(date_to_start);
date_to_end = convert_to_date_float(date_to_end);
days_to_subtract = args.period;
data["Tokens"] = data["Date"].apply(lambda date: extract_full_tokens(date, days_to_subtract, date_to_start, date_to_end))
