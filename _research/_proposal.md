
# metrics
- volatility
    - important for stock price prediction
    - highly related to market drops
    - affected strongly by news
    - "financial risk management"
    - beta is important in predicting return
        - beta = volatility compared to rest of market
        - however - difficult to predict (https://www.investopedia.com/investing/beta-know-risk/):
            - > Another troubling factor is that past price movements are very poor predictors of the future. Betas are merely rear-view mirrors, reflecting very little of what lies ahead.


Read more: Beta: Know The Risk https://www.investopedia.com/investing/beta-know-risk/#ixzz57aLhWGfy
Follow us: Investopedia on Facebook
- market sector drift
- gold price ( = strength of dollar)
- inflation rate
    - can be found based on CPI from BLS as demonstrated by https://cloud.google.com/bigquery/public-data/bureau-of-labor-statistics
- interest rate
- price of commodities ( and other Consumer Price Indexes)
    - foods
    - oil
    - etc
- S&P 500
- 13-week Treasury Bills (both regression of price and volatility)
    - How it's used: The rate is used as an index for various variable rate loans, particularly Stafford and PLUS education loans. Lenders use such an index, which varies, to adjust interest rates as economic conditions change.
- 10-year Treasury Notes
- Treasury bond "yeild to maturity"
    - how much bond expects to yeild
    - affects interset rates
         - including mortgages
- unemployment rates
    - affect stocks [11]

---

# Proposal:
- evaluate capability of news to predict all of these metrics, starting with most impactful first

Reasoning:
- The technique will be the same for predicting all of these metrics since the features are news data.
- We can start with something more interesting, most interesting to me is market volatility of stocks.
    - i.e., predicting period of high volatility and low volatility in stocks
        - e.g., ford recently went through high volatility - highly related to their earnings report (news)
            - not sure when it will stop either

- Later we can apply to other metrics to see if it acheivs similar results

- Note: volatility can be found in all of the metrics, but I specifically am interested in stock price volatility of individual companies
    - and perhaps sectors?

-----

#  process
1. building features from news articles
    - bag of words
    - semantic meaning
        - LSA
        - word2vec
    - n grams
    - sentence dependency (See sources for dependency features)
    - clustering words, events, semantics by by topic class (dimmensionality reduction)
        - used in bag of words, not sure how else
    - hand-crafted:
        - consider a feature which is related (w/ w2vec) to the name of the company / stock ticker name
        - consider another related to terms in the market speicifically


    - catagorization by semantic meaning -> sentiment analysis on each topic -> dimmensionality reduction (pca?)
2. correlating features with specific metrics
    - e.g., news relevant to ford affects tesla but not eli-lilly or gold price
    - analysis :
        - see if the correlated features make sense logically
    - meta:
        - can this be done without predicting the stock price / volatility?
3. predicting movements (time series) based on features

----
extras:
- other news sources:
    - fed minutes
    - earnings reports
    - twitter + social media
- other input sources
    - other stocks
    - bonds prices
    - etc

consider
    - volatility of market -vs- volatility of sector -vs- volatility of stock (!)
    - sensitivity to market movements
        - beta = volatility compared to rest of market

----
