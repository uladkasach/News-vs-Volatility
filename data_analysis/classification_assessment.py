'''
    1. load data
    2. split data : https://stackoverflow.com/questions/24147278/how-do-i-create-test-and-train-samples-from-one-dataframe-with-pandas/35531218
        - train, test[, validate]
    3. train classifier
    4. evaluate performance
        - predict with test data
        - compute confusion matrix : https://stackoverflow.com/a/29877565/3068233
        - compute perforamcne metrics : http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html

        - measure error better since we are have ordinal classification
            - https://pdfs.semanticscholar.org/0d35/82610e1738c1959fc8e35f542a866bf96518.pdf
            - https://www.cs.waikato.ac.nz/~eibe/pubs/ordinal_tech_report.pdf
'''
import argparse;
import pandas as pd;
import numpy as np;
from sklearn.cross_validation import train_test_split;
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix

## util
def extract_features_and_labels(data):
    features = data["Vector"].tolist();
    labels = data["Label"].tolist();
    return features, labels;

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_data', help='Path to Vectors Data');
parser.add_argument('-w', '--workers', type=int, default=2);
parser.add_argument('-c', '--classifier', help='define classifier: RF or NN', default="RF");
args = parser.parse_args();

## validate argumetns
if(args.classifier not in ["RF", "NN"]):
    print("classifier must be RF or NN");
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
print("training classifier");
X, y = extract_features_and_labels(train);
if(args.classifier == "RF"):
    classifier = RandomForestClassifier(max_depth=2, random_state=0, class_weight={"HIGH":100})
    classifier.fit(X, y);
    print("classification training completed!");


## evaluate performance
def calculate_performance(y_true, y_pred):
    # confusion matrix
    y_true_series = pd.Series(y_true, name='Actual')
    y_pred_series = pd.Series(y_pred, name='Predicted')
    df_confusion = pd.crosstab(y_true_series, y_pred_series)
    print(df_confusion);

    # p, r, f1(?)
    precision, recall, fscore, support = precision_recall_fscore_support(y_true, y_pred, average='weighted');
    print(precision);
    print(recall);
    print(fscore);

    # return results
    return df_confusion, precision, recall, fscore
def calculate_high_performance(y_true, y_pred):
    # confusion matrix
    y_true_series = pd.Series(y_true, name='Actual')
    y_pred_series = pd.Series(y_pred, name='Predicted')
    df_confusion = pd.crosstab(y_true_series, y_pred_series)
    print(df_confusion);

    # calculate stats
    confusion = df_confusion.as_matrix();
    T = confusion[0].sum();
    TP = confusion[0][0];
    TF = T - TP;
    P = confusion.transpose()[0].sum();
    FP = P - TP;
    precision = TP/float(P);
    recall = TP/float(T);
    F1 = 2*precision*recall/float(precision + recall);
    print("--")
    print("HIGH precision : " + str(TP) + " / " + str(P) + " = " + str(precision) )
    print("HIGH recall    : " + str(TP) + " / " + str(T) + " = " + str(recall) )
    print("HIGH F1 : " + str(F1))
print("------------------");
print("Train Performance:");
train_y_true = y;
train_y_pred = classifier.predict(X);
calculate_high_performance(train_y_true, train_y_pred);
print("------------------");

print("------------------");
print("Test Performance:");
X, y = extract_features_and_labels(test);
test_y_true = y;
test_y_pred = classifier.predict(X);
calculate_high_performance(test_y_true, test_y_pred);
print("------------------");
