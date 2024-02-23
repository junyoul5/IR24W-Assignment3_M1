from collections import namedtuple
import os
from bs4 import BeautifulSoup
import json
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys


posting = namedtuple('posting', ['name', 'score'])
english_stopwords = set(stopwords.words('english'))

def Indexing(rootFolder):

    index = {}
    num = 0

    for subdir, dirs, files in os.walk(rootFolder):
        print(subdir)
        for file in files:
            file_path = os.path.join(subdir,file)
            success = parseJson(index, file_path)
            if success:
                num += 1

    return index, num

def parseJson(index, filename):
    with open(filename, 'r', encoding='utf-8') as Jfile:
        Jcontent = json.load(Jfile)

    try:
        HTML = Jcontent["content"]
        soup = BeautifulSoup(HTML, 'html.parser')
        text = soup.get_text()
        Name = soup.title

        if Name:
            tokens = tokenize(text)
            for key, value in tokens.items():
                if key in index:
                    index[key].append(posting(Name, value))
                else:
                    index[key] = []
                    index[key].append(posting(Name, value))
            return True
        else:
            return False
    except:
        return False


def tokenize(text):
    line_tokens = re.findall(r'[a-zA-Z0-9]+', text.lower(), re.ASCII)
    filtered = [word for word in line_tokens if word not in english_stopwords]
    porter_stemmer = PorterStemmer()
    filtered2 = [porter_stemmer.stem(word) for word in filtered]
    Frequencies = {}
    try:
        for token in filtered2:
            if len(token) >= 3:
                if token not in Frequencies:
                    Frequencies[token] = 1
                else:
                    Frequencies[token] += 1
    except Exception as e:
        return {}
    return Frequencies

if __name__ == '__main__':
    index, num = Indexing(sys.argv[1])
    print(f'unique words: {len(index)}')
    print(f'number of documents {num}')
    try:
        size = sys.getsizeof(index)
        print(f'file size: {size/1024} kb')
    except:
        print("傻逼python私募了")

