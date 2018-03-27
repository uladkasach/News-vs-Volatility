# "Using News To Predict"
### [1] Predicting the Stock Market with News Articles - Stanford NLP Group
- https://nlp.stanford.edu/courses/cs224n/2007/fp/timmonsr-kylee84.pdf

### [2] Automated news reading: Stock price prediction based on financial news using context-capturing feature
- 2013
- https://www.sciencedirect.com/science/article/pii/S0167923613000651
- they "enhance existing text mining methods by using more expressive features to represent text and by employing market feedback as part of our feature selection process."
- Questions:
    - context-capturing features = ?
        - what are the more expressive features
    - how do they employ market feedback?
- ** metrics **
    - volatility
    - market drift
    - stock price (intra day and daily)
- **VERY STRONG ARTICLE**
- > our approach allows selecting semantically relevant features and thus, reduces the problem of over-fitting when
applying a machine learning

- most solutions involve using bagofwords / TF-IDF
- up to 76% when using "combinations of words" + feature selection

- Feature engineering:
    - feedback for feature extraction: positive -vs- negative class based on "market reaction" for each news article
        - *QUESTION*: does this not fall for the problem of having inaccurate labels? News that has no reaction may be labeled as having a reaction
    - steps of extaction:
        - extraction
            - words, word combinations
        - selection
            - based on market reaction (feedback)
        - representation
            - tf-idf

    - details:
        - extraction:
            - "dictaionry-approach" : pos-neg word list of psychology handbook
            - bag of words
            - N-Gram (2gram)
            - Noun Phrases
            - 2 word combinations
                - e.g., skip N words in between
        - selection:
            - Chi-square and Bi-normal-separation
- Data Source
    - corporate announcements
- **inovation**: feature selection
- strong literature review


### [3] stock trend prediction using news sentiment analysis - arXiv
- https://arxiv.org/pdf/1607.01958


### [4] Predicting Stock Prices from News Articles
    - https://www.stat.berkeley.edu/~aldous/Research/Ugrad/chen_USA.pdf


### [5] Quantifying the semantics of search behavior before stock market moves
- http://www.pnas.org/content/pnas/early/2014/07/23/1324054111.full.pdf
- segmenting the wiki corpus into semantic catagories, then evaluate the [search_volume_of_catagory -vs- market_movements] for each catagory


### [6] Predicting Socio-Economic Indicators using News Events
- (2016)
- https://cs.nyu.edu/~sunandan/event-predict.pdf
- generative model for event extraction from text
- use the events to predict socio economic indicators
    - specifically food prices
- *** events as features***
- **predicts**
    - food prices (regression)
    - price spikes (classification)
- **commodity pricing** is the metric theyre predicting:
    > Understanding the factors that impact volatility of
socio-economic indicators is a fundamental problem of interest for
policy-making [28] and financial institutions [16][35]

- sources:
    - relating news to stock prices
    - describing why socioeconomic features are important
- basis for:
    - extracting all features and not assuming / hardcoding logic
- **STRONG RELATED WORK SECTION**

------

# "socioeconomic indicators news prediction"

### [7] Predicting Financial Markets: Comparing Survey, News, Twitter and Search Engine Data
 - Huina Mao, Indiana University-Bloomington, Scott Counts, Microsoft Research, and Johan Bollen, Indiana University-Bloomington
 - 2011
 - *** market indices ***
    - the Dow Jones Industrial Average,
    - trading volumes,
    - market volatility (VIX)
    - gold prices.

### [8] Predicting Economic Indicators from Web Text Using Sentiment Composition
- 2014
- http://www.oxford-man.ox.ac.uk/sites/default/files/sentiment_ICICA2014.pdf


### [9] PREDICTING MARKET VOLATILITY FROM FEDERAL RESERVE BOARD MEETING MINUTES
 - https://stanford.edu/~rezab/papers/finlp_slides.pdf
 - *** metrics ***
    - volatility of stocks,
    - treasury bill,
    - treasury note
 - ** datasource **
    - meeting minutes of federal reserve board are publicly availible
        - decide interest rates
        - other assessments produced
 - ** dependency features **
 - high difficulty in predicting s&p500 based on minutes

