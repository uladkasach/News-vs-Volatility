## supervised data source:
- generate base dataset of
    - volatility
    - [news_articles_over_past_x_days]
        - w/ sources: twitter, google, earnings_reports, fortune, etc
- generate labeled training dataset
    - use volatility or TREND volatility [36] as the label
    - use the past_x_days as the features

# raw data + label -> features
- recurrent network onto news article -> volatility
- convert text to events
    - apply OpenIE to news -> events [37]
    - use  neural network to extract events [38]
- evaluate sentiment of articles


- utilizing news headlines -vs- content
    - [38] cited that it was best


# convert features to prediciton
- Convolutional Neural Network [38]



-----

event based modeling -vs- sentiment based


1. use recurrent network to predict whether text contains an event or not
2. use sentiment to gauge sentiment of event
3. use type of event and sentiment of event to predict volatility

reasoning for sentiment: drops -> volatility and (?) negative sentiment -> drops

perhaps skip the events and just go straight to negative sentiment first
