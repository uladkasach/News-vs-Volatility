

# predicting volatility with newsA


### [43] - Predicting risk from financial reports with regression."
- Kogan, Shimon, et al. Proceedings of Human Language Technologies: The 2009 Annual Conference of the North American Chapter of the Association for Computational Linguistics. Association for Computational Linguistics, 2009.
- http://www.aclweb.org/anthology/N09-1031
- ***VALUE and CAPABILITY and UTILITY of predicting Volatility***
- **definition of volatility**
- using annual earnings report use NLP to predict market volatility for next year
    - compare with results of NLP technique + previous data (since volatility is autoregressive) to see how much NLP adds
- ~15% MSE
- feature representation
    - tf
    - tf-idf
    - log1p
    - log1p bigrams
- data source
    - anuall earnings reports
- predicts annual volatility

### [46] Predicting abnormal returns from news using text classification.
- Luss, Ronny, and Alexandre d’Aspremont. "Predicting abnormal returns from news using text classification." Quantitative Finance 15.6 (2015): 999-1012.
- https://arxiv.org/pdf/0809.2792.pdf
- **note** "although the direction of change is not predictable, the size is" - volatility size is predictable
- autocorrelation references
    - several papers found and confirmed autocorrelation
- > These findings tend to demonstrate that, given solely historical stock returns,
future stock returns are not predictable while volatility is.
- **references** for using news data (several papers referenced)
    - news has significant predictive power in volatility
    - restricting the type of news can help as well  
- **machine learning for regression of volatility**
    - two papers that use 1. NN and 2. SVM for regressing the volatility
- **data** press releases
- **conclusion** abnormal returns (volatility) can be predicted well, but direction and thus returns can not
- **problem format and labeling data**
    - label as "positive" if volatility increases at some time after the release of the new
    - problem : text classification. E.g., will volatility increase after this news or not?
- > Text classification has also been used to directly predict volatility (see M.-A.Mittermayer
& Knolmayer (2006b) for a survey of trading systems that use text).
- > Our contribution here is twofold. First, abnormal returns are predicted using text classification techniques
similar to M.-A.Mittermayer & Knolmayer (2006a). Given a press release, we predict whether or
not an abnormal return will occur in the next 10, 20, ..., 250 minutes using text and past absolute returns.
The algorithm in M.-A.Mittermayer & Knolmayer (2006a) uses text to predict whether returns jump up 3%,
down 3%, remain within these bounds, or are “unclear” within 15 minutes of a press release. They consider
a nine months subset of the eight years of press releases used here.
- summary of above:
    - volatility is predicted from text classification by  M.-A.Mittermayer & Knolmayer (2006b)
    - these guys predict whether an "abnormal return" will occur in the next X minutes (10, 20, ..., 250) using text and past abs(returns)
    - M.-A.Mittermayer & Knolmayer (2006a) predicts whether volatility will be of class [jump up >3%, jump down >3%, stay between bounds, be unclear]


### [47] Performance of Heterogeneous Autoregressive Models of Realized Volatility: Evidence from U.S. Stock Market
- Petr Seďa, 2012
- defines historical background and use of fvolatility forcasting
- defines distinct areas of volatility (daily+, weekly, monthly)
- defines three metrics of realized volatility
- defines snp500


### [48] Applications of news analytics in ﬁnance: A review.
- Mitra, Leela, and Gautam Mitra. "Applications of news analytics in ﬁnance: A review." The handbook of news analytics in finance 596 (2011): 1.
- http://optirisk-systems.com/papers/Opt0014.pdf
- ** lit review ** cites many articles backing relevance of news to market
    - significant news -> increased trading volume
    - 65% of large re-evaluations can be linked to public news releases
    - sometimes significant news results in high volume but low change in price -> meaning that news is hard to interpret  
    - news can be split into expected news (e.g., regular reports) and unexpected news
    - news data = [event, cause of event, effect of event]
    - thorough definition of data types
    - SEC provides lots of "pre news"
    - "Macro economic news, particularly economic indicators from the major economies are widely used in automated trading"
    - Earnings Reports are key driving fources behind stocks prices
    - >  the market seems to react more strongly to corporate earnings related news than corporate strategic news
    - lots of literature upon extracting events from documents
        - e.g., entity, action, entity2
    - important to distinguish between "old" news (being published later) and "new" news
    - RavenPack and Reuters publish "relevancy" and "novelty" scores upon news data
    - news released in the morning have greater impact on volatility than news released at end of day
    - STRONG seasonality of news (in both seasons, weeks, and days)
        - most news released before opening
        - tons more news in weekdays (maxing on wednesdays)
    - stock market responds more to negative news than positive news
    - more positive news is released than negative news
    - "Lo (2008), for the Reuters Newscope Event Indices," uses market response to determine news value
    - "Lavernko, Schmill, Lawrie, Ogilvie, Jensen and Allan (2000), Moniz et. al. (2009), Peramunetilleke and Wong (2002) and Luss and d’Aspremont (2009)" also evaluate the "sentiment" of the news based on market response
