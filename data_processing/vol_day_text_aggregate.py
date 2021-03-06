'''
    calculate frequency for each volatility day from tokens list
        - removes word order
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


## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_labels', help='Path to tokens_for_each_vol');
parser.add_argument('-w', '--workers', metavar="D", type=int, default=2);
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## retreive data
data = pd.read_hdf(args.path_labels,'data');

## flatten texts array into one large string
def flatten_texts(texts):
    if(len(texts) == 0): return None;
    full_text = "";
    for text in texts:
        full_text += text + ". ";
    return full_text;
data["Text"] = data["Texts"].apply(lambda texts: flatten_texts(texts)) # store the counter directly

## drop the texts data
data = data.drop("Texts", axis=1);

## remove rows with null
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len));

## output the normalized data
file_name = args.path_labels.split("/")[-1];
dir_path = "/".join(args.path_labels.split("/")[:-1]);
name_parts = file_name.split(".");
name_parts.insert(-1, 'flat' );
name_parts = name_parts[:-1]; # drop extension
file_name = ".".join(name_parts);
file_path = dir_path + "/" + file_name;

data.to_hdf(file_path + ".hdf", "data", mode="w");
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv", index=False);
