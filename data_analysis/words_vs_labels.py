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
parser = argparse.ArgumentParser(description='Graph Volatility -vs- Price');
parser.add_argument('path_data', help='Path to Combined Tokens and Volatility Data');
parser.add_argument('-p', '--period', help='period which to compare: all, year, or month', default="all");
parser.add_argument('-t', '--top', type = int, help ='how many to keep when comparing relevant words. default = 300', default=300 )
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY', default = "2018");
parser.add_argument('-w', '--workers', metavar='D', type=int, default=2);
parser.add_argument('-c', '--chunk_size', metavar='D', help='chunk size', type=int, default=500)
args = parser.parse_args();

## validate arguments
if(args.period not in ["all", "year", "month"]):
    print("period must be all, year, or month");
    exit();

## retreive data
print("reading data");
data = pd.read_hdf(args.path_data, 'data');
print("done reading data");


## group dates by labels
datagroups = data.groupby("Label");
#print(groups["Volatility"].mean());
#print(datagroups.groups);

## extract word frequency counts for each group from groups
def extract_frequency_dataframe(datagroups, section_label):
    section = datagroups.get_group(section_label); # select the group
    print("`-> summing frequencies")
    frequency = section["Freq"].sum()
    print("`-> converting to df")
    counts = pd.DataFrame(frequency.most_common(), columns=["Token", "Frequency"]); # cast frequencies to dataframe
    print("`-> getting total")
    total = counts["Frequency"].sum();
    print("`-> normalizing")
    counts["Frequency"] = counts["Frequency"].apply(lambda x: x/float(total))
    print("`-> sorting")
    counts = counts.sort_values(by=['Frequency'], ascending=False)
    return counts # return result
print(datagroups.groups.keys())
print("extracting high counts")
high_counts = extract_frequency_dataframe(datagroups, "HIGH");
print("extracting low counts");
low_counts = extract_frequency_dataframe(datagroups, "LOW");

## keep only top X words for each
print("extracting heads");
high_counts = high_counts.head(args.top);
low_counts = low_counts.head(args.top);

## merge based on outer join
print("merging counts");
comparison_counts = pd.merge(high_counts, low_counts,  on="Token", how='outer')
comparison_counts = comparison_counts.fillna(0); # replace NaN with 0

## define output name bases
file_path = args.path_data.split("/")[-1];
file_base = ".".join(file_path.split(".")[:-1])
file_args_modifier = args.start_year+"_to_"+args.end_year+".top_"+str(args.top);


## compute and record difference
print("outputting comparisons");
if(True):
    ## compute
    print("computing difference");
    def compute_difference(row):
        difference = row["Frequency_x"] - row["Frequency_y"];
        return difference;
    comparison_counts["Difference"] = comparison_counts.apply(lambda row: compute_difference(row), axis=1);

    ## sort by difference descending
    print("sorting by difference");
    comparison = comparison_counts.sort_values(by=['Difference'], ascending=False)

    ## output
    print("recording difference");
    comparison.to_csv("results/compare/labels.difference."+file_args_modifier+".csv");


## compute and record ratio
if(True):
    ## compute
    print("computing ratio");
    def compute_ratio(row):
        if(row["Frequency_y"] == 0):
            ratio = float("inf");
        else:
            ratio = row["Frequency_x"]/row["Frequency_y"];
        return ratio;
    comparison_counts["Ratio"] = comparison_counts.apply(lambda row: compute_ratio(row), axis=1);

    ## sort
    print("sorting by Ratio");
    comparison = comparison_counts.sort_values(by=['Ratio'], ascending=False)

    ## output
    print("recording Ratio");
    comparison.to_csv("results/compare/labels.ratio."+file_args_modifier+".csv");
