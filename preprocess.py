import string
import io
from nltk.stem import PorterStemmer
import re
from collections import defaultdict

# set flag to start appending content,
# example:   if readline() = <Text> activate appending and stop when readline()=</Text>
def tokenizer_xml(keyword,filename):
    content = []
    file = open(filename)
    flag = 0
    para = ''
    while 1:
        line = file.readline()
        if line == '</'+keyword+'>\n':
            flag = 0
            content.append(para)
            para=''
        if flag == 1:
            line = line.strip()
            para = para + line +' '
        if line == '<'+keyword+'>\n':
            flag = 1
        if not line:
            break
    #seprate paragraphs into words with  ;,\s.\[\]\(\)\'"?!
    for i in range(0,len(content)):
        content[i] = re.split(r'[;,&%-:=.\[\]\(\)\'\/"?!\s]\s*',content[i])# function explanation here http://www.voidcn.com/article/p-mdydvcci-bqb.html
        while '' in content[i]:
            content[i].remove('')
    return content

    #content[para_number][words_number_in_each_para]

def tokenization_docID(filename):
    content = []
    r = '[^0-9]+'
    file = open(filename)
    while 1:
        line = file.readline()
        if '<DOCNO>' in line:
            docID = re.sub(r,'',line)
            content.append(int(docID))
        if not line:
            break
    return content



def preprocess_xml(keyword,filename):
    stopwords = open('stopwords.txt','r+').read().split()# huge disaster waste more than one hour without .split
    ps = PorterStemmer()
    punc = string.punctuation
    list_preprocess = tokenizer_xml(keyword,filename)
    list_striped = []
    for i in range(0,len(list_preprocess)):
        list_striped.append([])
        for j,term in enumerate(list_preprocess[i]):
            if term not in stopwords:          #tokenization rules  in multiple if  loops
                if term not in punc:
                    if not term.isdigit():# for pure numbers
                        list_preprocess[i][j] = ps.stem(term)
                        list_preprocess[i][j] = list_preprocess[i][j].lower()
                        list_striped[i].append(list_preprocess[i][j])
    return list_striped

def title_content_combine(filename):
    list_docID = tokenization_docID(filename)
    list_headline = preprocess_xml('HEADLINE',filename)
    list_content = preprocess_xml('TEXT',filename)
    dict_combine = defaultdict(list)
    if len(list_content) == len(list_headline) == len(list_docID):
        for i in range(0,len(list_docID)):
            dict_combine[list_docID[i]] = list_headline[i]+list_content[i]
    else:
        print ("wrong index length head:"+str(len(list_headline))+"content:"+str(len(list_content)) + "id" + str(len(list_docID)))
    #print(dict_combine)
    return dict_combine



def indexing(file_dict):
    dict = defaultdict(list) #defaultdict() example here https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p06_map_keys_to_multiple_values_in_dict.html
    for docID in sorted(file_dict.keys()):
        for i in range(0,len(file_dict[docID])):
            dict[file_dict[docID][i]].append((docID,i))
    return dict



def print_indexing(dict):
    file = open('index.txt','w+')
    docID = None
    sorted(dict.keys())
    for key in sorted(dict.keys()):
        file.write(key)
        for doc in sorted(dict[key]):
            if not (doc[0] == docID):
                file.write('\n\t')
                file.write(str(doc[0]))
                file.write(': ')
            docID = doc[0]
            file.write(str(doc[1]))
            file.write(' ')
        file.write('\n')
        docID = None

#print_indexing(indexing(title_content_combine('trec.5000.xml')))
