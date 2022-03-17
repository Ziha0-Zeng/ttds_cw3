import json
import os, sys
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import time
from MongoDBHandler import MongoDbHandler
import pandas as pd
from pandas import DataFrame
import json
import numpy as np

################################
# 该路径即可
# raw original file path
json_path1 = './raw_data/arxiv_10000_url_raw.json'
token_frequency_path = './sorted_all_words_10000.json'
################################

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()


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
    no_ands = no_doublespace.replace('and', ',')

    # some organization names within parentheses
    no_parenthese = remove_text_between_parens(no_ands)

    # remove special characters
    modified = re.sub(r'[^a-zA-Z]+', ' ', no_parenthese)  # "[^a-zA-Z0-9 \-\'\.\,]", ""
    modified_names = modified.lower()
    modified_names = modified_names.split()
    # mn_names = []
    # for name in modified_names:
    #     striped = name.strip()
    #     if striped != "":
    #         mn_names.append(striped.lower())

    # return ', '.join(mn_names)
    token_without_sw = [word for word in modified_names if not word in stop_words]
    stemmed = [porter.stem(word) for word in token_without_sw]
    word_len_limited = [word for word in stemmed if len(word) > 2]
    return word_len_limited


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
    word_len_limited = [word for word in stemmed if len(word) > 2]
    # return ' '.join(stemmed)
    return word_len_limited


# mongoSession = MongoDbHandler('localhost') # host, username, password (username and password should be changed to yours)

# i is used for counting number
all_words = {}
i = 0
with open(json_path1, 'r') as f:
    while True:
        line = f.readline()
        if not line:
            print("break i is ", i)
            break
        # elif i == 1000:
        #     break
        params = json.loads(line)

        # process authors, title and abstract part
        # print("id: ", params['id'])
        params['authors'] = author_process(params['authors'])
        # print("after : ", params['authors'])
        params['id'] = i
        params['title'] = text_process(params['title'])
        params['abstract'] = text_process(params['abstract'])
        if i % 10000 == 0:
            print("i is ", i)
        current_all_words = []
        current_all_words.extend(params['authors'])
        current_all_words.extend(params['title'])
        current_all_words.extend(params['abstract'])
        for word in current_all_words:
            if word in all_words.keys():
                all_words[word] = all_words[word] + 1
            else:
                all_words[word] = 1
        i = i + 1

        # insert data to the mongod, the collection is 'processed' in the 'ttds' database
        # mongoSession.insert_one("papers", "processed_data_new", params)
print("[INFO] finish counting")

# if "ber" in all_words:
#     print("cnm")

all_words_gt3 = {}
for key, value in all_words.items():
  if value >= 3:
    all_words_gt3[key] = value

print("[INFO] remove token num < 3")

# sorted_all_words = np.array(sorted(all_words_gt3.items(), key=lambda kv: (kv[1], kv[0]), reverse=True))
sorted_all_words = dict(sorted(all_words_gt3.items(), key=lambda kv: (kv[1]), reverse=True))
# remain_words = sorted_all_words[0:100, 0]


with open(token_frequency_path, 'w') as fp:
    json.dump(sorted_all_words, fp)
print()

# time.sleep(2)
# mongoSession.close()
