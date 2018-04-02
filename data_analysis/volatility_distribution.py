'''
    assess the distribution of volatility.
        - e.g., is it normal?
            - if so what are its parameters
'''
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
parser = argparse.ArgumentParser();
parser.add_argument('path_volatility', help='Path to Volatility');
args = parser.parse_args();

## get historicals data
data = pd.read_csv(args.path_volatility);

## append DateFloat collumn
data['DateFloat'] = data['Date'].apply(lambda x: convert_to_date_float(x))

## define data as vol data
vol_data = data["Volatility"];

## plot histogram
if(False):
    plt.hist(vol_data);
    plt.show();
    # VERY SKEWED


## calculate standard distribution and mean
stdev = vol_data.std();
mean = vol_data.mean();
print("mean : " + str(mean) + ", stdev : " + str(stdev))

## define medium threshold and high threshold based on mean and stdev
med_thres = mean + 0*stdev;
high_thres = mean + 1.25*stdev;
print("low  : [0, " + str(med_thres) +"]");
print("med  : ["+ str(mean) +", " + str(high_thres)+"]");
print("high : [" + str(high_thres) + ", +inf]");

## count the number of elements in each bin
counts = dict({
    "low" : 0,
    "med" : 0,
    "high" : 0,
})
for vol in vol_data:
    if(vol > high_thres):
        counts["high"] += 1;
    elif(vol > med_thres):
        counts["med"] += 1;
    else:
        counts["low"] += 1;
print(counts);


## plot the threshold on the volatility graph
ax = data.plot(x="DateFloat", y="Volatility", style = "bo");
plt.axhline(y=med_thres, color='y', linestyle='-')
plt.axhline(y=high_thres, color='r', linestyle='-')
plt.show()
