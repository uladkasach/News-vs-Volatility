'''
    1. load data
    2. split data : https://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas/35531218
        - train, test[, validate]
    3. train model
        - linear-regression
        - svm-regression
        - neural-network
'''
import argparse;
import pandas as pd;
import numpy as np;
from sklearn.cross_validation import train_test_split;
from sklearn.linear_model import LinearRegression;
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD

## util
scale = StandardScaler()
def extract_features_and_labels(data):
    features = data["Vector"].tolist();
    labels = np.array(data["pHIGH"].tolist()); ## labels = probaability of being "HIGH";

    ## normalize since NN are sensitive to scale and variance
    features = scale.fit_transform(features);
    #labels = scale.fit_transform(labels.reshape(-1, 1)).transpose()[0];

    return features, labels;

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_data', help='Path to Vectors Data');
parser.add_argument('-w', '--workers', type=int, default=1);
parser.add_argument('-m', '--model', help='define classifier: L or NN', default="L");
args = parser.parse_args();

## validate argumetns
if(args.model not in ["L", "NN"]):
    print("classifier must be L or NN");
    exit();

## retreive data
print("reading data");
data = pd.read_hdf(args.path_data, 'data');
print("done reading data");

## split data into train and test
print("spliting data")
train, test = train_test_split(data, test_size=0.2)
print(str(len(train.index)) + " -vs- " + str(len(test.index)) + " out of " + str(len(data.index)));

## train classifier
print("training model");
X, y = extract_features_and_labels(train);
if(args.model == "L"):
    model = LinearRegression(n_jobs=args.workers)
    model.fit(X, y);
    print("model training completed!");
if(args.model == "NN"):
    print("building NN model")
    model = Sequential()
    model.add(Dense(100, activation='relu', input_dim=X.shape[1]))
    model.add(Dropout(0.2))
    model.add(Dense(25, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer = 'adam')

    print("fitting NN model");
    # Train the model, iterating on the data in batches of 32 samples
    model.fit(X, y, epochs=70, batch_size=2000)



## evaluate performance
def calculate_performance(y_true, y_pred):
    print("TODO");
def calculate_high_performance(y_true, y_pred):
    print(y_true);
    print(y_pred);
    error = np.array(y_true) - np.array(y_pred);
    mse = np.mean((error)**2);
    rmse = np.sqrt(mse)
    err_stdev = np.std(error);
    print("RMSE:" + str(rmse));
    print("ERROR STDEV: " + str(err_stdev))
print("------------------");
print("Train Performance:");
train_y_true = y;
train_y_pred = model.predict(X)
if(args.model == "NN"): train_y_pred = train_y_pred.transpose()[0];
calculate_high_performance(train_y_true, train_y_pred);
print("------------------");

print("------------------");
print("Test Performance:");
X, y = extract_features_and_labels(test);
test_y_true = y;
test_y_pred = model.predict(X);
if(args.model == "NN"): test_y_pred = test_y_pred.transpose()[0];
calculate_high_performance(test_y_true, test_y_pred);
print("------------------");
