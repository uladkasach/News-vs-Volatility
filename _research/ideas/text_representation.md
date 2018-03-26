#Approaches to representation of news content

## data selection consideration
- content subsets
    - title + content
    - content
    - title
- lexical subsets
    - all
    - noun phrases only
    - noun + adj
    - verb only
    - verb + adv
    - noun + verb
    - noun + verb + adj + adv


## approaches consideration


### Feature Engineering
- methods
    - bag of words
    - tf-idf
    - summation of word vectors
    - word-vector * tf-idf combination
    - list of word-vectors
    - sentence-by-sentence word vector combinations

### Feature Learning
- article relevancy prediction  
    - use (feature engineering techniques + volatility data -> prediction) pipeline to label articles as relevant -vs- not relevant
        - could implement an iterative solution which selects the current best-performing model capable of predicting volatility to measure relevancy
        - could enforce that if the model predicts that article is not relevant it can not use its data in prediction
            - consider the training implications - it is two models that must be trained simultaneously
                - how to "backpropogate" updates
    - use neural network architectures to predict which combinations are relevant
- encoder-decoder network
    - encode-decode and use results as features
        - should separate most notable differences between articles
        - consider Variational Autoencoder
    - encode-decode w/ "relevancy" score as A feature to be predicted (in addition to original inputs)
        - provides more weight to mid features that capture highest separation AND  
