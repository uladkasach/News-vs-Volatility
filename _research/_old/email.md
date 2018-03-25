Dr Dundar,

I have been conducting literature review and compiling resources for this project and believe I know what the next steps to take are. Before starting to implement any of my ideas, I would like to receive feedback from you.

Up to this point I have broken down at a high level what is required to forecast unemployment rates based on news article information. Further, I have found how to acquire the unemployment rate information as well as several sources where we can extract news article data through an API (mitigating the time required to scrape websites).  I have also outlined possible methods by which feature extraction from news articles (the headlines) can be conducted and evaluated.

I would like to ask you for your feedback upon:
      1. the high level overview that I have drafted for the project
      2. feature extraction methods for the article headlines
      3. evaluation methods for predicting the unemployment rate
      4. several miscellaneous questions relating the project

------------------------------------------------------------------------------------------------------------------------

[1] Feedback regarding the high level project overview.

High Level Project Overview:
acquire data
Get access to a LOT of news article headlines
Get access to unemployment rate in past 20 years
feature extraction
extract features from news articles
extract cumulative features from time-sequence of news articles
generate model which predicts future unemployement rate
regression
classfication
increase, decrease (two class)
change in more granular catagories (k class)
e.g., [-inf, -y], [-y, -x], [-x, x], [x, y], [y, inf]
Could you please provide me feedback about the high level overview of the project? Do you think that I am missing any steps?

------------------------------------------------------------------------------------------------------------------------

[2] Feedback regarding feature extraction methods for the article headlines

The most promising feature extraction method I have come up with, with literature review and creative thinking, would be to:
      1. extract "concepts" / "topics" from the article headlines (and potentially even the articles themselves) from all of the articles extracted
      2. evaluate which concepts are relevant (correlated) to the future unemployment rate from all of the articles extracted and historical unemployment rates
      3. generate vectors of information extracted from the article about each of the relevant concepts
            - e.g., sentiment analysis, occurrence rate, etc  
This approach is based on the fact that the news is only related to the unemployment rate based on the concepts (e.g., events) that it talks about and how it talks about them.  

Steps 1, 2, and 3 have multiple ways that they can be accomplished. Before going into detail into what options we have, I would like to know: do you think this is a reasonable approach to extracting features from the news articles?

------------------------------------------------------------------------------------------------------------------------

[3]
