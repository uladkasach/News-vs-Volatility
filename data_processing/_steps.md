- creating labeled document tf-idf vectors:
    1. `python news_tfidf` creates `news/reuters.normalized.tfidf...`
    2. `python vol_day_news_ids` creates `vol_day/indicies...`
    3. `python vol_day_news_labels` creates `vol_day/news_labels...`
    4. `python vol_day_merge_news_labels_and_vectors.py` takes `news/reuters.normalized.tfidf...` and `vol_day/news_labels...` and creates `vol_day/news_vectors_and_labels...` 
