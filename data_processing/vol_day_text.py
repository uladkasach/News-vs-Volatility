'''
    list all text for each volatility day
        - uses non-tokenized news
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

## methods
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()
def reduce_to_requested_date_range(data, date_to_start, date_to_end):
    ## reduce date range to requested range
    data = data[data.Date >= date_to_start]
    data = data[data.Date <= date_to_end];
    return data;

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('-l', '--path_labels', help='Path to Volatility Labels');
parser.add_argument('-n', '--path_news', metavar='PATH', help="Path to News Data")
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "2018");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
parser.add_argument('-w', '--workers', metavar="D", type=int, default=2)
parser.add_argument('-p', '--period', metavar='DAYS', type=int, default=2);
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## get data - filter out by date as well
date_to_start = (args.start_year+"-01-01"); # first day of the year
date_to_end = (args.end_year+"-12-31"); # last day of the year
print("reading vol_data");
vol_data = pd.read_csv(args.path_labels);
vol_data = reduce_to_requested_date_range(vol_data, date_to_start, date_to_end);
print("reading news data");
news_data = pd.read_csv(args.path_news);
news_data["Date"] = news_data["TimeStamp"].apply(lambda timestamp: timestamp[:10]); ## extract date from timestamp
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
    full_text = relevant_news["Title"].tolist();

    ## increment counter and output result for this thread
    if(this_day % 10 == 0):
        print("on day " + str(this_day) + " out of " + str(total_days));
    global this_day;
    this_day += 1;

    ## return result
    return full_text;


## for each day in volatility data, create a bag of words dict for words/frequencies found in that period
print("extracting full tokens for range")
data = vol_data; # rename dataframe now that we're going to be appending tokens for each date
date_to_start = convert_to_date_float(date_to_start);
date_to_end = convert_to_date_float(date_to_end);
days_to_subtract = args.period;
total_days = len(data.index);
this_day = 0;
def applicator(date):
    result = extract_full_tokens(date, days_to_subtract, date_to_start, date_to_end); ## get full_tokens
    return result; ## return result
if(args.workers == 1):
    tokens_result = data["Date"].apply(lambda date: applicator(date))
else:
    tokens_result = pandas_parallel.apply_by_multiprocessing(data["Date"], applicator, workers=args.workers);
data["Texts"] = tokens_result;
print(data["Texts"]);

## remove NaN values
print("filtering out NaN values")
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len))

## reduce data
#data = pd.DataFrame(data[["Date", "Volatility", "Label", "Tokens"]]);

## output the normalized data
file_path = "../data/vol_day/text."+str(args.period) + "_days_before." + args.start_year + "_to_" + args.end_year;
data.to_hdf(file_path+".hdf", "data", mode='w');
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
