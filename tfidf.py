import query
import math
from nltk.stem import PorterStemmer


index_map = query.index_map
stopwords = query.stopwords
filename = 'queries.lab3.txt'
queries = query.tokenizer_query(filename)




def tf(term,docID):
    fren = 0
    term_pos_list = index_map[term]
    for pos in term_pos_list:
            if pos[0] == docID:
                fren += 1

    return fren

def df(term):
    fren = 0
    current_docID = -1
    term_pos_list = index_map[term]
    for pos in term_pos_list:
        if pos[0] > current_docID:
            current_docID = pos[0]
            fren += 1
    return fren

def weight_of_term(term,docID):
    if df(term) == 0 or tf(term,docID) ==0:
        return 0
    else:
        return (1+math.log(tf(term,docID),10))*math.log((1000/df(term)),10)



def tfidf_scoring(query,docID):
    ps = PorterStemmer()
    socre = 0
    for i,item in enumerate(query):
        if not item in stopwords:
            if not item.isdigit():
                query[i] = ps.stem(item.lower())
                socre += weight_of_term(query[i],docID)
    return socre

def tfidf_IDs(query):
    ps = PorterStemmer()
    docIDs_set = set()
    for i,item in enumerate(query):
        if not item in stopwords:
            if not item.isdigit():
                query[i] = ps.stem(item.lower())
                terms_index = index_map[query[i]]
                if not terms_index == None:
                    for item in terms_index:
                        docIDs_set.add(item[0])
    return docIDs_set


for i in range(0,10):
    score_list = []
    for item in tfidf_IDs(queries[i]):
        score_list.append(tfidf_scoring(queries[i],item))
    print (str(i+1) , max(score_list))

#2 3
