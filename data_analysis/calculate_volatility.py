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
parser.add_argument('path_historicals', help='Path to Historicals');
parser.add_argument('-p', '--volatility_period', metavar="DAYS", type=int, default=5);
parser.add_argument('-s', '--start_year', metavar='YYYY', default = "1990");
parser.add_argument('-e', '--end_year', metavar='YYYY', default="2018");
parser.add_argument('-d', '--direction', metavar="[past, future, center]", default="back", help="Direction to count volatility for. E.g., past -> past DAYS days")
args = parser.parse_args();

## validate arguments
direction_options_whitelist=["past", "future"]; ## TODO - implement 'center'
if (args.direction not in direction_options_whitelist):
    print("args must be " + " or ".join(["'"+string+"'" for string in direction_options_whitelist]) )
    exit();

## get historicals data
data = pd.read_csv(args.path_historicals);

## append DateFloat collumn
data['DateFloat'] = data['Date'].apply(lambda x: convert_to_date_float(x))

## reduce date range to requested range
if(args.start_year is not None):
    date_to_start = convert_to_date_float(args.start_year+"-01-01"); # first day of the year
    data = data[data.DateFloat > date_to_start]
if(args.end_year is not None):
    date_to_end = convert_to_date_float(args.end_year+"-12-31"); # last day of the year
    data = data[data.DateFloat < date_to_end];

## calculate volatility
def return_close_prices_based_on_trading_days(date, period_in_days, direction, data):
    # TODO - handle case where we have more than one data row per date (intraday data)

    # 1. get index of this date, target_index
    target_index = data["Date"].tolist().index(date);

    # 2. get list of Closed prices to consider - prices[target_index-period_in_days:target_index]
    if(direction == "past"):
        start_index = target_index-period_in_days;
        if(start_index < 0): start_index = 0;
        end_index = target_index;
    if(direction == "future"):
        start_index = target_index;
        end_index = target_index + period_in_days;
        if(end_index > len(data.index)-1): end_index = len(data.index)-1;

    close_prices = data["Close"].tolist()[start_index:end_index];

    # 3. get period_start and period_end
    period_start = data["Date"].tolist()[start_index]
    period_end = data["Date"].tolist()[end_index]


    # 4. return close prices
    return [np.array(close_prices), period_start, period_end];

def calculate_volatility_for(date, period_in_days, direction, data): # data should be a dataframe
    # 1. find all data thats within period
    result = return_close_prices_based_on_trading_days(date, period_in_days, direction, data),
    result = result[0] # TODO - figure out why we are getting result as [result,] instead of just result from the return_close_... function
    close_prices = result[0]
    period_start = result[1]
    period_end = result[2]

    # 2. calculate standard deviation over period (stdev = vol)
    if(len(close_prices) < 3):
        print("not enough data for " + date)
        return False;
    volatility = stdev = close_prices.std();

    # 3. output list of ["date", "volatility", "period_start", "period_end", "data_points_used"]
    return [date, volatility, period_start, period_end, len(close_prices)]


# extract volatility data
dates = data["Date"].tolist();
volatility_data_list = [];
for date in dates:
    volatility_data = calculate_volatility_for(date, args.volatility_period, args.direction, data);
    if(volatility_data == False): continue;
    volatility_data_list.append(volatility_data);
    #print(volatility_data);
print(volatility_data_list[:5]);
volatility_dataframe = pd.DataFrame(volatility_data_list, columns=["Date", "Volatility", "PeriodStart", "PeriodEnd", "DataPointsUsed"])

# export dataframe to cv
volatility_dataframe.to_csv("../data/sp500.vol."+str(args.volatility_period)+"."+args.direction+"."+args.start_year + "_to_" + args.end_year+".csv")
