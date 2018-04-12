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
parser.add_argument('-n', '--path_news', metavar='PATH', help="Path to News Vectors")
parser.add_argument('-l', '--path_labels', help='Path to Volatility Labels');
parser.add_argument('-w', '--workers', metavar="D", type=int, default=1)
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## get data - filter out by date as well
print("reading news vectors");
news_data = pd.read_hdf(args.path_news, 'data');
print("reading labels");
labels_data = pd.read_hdf(args.path_labels, 'data');

## map news_data index to string - since its originally int and labels is originally string
news_data.index = news_data.index.map(str);

## for each labeled news data, get the vector
data = labels_data;
def retreive_vector(row):
    news_index = row.name;
    try:
        news_row = news_data.loc[news_index];
    except:
        #print("could not find id " + str(news_index));
        return None;
    news_vector = news_row["Vector"];
    #print("found " + str(news_index));
    return news_vector;
print("extracting vectors for each label");
data["Vector"] = data.apply(lambda row: retreive_vector(row), axis=1);

## remove NaN values
print("filtering out NaN values")
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len))



## output the normalized data
file_name = args.path_labels.split("/")[-1];
file_name_no_ext = ".".join(file_name.split(".")[:-1])
file_path = "../data/news/vol_day_labeled_vectors." + file_name_no_ext;
print("file_path: " + file_path)
data.to_hdf(file_path+".hdf", "data", mode='w');
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
