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
from collections import Counter


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
parser.add_argument('path_data', help='Path to Combined Tokens and Volatility Data');
args = parser.parse_args();

## retreive data
data = pd.read_csv(args.path_data);

## cast tokens to list tokens - from ast strings
if(True):
    data["Tokens"] = data["Tokens"].apply(lambda tokens: ast.literal_eval(tokens));
    #print(data["Tokens"].tolist()[0][0]);

## group dates by labels
datagroups = data.groupby("Label");
#print(groups["Volatility"].mean());
#print(datagroups.groups);

## extract tokens for each group from groups
def extract_tokens(datagroups, section_label):
    section = datagroups.get_group(section_label)
    tokens_lists = section["Tokens"].tolist();
    tokens = [item for sublist in tokens_lists for item in sublist];
    return tokens;
high_tokens = extract_tokens(datagroups, "HIGH");
low_tokens = extract_tokens(datagroups, "LOW");
print(len(high_tokens));
print(len(low_tokens));

## calculate frequency of each word
high_counts = Counter(high_tokens)
print(high_counts.most_common(100))

low_counts = Counter(low_tokens)
print(low_counts.most_common(100))
