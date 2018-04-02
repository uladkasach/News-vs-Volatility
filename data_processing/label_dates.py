import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt

## methods
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()

## parse arguments
parser = argparse.ArgumentParser(description='Graph Volatility -vs- Price');
parser.add_argument('path_volatility', help='Path to Volatility');
parser.add_argument('-lt', '--low_threshold', metavar='NUM', default ="abs volatility threshold");
parser.add_argument('-ht', '--high_threshold', metavar='NUM', default="abs volatility threshold");
args = parser.parse_args();

## get historicals data
data = pd.read_csv(args.path_volatility);

## append DateFloat collumn
data['DateFloat'] = data['Date'].apply(lambda x: convert_to_date_float(x))

## calculate whether volatility was LOW, MED, or HIGH
def determine_label(volatility):
    if(volatility > args.high_threshold):
        return "HIGH";
    elif(volatility > args.low_threshold):
        return "MEDIUM";
    else:
        return "LOW";
data["Label"] = data["Volatility"].apply(lambda x: determine_label(x));
print(data);

# export dataframe to cv
volatility_dataframe.to_csv("../data/sp500.vol.nonlog."+str(args.volatility_period)+"."+args.direction+"."+args.start_year + "_to_" + args.end_year+".csv")
