import string
import io
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
from collections import defaultdict

# set flag to start appending content,
# example:   if readline() = <Text> activate appending and stop when readline()=</Text>
def tokenizer(keyword,filename):
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
            para = para + line
        if line == '<'+keyword+'>\n':
            flag = 1
        if not line:
            break
    #seprate paragraphs into words with  ;,\s.\[\]\(\)\'"?!
    for i in range(0,len(content)):
        content[i] = re.split(r'[;,&%-\s.\[\]\(\)\'\/"?!]\s*',content[i])
        while '' in content[i]:
            content[i].remove('')
    return content

    #content[para_number][words_number_in_each_para]



def preprocess(keyword,filename):
    stopwords = open('stopwords.txt','r+').read()
    ps = PorterStemmer()
    punc = string.punctuation
    list_preprocess = tokenizer(keyword,filename)
    list_striped = []
    file2 = open(filename+"_preprocess.txt",'w+')
    for i in range(0,len(list_preprocess)):
        list_striped.append([])
        for item in list_preprocess[i]:
            item = ps.stem(item)            #tokenization rules  in multiple if  loops
            if item not in stopwords:
                if item not in punc:
                    if not item.isdigit():# for pure numbers
                        if item[0].islower():# for e.g. FT in the titles and some digits-start words
                            if item[1].islower():#for case a- and a1
                                if not len(item) == 1:# for words in that's  the s after splited by '
                                    list_striped[i].append(item)
                                    file2.write(item)
                                    file2.write('\n')
    return list_striped

def title_content_combine(filename):
    list_headline = preprocess('HEADLINE',filename)
    list_content = preprocess('TEXT',filename)
    list_combine = []
    if len(list_content) == len(list_headline):
        for i in range(0,len(list_content)):
            list_combine.append(list_headline[i]+list_content[i])
    else:
        print ("wrong index length head:"+len(list_headline)+"content:"+len(list_content))

    return list_combine



def indexing(file_list):
    dict = defaultdict(list) #defaultdict() example here https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p06_map_keys_to_multiple_values_in_dict.html
    for doc in range(0,len(file_list)):
        for terms in range(0,len(file_list[doc])):
            dict[file_list[doc][terms]].append((doc,terms))
    return dict



def print_indexing(dict):
    file = open('index.txt','w+')
    docID = None
    sorted(dict.keys())
    for key in sorted(dict.keys()):
        file.write(key)
        for doc in dict[key]:
            if not (doc[0] == docID):
                file.write('\n\t')
                file.write(str(doc[0]))
                file.write(': ')
            docID = doc[0]
            file.write(str(doc[1]))
            file.write(' ')
        file.write('\n')
        docID = None

print_indexing(indexing(title_content_combine('trec.sample.xml')))
