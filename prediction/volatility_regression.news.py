import argparse;
import pandas as pd;
import numpy as np;
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from sklearn.cross_validation import train_test_split;

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_to_data', help='Path to Vectors for Vol_Days');
parser.add_argument('-w', '--workers', metavar="D", type=int, default=1)
parser.add_argument('-r', '--readable_output', action='store_true');
args = parser.parse_args();

## get data
print("reading ids");
data = pd.read_hdf(args.path_to_data, 'data');

## pad the sequences of vectors to standardize length
max_length = data["News"].map(len).max();
print(max_length);
vector_size = len(data["News"].iloc[[0]].item()[0]);
empty_vector = np.zeros(vector_size);
def pad_sequence(sequence, target_length):
    current_length = len(sequence);
    padding_required = target_length - current_length;
    for _ in range(padding_required):
        sequence.append(empty_vector);
    sequence = np.array(sequence);
    return sequence;
data["News"].apply(lambda news_vectors: pad_sequence(news_vectors, max_length));

## scale the data (normalize)
## TODO

## split data into train and test
print("spliting data")
train, test = train_test_split(data, test_size=0.2)
print(str(len(train.index)) + " -vs- " + str(len(test.index)) + " out of " + str(len(data.index)));

## get description of input
sequence_timesteps = max_length;
data_dim = vector_size;
print("input shape : " + str((sequence_timesteps, data_dim)));

# build the model
# references :
#   - https://keras.io/getting-started/sequential-model-guide/
#   - https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
#   - https://machinelearningmastery.com/sequence-classification-lstm-recurrent-neural-networks-python-keras/
print("building the model");
model = Sequential()
model.add(LSTM(128, return_sequences=True, input_shape=(sequence_timesteps, data_dim)))  # returns a sequence of vectors of dimension 128
#model.add(LSTM(32, return_sequences=True))  # returns a sequence of vectors of dimension 32
model.add(LSTM(32))  # return a single vector of dimension 32
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mean_squared_error'])


# break X and y for test and train
def split_into_features_and_labels(data):
    features = data["News"].tolist();
    labels = data["Volatility"].tolist();
    features = np.array(features);
    labels = np.array(labels);
    return features, labels;
X_train, y_train = split_into_features_and_labels(train);
X_test, y_test = split_into_features_and_labels(train);
print(X_train.shape);
print(y_train.shape);

# Train the model, iterating on the data in batches of 32 samples
print("fitting NN model");
model.fit(X_train, y_train, epochs=3, batch_size=10)


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
y_true = y_train;
y_pred = model.predict(X_train)
calculate_high_performance(y_true, y_pred);
score = model.evaluate(X_train, y_train, batch_size=10)
print(score);
print("------------------");

print("------------------");
print("Test Performance:");
y_true = y_test;
y_pred = model.predict(X_test)
calculate_high_performance(y_true, y_pred);
score = model.evaluate(X_test, y_test, batch_size=10)
print(score);
print("------------------");
