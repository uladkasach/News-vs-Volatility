import argparse;
import pandas as pd;
import numpy as np;
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from sklearn.cross_validation import train_test_split;
import matplotlib.pyplot as plt

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_to_data', help='Path to Volatility');
parser.add_argument('-w', '--workers', metavar="D", type=int, default=1)
parser.add_argument('-r', '--readable_output', action='store_true');
parser.add_argument('-t', '--timesteps', metavar="D", type=int, default=30) # default is ~ one month of timesteps
parser.add_argument('-o', '--overlap', metavar="D", type=int, default=5) # default is 5, the default measure for defining volatiltiy
args = parser.parse_args();

## get data
print("reading ids");
data = pd.read_csv(args.path_to_data, nrows=None);

## drop uneeded columns
data = data.drop(["Unnamed: 0", "PeriodStart", "PeriodEnd", "DataPointsUsed"],axis=1)

## scale the data (normalize: mean = 0, standard deviation = 1)
print("normalizing the dataset: mean = 0, stdev = 1");
mean = data["Volatility"].mean();
stdev = data["Volatility"].std();
data["Volatility"] = data["Volatility"].apply(lambda val: (val - mean)/stdev);

## generate dataset: y = volatility price, X = sequence of prior `timesteps`(a number) prices
##      volatility_overlap deals with how volatility is calculated: volatlity is calculated for the future X days.
##          this means that the volatility for March 7th, if X=5, will contain information about volatility of March 7th through 13th.
##          because of this, we do not want to use the past X volatilities to predict it since each of them will have information about days in the target range (window overlap)
print("building dataset");
def extract_sequence_for_index(index, timesteps, volatility_overlap):
    start_index = index-timesteps-volatility_overlap;
    if(start_index < 0): start_index = 0;
    stop_index = index-1-volatility_overlap;
    if(stop_index < 0): stop_index = 0;
    relevant_data = data.loc[start_index:stop_index];
    relevant_vol = relevant_data["Volatility"].tolist();
    if(len(relevant_vol) != timesteps): return None;
    relevant_vol = np.array(relevant_vol);
    relevant_vol = relevant_vol.reshape(timesteps, 1);
    return relevant_vol;
data["Features"] = data.apply(lambda row: extract_sequence_for_index(row.name, args.timesteps, args.overlap), axis=1)

## remove datapoints with sequences that do not have full timestep
##     - remove rows with null
orig_len = len(data.index)
data = data.dropna() # if any col is null in a row, remove it
data = data.reset_index();
filt_len = len(data.index);
print("dates filtered out: " + str(orig_len - filt_len));


## split data into train and test
print("spliting data")
train, test = train_test_split(data, test_size=0.5)
print(str(len(train.index)) + " -vs- " + str(len(test.index)) + " out of " + str(len(data.index)));

# break X and y for test and train
def split_into_features_and_labels(data):
    features = data["Features"].tolist();
    labels = data["Volatility"].tolist();
    features = np.array(features);
    labels = np.array(labels);
    labels = labels.reshape(labels.shape[0], 1);
    return features, labels;
X_train, y_train = split_into_features_and_labels(train);
X_test, y_test = split_into_features_and_labels(test);
print("Feature and Label dimensionality:");
print(X_train.shape);
print(y_train.shape);

## get description of input
sequence_timesteps = args.timesteps;
data_dim = 1;
print("input shape : " + str((sequence_timesteps, data_dim)));

# build the model
# references :
#   - https://keras.io/getting-started/sequential-model-guide/
#   - https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
#   - https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
print("building the model");
model = Sequential()
model.add(LSTM(32, return_sequences=True, input_shape=(sequence_timesteps, data_dim)))  # returns a sequence of vectors of dimension 128
#zmodel.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dropout(0.2))
#model.add(Dense(10))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])


# Train the model, iterating on the data in batches of 32 samples
print("fitting NN model");
model.fit(X_train, y_train, epochs=2, batch_size=200)

## calculate performance
def calculate_high_performance(y_true, y_pred):
    print(y_true);
    print(y_pred);
    error = np.array(y_true) - np.array(y_pred);
    mse = np.mean((error)**2);
    rmse = np.sqrt(mse)
    err_stdev = np.std(error);
    print("MSE:" + str(mse));
    print("RMSE:" + str(rmse));
    print("ERROR STDEV: " + str(err_stdev))
print("------------------");
print("Train Performance:");
y_true = y_train;
y_pred = model.predict(X_train)
calculate_high_performance(y_true, y_pred);
print("------------------");

print("------------------");
print("Test Performance:");
y_true = y_test;
y_pred = model.predict(X_test)
calculate_high_performance(y_true, y_pred);
print("------------------");

## plot predictions
X = np.array(data["Features"].tolist());
y_true = data["Volatility"].tolist();
y_pred = model.predict(X);
plt.plot(y_true, color = 'b');
plt.plot(y_pred, color = 'r');
plt.show();
