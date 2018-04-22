- volatility -vs- news presence
    - just a simple baseline to test
- volatility -vs- news
    - generate representations of documents and use RNN to predict change in volatility
        - regression [normalized abs change]
        - classification [increase_more_than_x%, change_less_than_x%, decrease_more_than_x%]
    - representations
        - tfidf-svd
        - classification of news
            - e.g., weather is not relevant to market
            - [economics, trade, oil, classes-etc...]
        - news vector information
        - sentiment information
        - event information
        - entities extraction
        - reduce representation only to key words (nouns, nouns+verbs, etc) (feature engineeringy)
- volatility + volume -vs- news
    - facts:
        - significant news -vs- regular news assessments [48]
            - significant news results in increased trading volume
        - high trading volume may or may not result in re-evaluation of price
            - if high volume + low change in price, news was difficult to interpret [48]
    - 1. can classify documents based on whether they cause volume and how interpretable they are:
        - some news is significant but not clear, but the "significant" words from the document should still be attempted to be caputured
        - some news is not significant, and the words here should not be captured
        - volume will be important in successfully predicint volatility change
        - e.g., classify news as
            - not_significant, significant_clear, significant_conflicted
                - not_significant : low volume causing
                - significant_clear : high volume causing and large change in value causing
                - significant_conflicted : high volume causing and low change in value causing
        - And based on these labels we can predict volatility?
    - 2 - Can we create embeddings for news articles that capture the volatility and volume that follow them?
        - e.g., variational auto encoder
            1. create encoder that generates a latent vector of a document from the word vectors
            2. create a decoder which attempts to
                1. predict volatility (pick one of the  below)
                    - volatility change [normalized volatility change]
                    - volatility class change [HIGH, NORMAL, LOW]
                    - label change [INCREASE MORE THAN X%, CHANGE BETWEEN ABS(X%), DECREASE MORE THAN X%]
                2. predict volume (pick one of the below)
                    - change [normalized volume change]
                    - label [HIGH, NORMAL, LOW]
                    - label change [INCREASE MORE THAN X%, CHANGE BETWEEN ABS(X%), DECREASE MORE THAN X%]
            3. use the latent vector to predict volatility
