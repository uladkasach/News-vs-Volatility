# Feature Extraction

difficulties arise from:
- extracting features from sequence of words (article headline)
- extracting features from sequence of articles (in time)

to generate fully informed features we will need to create features that take into account both of these sequences.
```
feature     = [article, article, article, ...]  
article     = [headline, date, source]
headline    = [word, word, word, ...]
source      = [geo, id]
```
so, `hyperparam.append(headline_feature_extraction_technique)` and `hyperparam.append(article_sequence_feature_extraction_technique)`


An additional consideration is how far back in time should we attempt to correlate articles and the metric. i.e., `hyperparam.append(article_selection_criteria)`


## action plan
1. create pipeline by which these 'hyperparameters' can be evaluated
    - i.e., implement naive feature extraction techniques and evaluate baselines on
        - correlation finding
        - regression of metric (metric prediction)


# sequence of words (article headlines)

note, for this data the MEANING of the sequence will be most important.
- word embeddings may make a significant impact
- sequence may be important to derive relationships like negation and etc

## engineered features
* from literature
    - [4] relative strength - Positive Events / (all events)
        - involves segmenting by "events" (/subjects) and evaluating whether they were positive or negative


## hybrid features

* ideas
    - vector of relevant concept sentiments
        - idea stemmed from the relative strength segmentation of relevant events feature (of [4])
        - rather than use concept maps, find a way to extract different "Events" / concepts / subjects that were talked about (e.g., relevant nouns and pronouns) and then do sentiment analysis
        - methods of extracting concepts:
            - select nouns in sentence
            - extract topics with lda
        - possible workflow:
            1. find relevant concepts in text
                - ***(i) feature*** : pick out nouns. conduct sentiment analysis. see whether sentiment on that noun is correlated with future value.
                    - ** correlate concept sentiment with future value **
            2. utilize relevant concept sentiment as a predefined-length vector of sentiment
                - will have to distinguish when nothing is expressed about it - *probably* neutral (0) is fine
        - hybrid because:
            - finding "concepts" in text is based on selecting nouns (a heuristic)
            - determining "relevant" concepts is based on data (learning)
        - pros:
            - could easily work on full articles rather than headlines
    - vector of relevant concept occurrences
        - a (likely) less informative version of the method above

## learned features
* from literature
    -
* ideas
    * <del> autoencoders : dimensionality reduction
        - probably not the right approach
        * perhaps explore variational auto encoders
        * (i) consider auto encoder which tries to recreate original input *as well* as a supervised label - and very the weight of getting each wrong
            - this should pick out which features represent the original data AND the value the best, not nessesarily what we want
    * generative networks (?)
        * adversarial

## evaluation

Evaluation serves two purposes:
1. reduce dimensionality of feature space (e.g., supervised dimensionality reduction)
    - evaluation should be able to tell us which features contain information relevant/correlated to the metric
2. assess the capability of predicting the metric
    - e.g., evaluate regression / classification

Method bases:
* ideas
    - naive
        - find where: larger feature magnitude (pos or neg) -> larger metric change
        - example on *concept sentiments*
            - take array of concept_sentiments (concept_sentiment dict for each article in past X | x from [day, week, month])
            - sum the sentiment for that period
                - sum the abs sentiment for that period too?
            - find the corellation coefficient for each (concept, metric)
                - we will canculate the sum of sentiment for many periods
    - linear regression
        - find:
            1. how capable this set is at predicting metric
            2. which metrics provide least information
                - remove these metrics
        - conduct regression and evaluate the weights associated with every feature
    - neural network regression / classification
        - find: which metrics provide the most information
        - backtrack weights to evaluate effective impact of each node
        - classification of UP/Down may be most efficient to implement
* supervised dimensionality reduction from literature:
    - rational:
        - we can extract the most informative from the input
    - techniques:
        - Partial Least Squares (PLS)
        - linear discriminant analysis (LDA)
            - for lda we can create classes based on % change
        - Fisher Linear Discriminant (FLD)
        - Hidden layers of Neural Networks
        - Covariance-preserving Projection (like LDA but preserves class covariance)
