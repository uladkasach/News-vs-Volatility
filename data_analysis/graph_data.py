import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates # used to parse x-axis values as dates
import csv
import argparse
import pandas as pd
import datetime as dt

'''
    example usage:
    python graph_data.py -n ../data/news/reuters.normalized.frequency.csv -v ../data/metrics/sp500.vol.nonlog.5.future.1990_to_2018.csv -i ../data/metrics/sp500.hist.1950_to_2018.csv -dv -dn
'''

## methods
def convert_to_date_float(date_string):
    return dt.datetime.strptime(date_string,'%Y-%m-%d').date()
def reduce_to_requested_date_range(data):
    ## reduce date range to requested range
    if(args.start_year is not None):
        date_to_start = (args.start_year+"-01-01"); # first day of the year
        data = data[data.Date > date_to_start]
    if(args.end_year is not None):
        date_to_end = (args.end_year+"-12-31"); # last day of the year
        data = data[data.Date < date_to_end];
    return data;

## parse arguments
parser = argparse.ArgumentParser(description='Graph Volatility -vs- Price');
parser.add_argument('-i', '--path_historicals', help='Path to Historicals Data');
parser.add_argument('-v', '--path_volatilities', metavar='PATH', help="Path to Volatility Data")
parser.add_argument('-n', '--path_news', metavar='PATH', help="Path to News Data")
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY');
parser.add_argument('-dc', '--close', action='store_true', help='display close prices')
parser.add_argument('-dr', '--returns', action='store_true', help='display returns')
parser.add_argument('-dv', '--volatility', action='store_true', help='display volatility')
parser.add_argument('-dn', '--news', action='store_true', help='display news')
args = parser.parse_args();

## get data - filter out by date as well
if(args.path_historicals != None):
    hist_data = pd.read_csv(args.path_historicals);
    hist_data = reduce_to_requested_date_range(hist_data);
else:
    hist_data = pd.DataFrame(columns=["Date"]);
if(args.path_volatilities != None):
    vol_data = pd.read_csv(args.path_volatilities);
    vol_data = reduce_to_requested_date_range(vol_data);
else:
    vol_data = pd.DataFrame(columns=["Date"]);
if(args.path_news != None):
    news_data = pd.read_csv(args.path_news);
    news_data = reduce_to_requested_date_range(news_data);
else:
    news_data = pd.DataFrame(columns=["Date"]);

## merge data based on Date
data = pd.DataFrame(columns=["Date"]);
data = pd.merge(data, hist_data,  on="Date", how='outer')
data = pd.merge(data, vol_data,  on="Date", how='outer')
data = pd.merge(data, news_data,  on="Date", how='outer')

## remove rows with null
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len));

## append DateFloat collumn
data['DateFloat'] = data['Date'].apply(lambda x: convert_to_date_float(x))

## calculate return
data["Return"] = (data["Close"] - data["Open"])/data["Open"]; ## percent change from open
data["LogReturn"] = np.log(np.abs(data["Return"]))

print(data);

## plot the data
fig, ax = plt.subplots();
is_secondary = False;
if(args.close):
    data.plot(x='DateFloat', y='Close', kind='line', style='b-',  marker='o', ax=ax, secondary_y=is_secondary)
    is_secondary = True;
if(args.returns):
    data.plot(x="DateFloat", y="Return", kind='line', style='g-',  marker='o', ax=ax, secondary_y=is_secondary)
    is_secondary = True;
if(args.volatility):
    data.plot(x="DateFloat", y="Volatility", kind='line', style='r-',  marker='x', ax=ax, secondary_y=is_secondary)
    is_secondary = True;
if(args.news):
    data.plot(x="DateFloat", y="Freq", kind='line', style='p',  marker='o', ax=ax, secondary_y=is_secondary)
    is_secondary = True;
plt.show();

### READ: http://www.ccsenet.org/journal/index.php/ijef/article/viewFile/5894/4675%3Forigin%3Dpublication_detail
