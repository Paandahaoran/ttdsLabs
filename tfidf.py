import math
from nltk.stem import PorterStemmer
import preprocess
import re

index_map = preprocess.indexing(preprocess.title_content_combine('trec.5000.xml'))
stopwords = open('stopwords.txt','r+').read().split()
filename = 'queries.ranked.txt'


def tokenizer_query(filename):
    queries = []
    file = open(filename)
    para = ''
    while 1:
        query = file.readline()
        if not query or query == '':
            break
        queries.append(query.strip().lower())
    #seprate paragraphs into words with  ;,\s.\[\]\(\)\'"?!
    for i in range(0,len(queries)):
        queries[i] = re.split(r'[;,&%-.\[\]\(\)\'\/"?!\s]\s*',queries[i])# function explanation here http://www.voidcn.com/article/p-mdydvcci-bqb.html
        while '' in queries[i]:
            queries[i].remove('')
    return queries




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
        if int(pos[0]) > int(current_docID):
            current_docID = pos[0]
            fren += 1
    return fren

def weight_of_term(term,docID):
    if df(term) == 0 or tf(term,docID) == 0:
        return 0
    else:
        return (1+math.log(tf(term,docID),10))*math.log((5000/df(term)),10) #N =1000



def tfidf_scoring(query,docID):
    ps = PorterStemmer()
    socre = 0
    for i,item in enumerate(query):
        if not item in stopwords:
            if not item.isdigit():
                query[i] = ps.stem(item)
                query[i] = query[i].lower()
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
#str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]) + " " + str(item[4]) + " " + str(item[5])
def run():
    score_list = []
    turns = 0
    output = open("results_ranked.txt",'w+')
    queries = tokenizer_query(filename)
    max_size = 1000
    for i in range(0,10):
        for j,item in enumerate(tfidf_IDs(queries[i])):
            if i != 0 and j > max_size:
                break
            score = (i+1,0,item,0,float(tfidf_scoring(queries[i],item)),0)
            score_list.append(score)
        for item in sorted(score_list,key=lambda x:x[4],reverse=True):
            output.write(str(item[0]) + " " + str(item[1]) + " " + str(item[2]) + " " + str(item[3]) + " " + str(item[4]) + " " + str(item[5]))
            output.write('\n')
        score_list.clear()
run()
