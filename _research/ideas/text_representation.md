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
    - use feature engineering techniques + volatility data to label articles as relevant -vs- not relevant
    - use neural network architectures to predict which combinations are relevant
