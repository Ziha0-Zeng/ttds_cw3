import json
import os,sys
import re
from datetime import datetime

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time
from myapp.preprocess.MongoDBHandler import MongoDbHandler
import pandas as pd
from pandas import DataFrame
import json

######################################
# original file path
json_path1 = './raw_data/arxiv_10000_url_raw.json'
database = "papers"
collection = "processed_data_10000"
######################################

# processed file path
# json_path2 = 'processedOrigin.json'

# store the data
# dict = {}
# attr = ['id','submitter','authors','title','comments','journal-ref','doi','report-no','categories','license','abstract','versions','update_date','authors_parsed']
stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

def time_process(time):
    return datetime.fromisoformat(time)

##############################
## authors process

# This function is used to remove content between parentheses recursively
def remove_text_between_parens(text):
    n = 1  # run at least once
    while n:
        text, n = re.subn(r'\([^()]*\)', '', text)  # remove non-nested/flat balanced parts
    return text

def author_process(authors):
    # check if it has 'and' to connect several authors
    # change 'and' to ',' and '  ' to ' '
    no_doublespace = authors.replace('  ', ' ')
    no_ands = no_doublespace.replace('and',',')
    
    # some organization names within parentheses
    no_parenthese = remove_text_between_parens(no_ands)

    # remove special characters
    modified = re.sub(r'[^a-zA-Z]+', ' ', no_parenthese) # "[^a-zA-Z0-9 \-\'\.\,]", ""
    modified_names = modified.split(',')
    mn_names = []
    for name in modified_names:
        striped = name.strip()
        if striped != "":
            mn_names.append(striped.lower())
    token_without_sw = [word for word in mn_names if not word in stop_words]
    stemmed = [porter.stem(word) for word in token_without_sw]
    word_len_limited = [word for word in stemmed if len(word) > 2]
    return ', '.join(word_len_limited)

##############################
## text process (title or abstract)
# This function is used for tokenization and lower all characters
# remove stopwords and then stem
def text_process(text):
    token = re.sub(r'[^\w]+', ' ', text)  # r'[^\w]+'
    token = token.lower()
    token = token.split()  # based on '\s' to split string
    filtered_word = []
    token_without_sw = [word for word in token if not word in stop_words]
    stemmed = [porter.stem(word) for word in token_without_sw]
    return ' '.join(stemmed)


if __name__ == "__main__":
    mongoSession = MongoDbHandler('localhost', 'root', '123456') # host, username, password (username and password should be changed to yours)
    print("!!!!!!!!!!!!!!!!!!!")
    # i is used for counting number
    i = 0
    with open(json_path1,'r') as f:
        while True:
            line = f.readline()
            if not line:
                print("break i is ",i)
                break
            # elif i == 1000:
            #     break
            params = json.loads(line)

            # process authors, title and abstract part
            # print("id: ", params['id'])
            params['authors'] = author_process(params['authors'])
            params['authors_array'] = author_process(params['authors']).split()
            # print("after : ", params['authors'])
            params['relevance'] = 0.0
            # params['id'] = i
            params['title'] = text_process(params['title'])
            params['abstract'] = text_process(params['abstract'])
            if i % 1000 == 0:
                print("i is ",i)

            i=i+1

            # insert data to the mongod, the collection is 'processed' in the 'ttds' database
            mongoSession.insert_one(database, collection, params)

    time.sleep(2)
    mongoSession.close()

