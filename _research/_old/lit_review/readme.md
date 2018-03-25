https://scholar.google.com/scholar?q=recurrent+neural+network+unemployement&hl=en&as_sdt=0&as_vis=1&oi=scholart&sa=X&ved=0ahUKEwimvYnjr_bYAhXH24MKHZmZD28QgQMIKDAA&authuser=1

https://scholar.google.com/scholar?hl=en&as_sdt=0%2C15&as_vis=1&authuser=1&q=forcasting+unemployement+with+news&btnG=

---

### 1. Web article: "This Machine Learning Technique Can Predict GDP Better Than Forecasters"
- https://seekingalpha.com/article/4090229-machine-learning-technique-can-predict-gdp-better-forecasters
- random forest regression

### 2. Using Neural Nets to Forecast the Unemployment Rate
- 2006
- abstract only
- https://link.springer.com/article/10.2145/20060105
- Forcast unemployement rate with:
    - econometric model
    - artificial neural network model
- outperforms best forcasting method to date
    - main unemployement forcast is by Survey of Professional Forcasters. 2006

### 3. Electric load forecasting by seasonal recurrent SVR (support vector regression) with chaotic artificial bee colony algorithm
- (2011)
- abstract only
- https://www.sciencedirect.com/science/article/pii/S0360544211004634
- uses recurrent networks to generate features to plug into Support vector regression (SVR)
    - "the concept of recurrent neural networks (RNNs), focused on using past information to capture detailed information, is helpful to be combined into an SVR model."
- **generates features : may be useful to get full article**


### 4. Apply news information on the internet to the prediction of interest rates:
- http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.105.9920&rep=rep1&type=pdf
- 2002
- **Uses cognitive maps (Prior Knowledge) to search for news on the Internet**
- predicts interest rates (Knowledge based news miner (KBNMiner))
- Literature review cites other models which predicted interest rates. Also, cites a model which used manually labeled news articles as data for a neural network.
- describes basis for using news articles for predicting interest rates
- <del> pipeline:
    1. data selection
        - use cognative map to narrow down news articles
    2. data pre-processing
    3. data transformation
    4. data mining (to get patterns)
    5. interpreting patterns
- positive -vs- negative effects for each related concept
- detect which concepts are present
- feature : relative strength - Positive Events / (all events)
- questions:
    - how do they use the news articles they select with the NN?
        - answer: they generate features based on the news article utilizing strengths (pos and neg) of events found from concept map AS WELL AS
            - previous average stock price
            - previous average bond price
            - previous average exchange rate


### 5. A Model Selection Approach to Real-Time Macroeconomic Forecasting Using Linear Models and Artificial Neural Networks
- 1995
- http://econwpa.repec.org/eps/mac/papers/9503/9503004.pdf
- Pennsylvania State and Berkly
- model selection : adaptive outperform non-adaptive

### 6. Forecasting US unemployment with Radial Basis Neural Networks, Kalman Filters and Support Vector Regressions
- 2015
- http://eprints.gla.ac.uk/102080/1/102080.pdf
- investigates using Radial Basis Funcion NN's to predict unemployement.
    - Utilizes 5 other models (including 3 NN) as benchmarks of the NN model
- Explores Kalman Filter and SVM Regression as combination models as well.
    - Combination models are benchmarked on other models (simple average and least absolute shrinkage and selection operator.)
- Performance estimated on 1972-2013. Last 7 years used as out-of-sample testing.  
- Radial Basis outperforms all other models
- > NNs’ data-adaptive learning and
clustering ability can prove to be very useful in forecasting applications
- > The empirical evidence indicate that the NNs present significantly better
forecasts than traditional autoregressive models.
- forcasts monthly change of the US unemployment rate (NEMP). Data can be found in online Federal Reserve Economic Data (FRED) database
    - > The US unemployment rate or civilian unemployment rate represents the number of unemployed as a percentage of the labour force. Labour force data are restricted to people 16 years of age and older, who currently reside in 1 of the 50 states or the District of Columbia, who do not reside in institutions (e.g., penal and mental facilities, homes for the aged) and who are not on active duty in the Armed Forces. This is the definition provided by FRED.
- conducts experiments and sensitivity analysis to select potential features.
- ** Bench Marks **
    - Statistical
        - Auto-Regressive Moving Average Model (ARMA)
            - benchmark statistical performance
            - (7, 7) model where coefficients are significant at the 95% confidence interval.
        - Smooth Transition Autoregressive Model (STAR)
            - two AR models with function that defines non-linearity
    - Neural Network
        - previous uses of NN in financial and acroscopic forcasting : (Hiemstra 1996; Moshiri et al. 1999; Zhang and Qi 2005).
        - MLP, RNN and the PSN are the models used as NN benchmarks
        - RNN architectures enable "short-term memory" - enables drawing on all previous inputs and sequential history
            - downfall is that they are more resource intensive (RAM)
        - PSN's combine fast learning of single layer networks with mapping capability of higher order NN's **(!)**
        - more information on these architectures is avalilible: Zhang et al. (1998), Sermpinis et al. (2012)., and in appendix
- Radial Basis Function NN
    - requires less training time but can acheive higher levels of accuracy
- forcast combination techniques are listed, but will not be outlined here as they are irrelevant to our goals
- methods of selecting inputs for NN's were never documented


## 7. The Stock Market's Reaction to Unemployment News: Why Bad News Is Usually Good For Stocks
- 2002
- https://pdfs.semanticscholar.org/6949/23847c7ad34cfecfefb76f14a7a42e1281ab.pdf
- > Blanchard (1981) showed that in equilibrium the same news can some times be
good and some times bad for financial assets, depending on the state of the economy.
    - for stock prices, news may depend on other market metrics
- > Perhaps no economic report exerts as much impact [as the unemployement rate] on
speculative prices or is as closely followed by market participants.
- this study does not use actual news (text) data, but refers to "news" as the change in unemployement rate
----

http://scholarworks.lib.csusb.edu/cgi/viewcontent.cgi?article=1040&context=jiim

http://www.me.chalmers.se/~mwahde/MasterTheses/Hulthen_MScThesis.pdf

https://pdfs.semanticscholar.org/99b6/6f8282b9912715def862f1a1f632fb06cb38.pdf
