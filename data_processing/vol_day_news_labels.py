'''
    given a dataframe with vol_day/indicies (indicies for each news article),
    - generate a dataframe that records the probability of a news article being of a Label
        - e.g., if article used in 3 HIGH and 1 LOW vol_day, p(HIGH)=0.75, p(LOW)=0.25
'''
import argparse
import numpy as np
import pandas as pd
import datetime as dt
import pandas_util.parallel as pandas_parallel

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_indicies', help='Path to vol_day/indicies Labels');
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## read data
print("reading indicies")
data = pd.read_hdf(args.path_indicies, 'data');
print(data);

## extract by each row
print("extracting label frequencies");
frequencies = dict();
for index, row in data.iterrows():
    this_label = row["Label"];
    these_indicies = row["News"];
    for news_index in these_indicies:
        index_name = str(news_index);
        if(index_name not in frequencies): frequencies[index_name] = dict({"LOW":0, "MEDIUM":0, "HIGH":0});
        frequencies[index_name][this_label] += 1;
label_data = (pd.DataFrame.from_dict(frequencies, orient='index'));
print(label_data);

## define probabilities
print("appending label probabilities");
def prob_of_target_label(row, label):
    total = row["HIGH"] + row["MEDIUM"] + row["LOW"];
    target = row[label];
    probability = target/float(total);
    #print(probability);
    return probability;
label_data["pHIGH"] = label_data.apply(lambda row: prob_of_target_label(row, "HIGH"), axis=1);
label_data["pMEDIUM"] = label_data.apply(lambda row: prob_of_target_label(row, "MEDIUM"), axis=1);
label_data["pLOW"] = label_data.apply(lambda row: prob_of_target_label(row, "LOW"), axis=1);

## rename the data we're interested in - for keeping consistency with other files
data = label_data;

## output the normalized data
file_name = args.path_indicies.split("/")[-1];
file_name_no_ext = ".".join(file_name.split(".")[:-1])
file_path = "../data/vol_day/news_labels." + file_name_no_ext;
print("file_path: " + file_path)
data.to_hdf(file_path+".hdf", "data", mode='w');
if(args.readable_output):
    print("readable output");
    data.to_csv(file_path  + ".csv");
