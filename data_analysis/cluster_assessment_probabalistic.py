'''
    cluster Vectors column of data, assess purity based on Label (label is catagorical)
'''
from sklearn.cluster import KMeans
import numpy as np
import argparse
import pandas as pd
import datetime as dt
import json

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_data', help='Path to Vectors Data');
parser.add_argument('-l', '--labels', help='Path to cluster labels - used to cache clustering')
parser.add_argument('-w', '--workers', type=int, default=2);
parser.add_argument('-k', '--clusters', type=int, default=2);
parser.add_argument('-n', '--normalize', action='store_true', help='normalize the summaries')
args = parser.parse_args();

## retreive data
print("reading data");
data = pd.read_hdf(args.path_data, 'data');
print("done reading data");

## calculate frequency of each label
label_sizes = data.groupby(['Label']).size().to_dict();

## extract vectors
vectors = data["Vector"].tolist();
volatility_labels = data["Label"].tolist();

## compute clusters
print("computing k-means");
kmeans = KMeans(n_clusters=args.clusters).fit(vectors)
cluster_labels = kmeans.labels_
print(kmeans.labels_)

## generate summary of clusters -vs- labels assignments
summary = dict();
for index, cluster_label in enumerate(cluster_labels):
    vol_label = volatility_labels[index];
    sum_key = str(cluster_label);
    if(sum_key not in summary): summary[sum_key] = dict();
    if(vol_label not in summary[sum_key]): summary[sum_key][vol_label] = 0;
    summary[sum_key][vol_label] += 1;

## normalize purity of each class through summary
# e.g., in the summaries show that 5% of highs and 90% of lows are in the class
if(args.normalize):
    final_summary = dict();
    for cluster_label, inner_summary in summary.iteritems():
        final_inner_summary = dict();
        for vol_label, frequency in inner_summary.iteritems():
            final_inner_summary[vol_label] = frequency/float(label_sizes[vol_label]);
        final_summary[cluster_label] = final_inner_summary;
else:
    final_summary = summary;

## output final summary for review
print(json.dumps(final_summary, sort_keys=True, indent=4));

## evaluate clusters-vs-labels by purity
def calculate_a_purity(class_frequencies):
    class_frequencies = pd.DataFrame.from_dict(class_frequencies, orient='index');
    class_frequencies = class_frequencies.reset_index();
    class_frequencies = class_frequencies.rename(columns={'index':'Label', 0: "Freq"});
    max_frequency = class_frequencies['Freq'].max();
    total_frequency = class_frequencies['Freq'].sum();
    purity = max_frequency / float(total_frequency);
    print(str(max_frequency) + " / " + str(total_frequency) + " = " + str(purity));
    return purity;
sum_purity = 0;
total_length = len(final_summary.keys())
for cluster_label, class_frequencies in final_summary.iteritems():
    this_purity = calculate_a_purity(class_frequencies);
    sum_purity += this_purity;
total_purity = sum_purity / float(total_length);
print(total_purity);
