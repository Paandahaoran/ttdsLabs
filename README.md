# ttdsCW1 haoran pan    running instruction

there are three main .py documents : preprocess.py , query.py and tfidf.py, each responsible for :

preprocess.py:
  Dealing preoprocessing of text and Positional inverted index work, then generate index.txt, which is
  the document contains the result of inverted index with the dictionary order of terms and data construction:  
  term
      docID: pos1,pos2...

query.py:
  dealing the searching questions of :Boolean search, Phase search, and Proximity search with one main function : query.boolean_query(), and it will generate results in the same root directory

tfidf.py:
  dealing the ranked IR based on TFIDF and genearte the tfidf scores for each query and ranked the score from high to low, all results from query one and maxmium 1000 results for the rest queries.
