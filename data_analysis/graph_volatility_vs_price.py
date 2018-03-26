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
parser.add_argument('path_historicals', help='Path to Historicals Data');
parser.add_argument('-v', '--path_volatilities', metavar='PATH', help="Path to Volatility Data")
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY');
parser.add_argument('-d', '--delta', action='store_true', help='Display changes (Delta) instead of absolute values')
args = parser.parse_args();

## get data
hist_data = pd.read_csv(args.path_historicals);
vol_data = pd.read_csv(args.path_volatilities);
data = pd.merge(hist_data, vol_data, on="Date")

## append DateFloat collumn
data['DateFloat'] = data['Date'].apply(lambda x: convert_to_date_float(x))

## calculate change in close price and change in volatility
data["DeltaClose"] = data["Close"] - data["Close"].shift(1); # Closed_i - Closed_(i+1)
data["PercentDeltaClose"] = data["DeltaClose"]/data["Close"]; # -> PercentDeltaClose = (Closed_i - Closed_(i+1))/Closed_i = 1 - Closed_(i+1)/Closed_i
data["DeltaVolatility"] = data["Volatility"] - data["Volatility"].shift(1);
data["PercentDeltaVolatility"] = data["DeltaVolatility"]/data["Volatility"];

#print(data["PercentDeltaClose"]);


## reduce date range to requested range
if(args.start_year is not None):
    date_to_start = convert_to_date_float(args.start_year+"-01-01"); # first day of the year
    data = data[data.DateFloat > date_to_start]
if(args.end_year is not None):
    date_to_end = convert_to_date_float(args.end_year+"-12-31"); # last day of the year
    data = data[data.DateFloat < date_to_end];

## plot the data
if(args.delta):
    if(False):
        ax = data.plot(x='DateFloat', y=['PercentDeltaClose', 'PercentDeltaVolatility'], kind='bar', color=['blue', 'red'])
    else:
        ax = data.plot(x='DateFloat', y='PercentDeltaClose', kind='line', style='b-',  marker='o')
        data.plot(x='DateFloat', y='PercentDeltaVolatility', kind='line', style='r-', marker='x', ax=ax, secondary_y=True)
else:
    ax = data.plot(x='DateFloat', y='Close', kind='line', style='b-',  marker='o')
    data.plot(x='DateFloat', y='Volatility', kind='line', style='r-', marker='x', ax=ax, secondary_y=True)
#data.plot(x='DateFloat', y='Volume', kind='line', style='g-', marker='x', ax=ax, secondary_y=True)
plt.show();

### READ: http://www.ccsenet.org/journal/index.php/ijef/article/viewFile/5894/4675%3Forigin%3Dpublication_detail
