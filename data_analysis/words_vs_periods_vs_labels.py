'''
    calculate normalized frequency of word for each label (HIGH, LOW) for each period (yearly, monthly)
'''
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
import pickle;


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
args = parser.parse_args();

## validate arguments
if(args.period not in ["all", "year", "month"]):
    print("period must be all, year, or month");
    exit();

## retreive data
print("reading data");
data = pd.read_hdf(args.path_data, 'data');
print("done reading data");

## extract year
data["Year"] = data["Date"].apply(lambda x: x[:4]);
#print(data);



## group dates by labels
datagroups = data.groupby(["Year", "Label"]);
#print(groups["Volatility"].mean());
#print(datagroups.groups.keys());

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
if(False): # extract from raw data
    group_data = dict({
        "LOW" : [],
        "HIGH" : [],
    })
    year_range = np.arange(int(args.start_year), int(args.end_year)+1, 1);
    valid_keys =  datagroups.groups.keys(); #[str(key) for key in datagroups.groups.keys()];
    for year in year_range:
        for label in ["LOW", "HIGH"]:
            key = (str(year), label);
            print(key);
            if(key not in valid_keys):
                print("`-> key " + str(key) + " not in valid keys");
                counts = pd.DataFrame(Counter().most_common(), columns=["Token", "Frequency"]);
            else:
                print("`-> key was found");
                counts = extract_frequency_dataframe(datagroups, key);
            print("`-> head was extracted")
            counts = counts.head(args.top); # keep only top x words for each
            group_data[label].append(counts);
    #print("saving group_data to pickle file");
    with open("_cache/words_vs_periods.group_data.pkl", "w+") as file:
        pickle.dump(group_data, file);
else:
    with open("_cache/words_vs_periods.group_data.pkl") as file:
        group_data = pickle.load(file);

## output comparison for each label
def compare_frames_of_years(years):
    ## merge data based on outer join
    comparison = pd.DataFrame(Counter().most_common(), columns=["Token", "Frequency"]);
    relevant_columns = [];
    for index, data_for_year in enumerate(years):
        if(len(data_for_year.index) == 0): continue;
        this_year = str(int(args.start_year) + index);
        relevant_columns.append("Frequency_" + this_year);
        comparison = pd.merge(comparison, data_for_year, on="Token", how='outer', suffixes=["", "_"+this_year]);
    comparison = comparison.fillna(0); # replace NaN with 0

    ## caclulate standard deviation of frequencies - metric of comparison
    print(relevant_columns);
    comparison["StandardDeviation"] = comparison.apply(lambda row: np.array(row[relevant_columns]).std(), axis=1)
    comparison["Mean"] = comparison.apply(lambda row: np.array(row[relevant_columns]).mean(), axis=1)

    ## calculate a naive score which we can rank terms by
    # with mean = 1, stdev = -1, score = mean - standard deviation -> ranks low standard deviation high mean ones
    comparison["MeanMinusStdev"] = comparison.apply(lambda row: row["Mean"] - row["StandardDeviation"], axis=1 )

    ## drop the orig frequency column - used for prefixing
    comparison = comparison.drop("Frequency", axis=1)

    ## sort by MeanMinusStdev
    comparison = comparison.sort_values(by=['MeanMinusStdev'], ascending=False)

    ## return result
    return comparison;
print("computing high comparison...");
high_comparison = compare_frames_of_years(group_data["HIGH"]);
print("computing low comparison...");
low_comparison = compare_frames_of_years(group_data["LOW"]);

## compare lables
print("computing full comparison");
full_comparison = pd.merge(high_comparison[["Token","MeanMinusStdev"]], low_comparison[["Token","MeanMinusStdev"]], on="Token", how='outer', suffixes=["_HIGH", "_LOW"])
full_comparison = full_comparison.fillna(0); # replace NaN with 0

## define output name bases
file_path = args.path_data.split("/")[-1];
file_base = ".".join(file_path.split(".")[:-1])
file_args_modifier = args.start_year+"_to_"+args.end_year+".top_"+str(args.top);

## output period comparisons
high_comparison.to_csv("results/compare/periods.HIGH."+file_args_modifier+".csv");
low_comparison.to_csv("results/compare/periods.LOW."+file_args_modifier+".csv");

## compute and output label comparisons
print("outputting comparisons");
if(True):
    ## compute
    print("computing difference");
    def compute_difference(row):
        difference = row["MeanMinusStdev_HIGH"] - row["MeanMinusStdev_LOW"];
        return difference;
    full_comparison["Difference"] = full_comparison.apply(lambda row: compute_difference(row), axis=1);

    ## sort by difference descending
    print("sorting by difference");
    comparison = full_comparison.sort_values(by=['Difference'], ascending=False)

    ## output
    print("recording difference");
    comparison.to_csv("results/compare/periods.labels.difference."+file_args_modifier+".csv");


## compute and record ratio
if(True):
    ## compute
    print("computing ratio");
    def compute_ratio(row):
        if(row["MeanMinusStdev_LOW"] == 0):
            ratio = float("inf");
        else:
            ratio = row["MeanMinusStdev_HIGH"]/row["MeanMinusStdev_LOW"];
        return ratio;
    full_comparison["Ratio"] = full_comparison.apply(lambda row: compute_ratio(row), axis=1);

    ## sort
    print("sorting by Ratio");
    comparison = full_comparison.sort_values(by=['Ratio'], ascending=False)

    ## output
    print("recording Ratio");
    comparison.to_csv("results/compare/periods.labels.ratio."+file_args_modifier+".csv");
