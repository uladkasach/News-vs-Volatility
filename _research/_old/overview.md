## Ideal Project Overview:

1. acquire data
    * Get access to a LOT of news article headlines
    * Get access to unemployment rate in past 20 years
2. feature extraction
    * extract features from news articles
    * extract cumulative features from time-sequence of news articles
4. generate model which predicts future unemployement rate
    * regression
    * classfication
        * increase, decrease (two class)
        * change in more granular catagories (k class)
            - e.g., [-inf, -y], [-y, -x], [-x, x], [x, y], [y, inf]



## Evaluation:
- we can attempt to show that news article data improves prediction in a statistically relevant way
    - baseline
        - replicating previous work
        - same work without non article data
            - since we are capable of using other previous market metrics



## Questions:
- should we even consider using other market metrics (bond price, price of oil, interest rates, sp500, etc) or just stick to article information?
- is it reasonable to focus on extracting features from the news articles first?
- feedback on methods to evaluate correlation of articles to market prices
    - naive method
    - lda -> regression