### [10] Text Mining Systems for Market Response to News: A Survey
- 2006
- Marc-André Mittermayer, Gerhard F. Knolmayer  


----
# SCHOLAR: predicting treasury bond yeild based on news

### [11]  The Stock Market's Reaction to Unemployment News: Why Bad News Is Usually Good for Stocks
- 2006



 -----
# predicting based on news
### [14] The role of news-based uncertainty indices in predicting oil markets: a hybrid nonparametric quantile causality method
- predicts oil prices based on "news"
- http://repec.economics.emu.edu.tr/repec/emu/wpaper/15-02.pdf
- 2015
- interrelationship of oil-price shocks with recessions and inflationary episodes in
the US economy,

### [15] Predicting stock market indicators through twitter “I hope it is not as bad as I fear”
- https://www.sciencedirect.com/science/article/pii/S1877042811023895/pdf?md5=09eeb316cb25f9fdf102bd1fb70e2c52&pid=1-s2.0-S1877042811023895-main.pdf&_valck=1
- 2011


-----

# from searching for datasets

### [37] Using structured events to predict stock price movement: An empirical investigation.
- http://www.aclweb.org/anthology/D14-1148
-  Xiao Ding, Yue Zhang, Ting Liu, and Junwen Duan.
-  In Proc. of EMNLP, pages 1415–1425, Doha, Qatar, October 2014. Association for Computational Linguistics.

- > previous work uses shallow features (bag-of-words, named entities, noun phrases) which dont capture entity-relation information and hence cannot represent entity-relation information and events

- utilizes OpenIE (open information extraction) to extract structured relationships from news data from the web
    - i.e., "events" specifically

- finds the relationship between "events" extracted with OpenIE and stock prices

- > Largescale experiments show that the accuracy of S&P 500 index prediction is 60%, and that of individual stock prediction can be over 70%.

- from [38] : disadvantage of structured representations of events is data sparsity


- prior work:
    - Literature that have utilized NLP and found that events are key
        - (Das and Chen, 2007; Tetlock, 2007; Tetlock et al., 2008; Si et al., 2013; Xie et al., 2013; Wang and Hua, 2014)
        - some prior works simply consider "events" as lists of words: (Fung et al., 2002; Fung et al., 2003; Hayo and Kutan, 2004; Feldman et al., 2011).
    - literature that have utilized basic features from news to model events
        - (Lavrenko et al., 2000; Kogan et al., 2009; Luss and d’Aspremont, 2012; Schumaker and Chen, 2009).


- conclusion: deep neural networks work better than linear models


- compares bag of words -vs- event features w/ SVM and NN models


> Tetlock, Saar-Tsechansky, and Macskassy (2008)
that there is a one-day delay between the price
response and the information embedded in the
news.


> Radinsky et al. (2012) argued that news titles are
more helpful for prediction compared to news contents


*** fact *** : when predicting individual stocks using only news from that company results in better performance than when using sector news which is better than when using all news - when building features with this technique


- literature review
    - financial news can strongly impact security share price  (Chan, 2003; Tetlock et al., 2008).
    - bag of words news mining : (Lavrenko et al., 2000; Kogan et al.,
2009; Luss and d’Aspremont, 2012).
    - Schumaker and Chen (2009) extract noun phrases and named entities to augment bags-of-words
    - Xie et al. (2013), Wang et al. (2014) explore a rich feature space that relies on frame semantic parsing
    - "event" based approaches : (Fung et al., 2002; Hayo and Kutan, 2005;Feldman et al., 2011).
        - Fung, Yu, and Lam (2002) use a normalized word vector-space
        -  Feldman et al. (2011) extract 9 predefined categories of events based on heuristic rules
        - use information extraction techniques (OpenIE) : (Yates et al. (2007); Etzioni et al. (2011); Faber et al. (2011))
    - sentiment analysis approaches:  (Das and Chen, 2007; Tetlock, 2007; Tetlock etal., 2008; Bollen et al., 2011; Si et al., 2013).
        - Tetlock et. al. : negative words -vs- stock price
        - Bollen and Zeng (2011) : is overall twitter sentiment related to volatility of DIJA?


