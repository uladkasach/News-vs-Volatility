'''
    cluster Vectors column of data, assess purity based on Label (label is catagorical)
'''
from sklearn.cluster import KMeans
import numpy as np
import argparse
import pandas as pd
import datetime as dt
import json
import pickle

## parse arguments
parser = argparse.ArgumentParser();
parser.add_argument('path_data', help='Path to Vectors Data');
parser.add_argument('-w', '--workers', type=int, default=2);
parser.add_argument('-k', '--clusters', type=int, default=2);
parser.add_argument('-n', '--normalize', action='store_true', help='normalize the summaries')
parser.add_argument('-cc', '--cache_clusters_retreive', action='store_true', help='retreive clusters from cache')
parser.add_argument('-cs', '--cache_summary_retreive', action='store_true', help='retreive summary from cache')
parser.add_argument('-cfs', '--cache_final_summary_retreive', action='store_true', help='retreive final summary from cache')
args = parser.parse_args();

if(not args.cache_clusters_retreive or not args.cache_final_summary_retreive and args.normalize): ## if not retreiving either from cache, get full data
    ## retreive data
    print("reading data");
    data = pd.read_hdf(args.path_data, 'data');
    print("done reading data");


if(not args.cache_final_summary_retreive and args.normalize): ## if not retreiving final summary from cache, grab it
    ## calculate frequency of each label
    print("calculating label sizes");
    label_sizes = dict({
        "HIGH" : data["pHIGH"].sum(),
        "MEDIUM" : data["pMEDIUM"].sum(),
        "LOW" : data["pLOW"].sum(),
    })
    print(label_sizes);


## get clusters - cache if needed
print("retreiving clusters...");
if(not args.cache_clusters_retreive):
    ## extract vectors
    vectors = data["Vector"].tolist();

    ## compute clusters
    print("computing k-means");
    kmeans = KMeans(n_clusters=args.clusters, n_jobs=args.workers).fit(vectors)
    cluster_labels = kmeans.labels_
    with open("_cache/cluster_assess_probabilistic.labels.pkl", "w+") as file:
        pickle.dump(cluster_labels, file);
else:
    with open("_cache/cluster_assess_probabilistic.labels.pkl") as file:
        cluster_labels = pickle.load(file);
print(cluster_labels[0:100]);

## generate summary of clusters -vs- labels assignments
print("retreiving summary");
if(not args.cache_summary_retreive):
    print("computing summary");
    summary = dict();
    for index, cluster_label in enumerate(cluster_labels):
        #vol_label = volatility_labels[index];
        data_row = data.iloc[[index]];
        sum_key = str(cluster_label);
        if(sum_key not in summary): summary[sum_key] = dict({
            "HIGH" : 0,
            "MEDIUM" : 0,
            "LOW" : 0,
        });
        ## add label-weight of each vector found in cluster to the cluster summeary
        summary[sum_key]["HIGH"] += data_row['pHIGH'].item();
        summary[sum_key]["MEDIUM"] += data_row['pMEDIUM'].item();
        summary[sum_key]["LOW"] += data_row['pLOW'].item();

        if(index % 500 == 0): print("`-> at index " + str(index) + " of " + str(len(cluster_labels)));
    with open("_cache/cluster_assess_probabilistic.summary.pkl", "w+") as file:
        pickle.dump(summary, file);
else:
    with open("_cache/cluster_assess_probabilistic.summary.pkl") as file:
        summary = pickle.load(file);

if(not args.cache_final_summary_retreive):
    ## normalize purity of each class through summary
    # e.g., in the summaries show that 5% of highs and 90% of lows are in the class
    if(args.normalize):
        print("normalizing summary")
        final_summary = dict();
        for cluster_label, inner_summary in summary.iteritems():
            final_inner_summary = dict();
            for vol_label, frequency in inner_summary.iteritems():
                final_inner_summary[vol_label] = frequency/float(label_sizes[vol_label]);
            final_summary[cluster_label] = final_inner_summary;
    else:
        final_summary = summary;
else:
    print("not defined!");
    exit();

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

def calculate_high_purity(class_frequencies):
    class_frequencies = pd.DataFrame.from_dict(class_frequencies, orient='index');
    class_frequencies = class_frequencies.reset_index();
    class_frequencies = class_frequencies.rename(columns={'index':'Label', 0: "Freq"});
    max_frequency = class_frequencies[class_frequencies["Label"] == "HIGH"]["Freq"].sum();
    total_frequency = class_frequencies['Freq'].sum();
    purity = max_frequency / float(total_frequency);
    print(str(max_frequency) + " / " + str(total_frequency) + " = " + str(purity));
    return purity;
sum_purity = 0;
total_length = len(final_summary.keys())
for cluster_label, class_frequencies in final_summary.iteritems():
    this_purity = calculate_high_purity(class_frequencies);
    sum_purity += this_purity;
total_purity = sum_purity / float(total_length);
print(total_purity);
