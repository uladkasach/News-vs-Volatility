'''
    given a dataframe with news data (including an id for each news article),
     generate a dataframe that lists by id each news article in the "News" column
'''
import argparse
import numpy as np
import pandas as pd
import datetime as dt
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
parser.add_argument('-l', '--path_ids', help='Path to Vol_Day Ids');
parser.add_argument('-n', '--path_news', metavar='PATH', help="Path to News Vectors")
parser.add_argument('-w', '--workers', metavar="D", type=int, default=1)
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## get data - filter out by date as well
print("reading ids");
vol_data = pd.read_hdf(args.path_ids, 'data');
print("reading news data");
news_data = pd.read_hdf(args.path_news, 'data');

## methods
def convert_ids_to_vectors(news):
    vectors = [];
    for id in news:
        this_vector = news_data.loc[[id]]["Vector"].item();
        vectors.append(this_vector);
    print(len(vectors));
    return vectors;

## for each day in volatility data, create a bag of words dict for words/frequencies found in that period
print("extracting full tokens for range")
data = vol_data; # rename dataframe now that we're going to be appending tokens for each date
if(args.workers == 1):
    tokens_result = data["News"].apply(convert_ids_to_vectors)
else:
    tokens_result = pandas_parallel.apply_by_multiprocessing(data["News"], convert_ids_to_vectors, workers=args.workers);
data["News"] = tokens_result;

## free news memory now that we no longer need that dataset
print("freeing news memory");
del news_data;

## remove NaN values
print("filtering out NaN values")
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len))

## reduce data
data = pd.DataFrame(data[["Date", "Volatility", "Label", "News"]]);
print(data);

## output the normalized data
file_name = args.path_ids.split("/")[-1];
file_name_no_ext = ".".join(file_name.split(".")[:-1])
file_path = "../data/vol_day/vectors.for_" + file_name_no_ext;
data.to_hdf(file_path+".hdf", "data", mode='w');
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