### [38] Deep Learning for Event-Driven Stock Prediction
- http://www.aaai.org/ocs/index.php/IJCAI/IJCAI15/paper/download/11031/10986
-  Xiao Ding, Yue Zhang, Ting Liu, and Junwen Duan. (same people as [37])
- 1. use neural network to extract events from news data
- 2. use recurrent network to relate event data to stock prices

- >  explore financial news for predicting ***market volatility***

** further literature **
- cites heavily [Bengio, 2009] relating to deep learning based on news
- sentiment : [Das and Chen, 2007; Tetlock, 2007; Tetlock et al., 2008; Bollen et al., 2011; Si et al., 2013].

**questions** :
- combine multiplicativly -vs- implicitly?
- "semantic compositionality over event arguments"
    - what are the event arguments

- literature review:
    -  pioneering work: bags-of-words, noun phrases, and named entities [Kogan et al., 2009; Schumaker and Chen, 2009].
        - these features do not capture structured relations

- build "event vectors"
    - s.t.,
    > similar events, such as (Actor = Nvidia fourth quarter results, Action = miss, Object = views) and (Actor = Delta profit, Action = didn’t reach, Object = estimates), have similar vectors, even if they do not share common words.

- feature learning model :
     > can learn the semantic compositionality over event arguments by combining them multiplicatively instead of only implicitly, as with standard neural networks.

- prediction model : build prediction with CONV network
    - embeddings are appropriate for achieving good results with a density estimator (e.g. convolutional neural network), which can misbehave in high dimensions [Bengio et al., 2005]
        - *** fact ***: convolutional networks can misbehave with high dimensional data

- "Research shows diminishing effects of reported events on stock market volatility"
    - the longer ago the event was the less it affects
    - the larger the period you are predicting the less successful you will be
        - Xie et al. [2013], Tetlock et al. [2008] and Ding et al. [2014]

- Feature learning model:
    - input : word embeddings
    - output : event embedding
    - details
        - structured events = (Object, Relationship, Object)
            - each of these is inputted into the model as the average of its words
                - since each of the parts of the Tuple can be composed of multiple words
        - modify regular embedding network by adding a  role*actor*action metric in adition to bias, where the Role parameter is also learned

    - loss : **margin-loss** to relate structured events to word embeddings
        - make fake events -vs- real events


- prediction :
     > The output of the model is a binary class, where
    Class +1 represents that the stock price will increase, and
    Class -1 represents that the stock price will decrease.

    - Use convolution to generate features
        - convolution to summarize sequential data over 3 day periods, max pooling to summarize most informative information over the whole period.
        - > it can be viewed as feature extraction based on sliding window

- *** FACT: ***  Randinsky et al. [2012] and Ding et al.
[2014] show that news titles are more useful for prediction
compared to news contents.


- meta:
    - see test train spliting for the dataset

- related work:
    - sentiment evaluation of news on market prices: [Das and Chen, 2007; Tetlock, 2007; Tetlock et al., 2008; Bollen et al., 2011; Si et al., 2013].
    -  twitter sentiment related to volatility : Bollen and Zeng [2011]

- **tl;dr** :
    - goal: predict stock price movement (up/down) based on news article titles
        - predict individual stocks & S&P500
    - uses: neural network to create "event embeddings", conv network to predict movement based on event embeddings
    - data sources:
        - news titles from routers + bloomburg source : https://github.com/philipperemy/financial-news-dataset
        - stock price data : yahoo dailys
    - baselines :
        - news bag of words -> features -> svm -> prediction
            - Luss and d’Aspremont et al. [2012]
        - [37] - by them
    - models evaluated over combinations of:
        - features models:
            - word embeddings
                - sum of each word in the document
            - event embeddings
                - as described above
        - prediction
            - standard feed forward neural network
            - convolutional neural network
    - conclusions:
        - event features > word features


### [39] Twitter mood predicts the stock market.
- Johan Bollen, Huina Mao, Xiao-Jun Zeng (2011)
-  https://arxiv.org/pdf/1010.3003&
> is the public mood correlated or even predictive of economic indicators?
- paper analyzes if collective sentiment of twitter is correlated to DIJA
- "[9] investigates the relations between breaking financial news and stock price changes."
