'''
    analysis:
    1. load all data into pandas
    2. cast "date" field into readable date
    3. extract "catagory" from url of reuters news
    4. assess frequency of news / day
    5. assess frequency of each catagory of news / day
'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt
import pytz


## methods

'''
    Normalize TimeStamp
'''
utc=pytz.utc
eastern=pytz.timezone('US/Eastern')
fmt='%Y-%m-%d %H:%M:%S %Z'
def normalize_timestamp(timestamp):
    # check that it is a string, if not, not valid
    if(type(timestamp) != str): # timestamp must be a string
        print("(!) invalid timestamp: " + str(timestamp))
        return None;

    # extract parts
    time_parts = timestamp.split(" ");
    if(len(time_parts) == 3):
        time_magnitude = time_parts[0].split("\xc2\xa0")[1];
        time_qualifier = time_parts[1];
        time_zone = time_parts[2];
    elif(len(time_parts) == 2):
        time_magnitude = time_parts[0][-7:-2];
        try: ## cast terms like `X7:07` to `07:07` where X is a non Ascii character
            int(time_magnitude[0])
        except:
            time_magnitude = list(time_magnitude)
            time_magnitude[0] = "0";
            time_magnitude = ''.join(time_magnitude);
        time_qualifier = time_parts[0][-2:];
        time_zone = time_parts[1];
    else:
        print("(!) invalid timestamp: " + str(timestamp))
        return None;

    # convert to 24hr
    hours = int(time_magnitude.split(":")[0]);
    minutes = int(time_magnitude.split(":")[1]);
    if(time_qualifier == "PM" and hours != 12):
        hours = hours + 12;
    time_magnitude = format(hours, '02') + ":" + format(minutes, '02');

    # convert to UTC
    date_string = timestamp[0:8];
    time_string = timestamp[0:8] + " " + time_magnitude+" " + time_zone;
    date = dt.datetime.strptime(time_string,'%Y%m%d %H:%M %Z')
    if(time_zone == "UTC"):
        date_utc=utc.localize(date,is_dst=None)
        date_utc=date_utc.astimezone(utc)
    elif(time_zone == "EDT"):
        date_eastern=eastern.localize(date, is_dst=True)
        date_utc=date_eastern.astimezone(utc)
    elif(time_zone == "EST"):
        date_eastern=eastern.localize(date, is_dst=False)
        date_utc=date_eastern.astimezone(utc)
    else:
        print("timezone not valid: " + time_zone + " for " + timestamp);
        exit();
    normalized_timestamp = date_utc.strftime(fmt)

    # return the time
    return normalized_timestamp;


def extract_catagory_from_url(url):
    catagory = url.split("/")[-2];
    return catagory;


## parse arguments
parser = argparse.ArgumentParser(description='Analyze News');
parser.add_argument('path_news', help='Path to News Data');
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
args = parser.parse_args();

## get news data
print("loading data");
data = pd.read_csv(args.path_news, sep='\t', index_col=[0], names = ["index", "TimeStamp", "Title", "URL"]);

## extract Date  and Time from Timestamp
print("normalizing `TimeStamp` field")
data["TimeStamp"] = data["TimeStamp"].apply(lambda x: normalize_timestamp(x));

## filter out fields that have an invalid timestamp
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
filt_len = len(data.index);
print("news filtered out: " + str(orig_len - filt_len));

## extract catagory from url
print("creating `Catagory` field")
data["Catagory"] = data["URL"].apply(lambda x: extract_catagory_from_url(x));

## sort by timestamp
print("sorting by timestamp")
data.sort_values(by=['TimeStamp'])

## output the normalized data
file_name = args.path_news.split("/")[-1];
dir_path = "/".join(args.path_news.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, "normalized");
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;
data.to_csv(file_path, columns=["TimeStamp", "Catagory", "Title", "URL"], index=False)
