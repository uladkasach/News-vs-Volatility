'''
    analysis:
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
def extract_date(timestamp):
    date = timestamp[0:10];
    return date;
def extract_time(timestamp):
    time = timestamp[11:16];
    return time;
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()

## parse arguments
parser = argparse.ArgumentParser(description='Analyze News');
parser.add_argument('path_news', help='Path to News Data');
parser.add_argument('-p', '--plot', action='store_true', help='plot the frequency')
args = parser.parse_args();

## get news data
print("loading data");
data = pd.read_csv(args.path_news);

## extract Date  and Time from Timestamp
print("extracting `Date` field")
data["Date"] = data["TimeStamp"].apply(lambda x: extract_date(x));
print("extracting `Time` field")
data["Time"] = data["TimeStamp"].apply(lambda x: extract_time(x));

## calculate frequency of news on each date
frequency_data = pd.DataFrame({'Freq' : data.groupby( [ "Date"] ).size()}).reset_index();

## output the frequency data
file_name = args.path_news.split("/")[-1];
dir_path = "/".join(args.path_news.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, "frequency");
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;
frequency_data.to_csv(file_path, columns=["Date", "Freq"], index=False)

## plot if requested
if(args.plot):
    ## append DateFloat column
    frequency_data['DateFloat'] = frequency_data['Date'].apply(lambda x: convert_to_date_float(x))
    print(frequency_data);

    ## plot the frequency
    ax = frequency_data.plot(x="DateFloat", y="Freq", kind='line', style='b-',  marker='o')

    ## show plot
    plt.show();
