import string
import io
from nltk.stem import PorterStemmer
import re


'''file = open('testTrec.xml')
while 1:
    line = file.readlines()
    if line == '\t<'+'TEXT'+'>\n':
    print (line)
    if not line:
            break
file.close()'''


# set flag to start appending content,
# example:   if readline() = <Text> activate appending and stop when readline()=</Text>
'''def tokenizer(keyword,filename):
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
    for i in range(0,len(content)):
        content[i] = re.split(r'[;,\s.\[\]\(\)\'"?!]\s*',content[i])
        while '' in content[i]:
            content[i].remove('')
    return content

a = '5'

print (not a.isdigit())
'''




dict = {'wo':(2,3)}

print (type(dict['wo'][1]))
