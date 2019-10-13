import string
import io
from nltk.stem import PorterStemmer
import re
import preprocess
from collections import defaultdict
stopwords = open('stopwords.txt','r+').read()
index_map = preprocess.indexing(preprocess.title_content_combine('trec.sample.xml'))


def tokenizer_query(filename):
    queries = []
    file = open(filename)
    para = ''
    while 1:
        query = file.readline()
        if not query or query == '':
            break
        queries.append(query.strip())
    #seprate paragraphs into words with  ;,\s.\[\]\(\)\'"?!
    for i in range(0,len(queries)):
        queries[i] = re.split(r'[;,&%-.\[\]\(\)\'\/"?!\s]\s*',queries[i])# function explanation here http://www.voidcn.com/article/p-mdydvcci-bqb.html
        while '' in queries[i]:
            queries[i].remove('')
    return queries

#print (tokenizer_query('queries.lab2.txt'))

def phase_index(phase,distance):
    phase_list = []
    if len(phase) == 1:
        term_list = index_map[phase[0].lower()]
        #phase1_list contains numbrs of docID
        for pos in term_list:
            phase_list.append(pos[0])
    else:
        term1_list = index_map[phase[0].lower()]
        term2_list = index_map[phase[1].lower()]
        #distence judgement
        for pos1 in term1_list:
            for pos2 in term2_list:
                if pos1[0] == pos2[0]:
                    terms_dis = abs(pos1[1]-pos2[1])
                    if terms_dis <= int(distance):
                        phase_list.append(pos1[0])
    phase_list = set(phase_list)
    return phase_list


def boolean_query(query):
    #keyword boolean indicaters
    NOT = False
    OR = False
    AND = False
    #query phase_1 and phase_2
    phase_1=[]
    phase_2=[]
    ps = PorterStemmer()
    #flag of keyword position for spilt phases
    key_flag = 0
    #distance of words  default value is 1
    distance = 1
    # stopping and stemming preprocess of query
    for i,item in enumerate(query):
        query[i] = ps.stem(item.lower())
    print (query)
    # indicaters operations of keywords
    if 'not' in query:
        NOT = True
        key_flag = query.index('not')
        query.remove('not')
    if 'or' in query:
        OR = True
        if key_flag == 0:
            key_flag = query.index('or')
        else:
            key_flag = key_flag-1
        query.remove("or")
    if 'and' in query:
        AND = True
        if key_flag == 0:
            key_flag = query.index('and')
        else:
            key_flag = key_flag-1
        query.remove('and')
    #spilt phases
    if key_flag == 0:
        phase_1 = query[1:]
    else:
        phase_1 = query[1:key_flag]
        phase_2 = query[key_flag:]

    if query[1][1:].isdigit():
        distance = query[1][1:]
        del query[1]
        phase_1 = query[1:3]

    #boolean query with phase_1 and phase_2
    #different situation for one terms and phase
    print(phase_1)
    print(phase_2)
    if not phase_2:
        phase1_doclist = phase_index(phase_1,distance)
        return phase1_doclist
    if phase_2 and (NOT or AND or OR):
        phase1_doclist = phase_index(phase_1,distance)
        phase2_doclist = phase_index(phase_2,distance)
        #https://blog.csdn.net/business122/article/details/7541486 set calculation instruction
        if not NOT:
            if AND:
                return phase1_doclist & phase2_doclist
            if OR:
                return phase1_doclist | phase2_doclist
            else:
                return "error"
        else:
            if AND:
                return phase1_doclist- phase2_doclist
            if OR:
                return phase1_doclist ^ phase2_doclist
            else:
                return "error"
    else:
        return 'error'




for i in range(0,9):
    print (boolean_query(tokenizer_query('queries.lab2.txt')[i]))

#indexing(title_content_combine('trec.sample.xml'))
