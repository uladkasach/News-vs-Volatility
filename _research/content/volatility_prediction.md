

### [19] FORECASTING VOLATILITY IN THE STOCK MARKET
- https://beta.vu.nl/nl/Images/werkstuk-ladokhin_tcm235-91388.pdf
- 2009
- Think Thesis style document (big)
- defines volatility and compares several approaches and datasets
- discusses its utility

***IMPORTANT DOCUMENT ***

- volatility is very important in returns and risk managment
    - see the 10 exampels
- volatility can not be accurately calculated based on daily returns
    - does not capture intra day volatility
- many error functions

- (Donaldson, 1997) shows NN can be successful at forcasting
>  (Gonzales, 1997) authors are investigating the use of Neural Networks for predicting volatility for Ibex35 index. This paper shows advantages of the non-linear Neural Networks
over the linear models for volatility forecasting.
> (Hamid, 2004) describes the usage of a feed forward Multilayer Perceptron for
forecasting the volatility of S&P 500 futures. The network uses 13 different financial
indicators as inputs, and gives the forecast for futures of different maturities


- ***EXCELLENT*** baselines documented

-------
# SCHOLAR predicting stock volatility

### [20] The economic value of predicting stock index returns and volatility
- http://www.jstor.org/stable/pdf/30031862.pdf?casa_token=A542urdsO-4AAAAA:UAquZ5KNk1tk2JC6YYaUkRTR3rfLdm0HQCDePDnNVPi0YZDped458tvkv4ARPr0CEvPTIKfyidNMSvxFbtc2JS9-fBqxINQAYX39i7IO8Ga7_yVA
- 2004
- "It appears easier to forecast returns at times when volatility is high"

### [21] Forecasting S&P 100 volatility: the incremental information content of implied volatilities and high-frequency index returns
- http://www.smartquant.com/references/Volatility/vol3.pdf
- 2000

### [22] Forecasting Volatility in the New Zealand Stock Market
- 1999
- https://researchspace.auckland.ac.nz/bitstream/handle/2292/175/202.pdf?sequence=1

### [23] On forecasting daily stock volatility: The role of intraday information and market conditions
- 2009
- http://eprints.lancs.ac.uk/48926/1/Document.pdf
- bussiness school
- ** why volatility **
    - "Volatitlity is a crucial concept for portfolio managment, option pricing, and financial market regulation, inter alios"
- a challenge is that "volatility is not observed even ex post"
- The GARCH modeling framework introduced by Engle in 1982 is still widely used to analyze dynamics of dialy variation

### [24] Forecasting the volatility of stock price index
- 2007
- http://opac.vimaru.edu.vn/edata/E-Journal/2007/Expert%20Systems%20with%20Applications/Expert%20Systems.%20Vol%2033.%20Issue%204.A11.pdf
- **why volatility**
    - > Accurate volatility forecasting is the core task in the risk management in which various portfolios’ pricing, hedging, and option strategies are exercised.
- begin using ann


### [25] How Relevant is Volatility Forecasting for Financial Risk Management?
- 2000
- http://www.jstor.org/stable/2646668?casa_token=Dw9kxnZmXEcAAAAA:VHzGUEAedqKjYJiejf2UL0uOrTUwFKiug3P7e4NMQuIDBdgkAFJzP8MCE2XjlnslR9VAAGgRJbRtn5_p6OsRIQICQua8PGCWk4IgSAIcEidfd4z2&seq=1#page_scan_tab_contents
- > "It depends." if  forcastable, then useful for risk managment.

### [26] Macroeconomic Determinants of Stock Market Volatility and Volatility Risk-Premiums
- 2012
- https://warwick.ac.uk/fac/soc/economics/staff/academic/corradi/research/macrovol.pdf
- ** great econ resource for volatility **
- "volatility is correlated to business cycle"

### [28] Forecasting UK stock market volatility
- 2000
- https://www.researchgate.net/profile/Alan_Speight/publication/227602899_Forecasting_UK_stock_market_volatility/links/00b7d5208a9c73e1fd000000/Forecasting-UK-stock-market-volatility.pdf
- > Since the stock market crash of 1987, stock price volatility
has been the focus of both empirical academic research and
regulatory concern


----
# citers of [24]
https://scholar.google.com/scholar?as_ylo=2014&hl=en&as_sdt=800005&sciodt=0,15&cites=2414425181234816623&scipsc=

### [29] Forecasting financial time series volatility using Particle Swarm Optimization trained Quantile Regression Neural Network
- https://www.sciencedirect.com/science/article/pii/S1568494617301862
- 2017
- > Accurate forecasting of volatility from financial time series is paramount in financial decision making.
- compares their technique to multiple baselines
- ** no news data **


### [30]  Comparison of ARIMA and artificial neural networks models for stock price prediction.
Adebiyi, A. A., Adewumi, A. O., & Ayo, C. K. (2014).Journal of Applied Mathematics, 2014.

### [31]  A differential harmony search based hybrid interval type2 fuzzy EGARCH model for stock market volatility prediction.
Dash, R., Dash, P. K., & Bisoi, R. (2015). International Journal of Approximate Reasoning, 59, 81-104.

### [32]  Volatility forecast using hybrid neural network models. Expert Systems with Applications,
Kristjanpoller, W., Fadic, A., & Minutolo, M. C. (2014).41(5), 2437-2442.

### [33] Forecasting stock market indexes using principle component analysis and stochastic time effective neural networks.
Wang, J., & Wang, J. (2015). Neurocomputing, 156, 68-78.

### [34] Forecasting energy market indices with recurrent neural networks: Case study of crude oil price fluctuations.
Wang, J., & Wang, J. (2016).  Energy, 102, 365-374.

### [35] Application of artificial neural network models and principal component analysis method in predicting stock prices on Tehran Stock Exchange.
Zahedi, J., & Rounaghi, M. M. (2015). Physica A: Statistical Mechanics and its Applications, 438, 178-187.

#### [45] Deep Learning Stock Volatility with Google Domestic Trends
-  https://www.researchgate.net/profile/Eric_Nichols3/publication/287250000_Deep_Learning_Stock_Volatilities_with_Google_Domestic_Trends/links/5796e9af08aec89db7b8628a/Deep-Learning-Stock-Volatilities-with-Google-Domestic-Trends.pdf
- Ruoxuan Xiong1, Eric P. Nichols2 and Yuan Shen*3
- 2016

- notable information:
    - method of predicting intraday volatility based on daily info
    - they use "log" for return info
    - they use Mutual-Information as visualization for feature selection (?)
- other references:
    - ref 3: volatility prediction
