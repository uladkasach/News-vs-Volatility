1. evaluate vol_day representations
    - basic freq comparisons
        - <s> bag of words / frequency
    - clustering
        - <s> tf-idf
    - classification - vol_day labels
        - <s> tf-idf RF
        - tf-idf NN
2. evaluate document level representations
    - clustering
        - <s> tf-idf
    - regression - [vector->vol_day label] predict the chance that it will be part of a HIGH label
        - tf-idf
    - ordered regression - [document_vectors->vol_day label]
        - tf-idf
