from collections import Counter
import time
import math
import pymongo
import json
import re
from collections import defaultdict
from tqdm import tqdm
import numpy as np
import pandas as pd
from gensim import corpora, models, similarities
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from myapp.preprocess.database import authors2Regex, request2Condition
import nltk
# nltk.download('stopwords')

from myapp.preprocess.MongoDBHandler import MongoDbHandler
# from database import Dataset


class InvertIndexGenerator:
    def __init__(self):
        self.collection = None
        self.db = None
        self.test_num = 10000
        self.inv_index = defaultdict()
        self.doc_size = 0
        self.tfidf_dict = None
        self.exist_token = defaultdict()
        self.stop_words = set(stopwords.words('english'))
        self.porter = PorterStemmer()
        self.doc_len = 10000

    def text_process(self, text):
        token = re.sub(r'[^\w]+', ' ', text)  # r'[^\w]+'
        token = token.lower()
        token = token.split()  # based on '\s' to split string
        filtered_word = []
        token_without_sw = [word for word in token if not word in self.stop_words]
        stemmed = [self.porter.stem(word) for word in token_without_sw]
        return stemmed

    # return author, title and abstract docs
    def readDocs(self, host='localhost', port=27017):
        client = pymongo.MongoClient(host=host, port=port, username="root", password="123456")
        self.db = client.papers
        self.collection = self.db.processed_data_10000
        self.collection1 = self.db.tfidf_10000
        self.collection2 = self.db.invert_index
        self.collection3 = self.db.tfidf_token2id
        self.collection_raw_data_10000 = self.db.raw_data_10000
        self.tfidf_10000_vectorized = self.db.tfidf_10000_vectorized
        self.tfidf_100000_vectorized = self.db.tfidf_100000_vectorized
        self.token2id = defaultdict(int)


    def tfidf_lib(self):
        with open('./sorted_all_words_10000.json') as fp:
            sorted_all_words = json.load(fp)

        texts = []
        for i, x in tqdm(enumerate(self.collection.find({}, {"id": 1, "authors": 1, "title": 1, "abstract": 1}))):
            # self.exist_token = defaultdict()
            # if i > self.test_num - 1:
            #     break
            doc = (x["authors"] + " " + x["title"] + " " + x["abstract"]).split()
        ##########################
            # 用inverted index
            for pos, token in enumerate(doc):
                if token not in self.inv_index and token in sorted_all_words:
                    self.inv_index[token] = [i]
                elif token in self.inv_index and token in sorted_all_words:
                    self.inv_index[token].append(i)
        self.doc_size = i + 1
        print("[INFO] start writing")
        print(len(self.inv_index.keys()))
        for i, token in tqdm(enumerate(self.inv_index)):
            tfidf = np.zeros(self.doc_size)
            # tfidf = []
            self.token2id[token] = i
            for doc_id in set(self.inv_index[token]):
                tf_value = self.inv_index[token].count(doc_id)
                df_value = len(self.inv_index[token])

                # calculate score for
                score = ((1 + np.log10(tf_value)) * np.log10(self.doc_size / df_value))
                tfidf[doc_id] = score
                # tfidf.append([doc_id, score])
            self.collection1.insert_one({"id": i, "array": list(tfidf)})

        with open('token2id_100000.json', 'w') as fp:
            json.dump(self.token2id, fp)


    def tfidf_lib_fast(self):
        with open('./sorted_all_words_10000.json') as fp:
            sorted_all_words = json.load(fp)

        texts = []
        for i, x in tqdm(enumerate(self.collection.find({}, {"id_new": 1, "authors": 1, "title": 1, "abstract": 1}))):
            # self.exist_token = defaultdict()
            # if i > self.test_num - 1:
            #     break
            doc = (x["authors"] + " " + x["title"] + " " + x["abstract"]).split()
        ##########################
            # 用inverted index
            for pos, token in enumerate(doc):
                if token not in self.inv_index and token in sorted_all_words:
                    self.inv_index[token] = [i]
                elif token in self.inv_index and token in sorted_all_words:
                    self.inv_index[token].append(i)
        self.doc_size = i + 1
        print("[INFO] start writing")
        print(len(self.inv_index.keys()))
        for i, token in tqdm(enumerate(self.inv_index)):
            #######################################################
            count = Counter(self.inv_index[token])
            doc_id_set, tf_values = np.array(list(count.keys())), np.array(list(count.values()))
            tfidf = np.zeros(self.doc_size)
            df_value = len(self.inv_index[token])
            scores = ((1 + np.log10(tf_values)) * np.log10(self.doc_size / df_value))
            tfidf[doc_id_set] = scores
            #######################################################
            # # a = self.inv_index[token]
            # # doc_set: list of unique document ids
            # # doc_id_set = np.array(list(set(self.inv_index[token])))
            # doc_dict = defaultdict(int)
            # for doc in self.inv_index[token]:
            #     doc_dict[doc] += 1
            #
            # doc_id_set, tf_values = np.array(list(doc_dict.keys())), np.array(list(doc_dict.values()))
            # tfidf = np.zeros(self.doc_size)
            # df_value = len(self.inv_index[token])
            # scores = ((1 + np.log10(tf_values)) * np.log10(self.doc_size / df_value))
            # tfidf[doc_id_set] = scores
            # # doc_id_set = pd.unique(self.inv_index[token])
            # # tf_values =
            ######################################################
            # # doc_id_set: list of unique document ids
            # # tf_values:  list of tf values of doc_set
            # doc_id_set, tf_values = np.unique(self.inv_index[token], return_counts=True)
            # tfidf = np.zeros(self.doc_size)
            # df_value = len(self.inv_index[token])
            # scores = ((1 + np.log10(tf_values)) * np.log10(self.doc_size / df_value))
            # tfidf[doc_id_set] = scores
            ###############################################################
            self.token2id[token] = i
            self.tfidf_10000_vectorized.insert_one({"id_new": i, "array": list(tfidf)})

        with open('token2id_10000.json', 'w') as fp:
            json.dump(self.token2id, fp)

    # def tfidf_query(self, query):
    #     print("[INFO] start query")
    #     # preprocessing
    #     tokens = self.text_process(query)
    #     ########################
    #     # read tfidf and token2id
    #     with open('./token2id_100000.json', 'r') as fp:
    #         token2id = json.load(fp)
    #
    #     token_list = []
    #     for token in tokens:
    #         if token in token2id:
    #             token_list.append(token2id[token])
    #     # token_list = [token2id[token] for token in tokens]
    #
    #     # [[1, 0], [2, 3]]
    #     token_array = np.zeros((len(token_list), self.doc_size))
    #     for i, id in enumerate(token_list):
    #         # array = self.collection.find_one({"id": 1}, {"array": 1})
    #         for array in self.collection1.find({}, {"array": 1}).skip(id).limit(1):
    #             for doc in array['array']:
    #                 token_array[i, doc[0]] = doc[1]
    #
    #
    #             # token_array.append(array['array'])
    #             # print
    #
    #     # calculate score
    #     if len(token_list) > 0:
    #         scores = np.array(token_array).sum(axis=0)
    #         sorted_id = np.argsort(scores)[::-1]
    #         return sorted_id
    #     else:
    #         return [-1]

    def tfidf_query_full(self, query, query_start_time="", query_end_time="", author="", relevance_flag=0):
        print("[INFO] start query")
        # preprocessing
        tokens = self.text_process(query)
        ########################
        # read tfidf and token2id
        with open('myapp/preprocess/token2id_10000.json', 'r') as fp:
            token2id = json.load(fp)
        token_list = []
        for token in tokens:
            if token in token2id:
                token_list.append(token2id[token])
        # token_list = [token2id[token] for token in tokens]

        tfidf_array = []
        for token_id in token_list:
            for data in self.tfidf_10000_vectorized.find({}, {"array": 1}).skip(token_id).limit(1):
                tfidf_array.append(data["array"])
            # data = self.tfidf_100000_vectorized.find_one({"id_new": token_id}, {"id_new": 1, "array": 1})
            # tfidf_array.append(data["array"])
            # print()
        # calculate score
        if len(token_list) > 0:
            scores = np.array(tfidf_array).sum(axis=0)
            
            # applied relevance score calculation
            if relevance_flag:
                relevance_list = []
                result = self.collection.find({"id_new": {"$in": [i for i in range(self.doc_len)]}}, {"relevance": 1})
                for relevance in result:
                    relevance_list.append(relevance["relevance"])

                scores += scores * np.array(relevance_list)

            sorted_id = np.argsort(scores)[::-1]
            #####################
            # 去0
            index = 0
            for i, id in enumerate(sorted_id):
                if math.isclose(scores[id], 0.0):
                    index = i
                    break
            sorted_id = sorted_id[:index]
            print(len(sorted_id))

            # 符合的list
            # query_start_time = "2020-06-02"
            # query_end_time = "2021-06-02"
            # gt = self.collection_raw_data_10000.find({"update_date": {"$gt": query_start_time}}, {"_id": 0, "id_new": 1})
            # lt = self.collection_raw_data_10000.find({"update_date": {"$lt": query_end_time}}, {"_id": 0, "id_new": 1})
            remain_doc_id_list = []
            
            if query_start_time:
                # 有开始结束日期
                if query_end_time:
                    result = self.collection_raw_data_10000.find(
                        {
                            "$and": [
                                {"update_date": {"$gt": query_start_time}},
                                {"update_date": {"$lt": query_end_time}}
                            ]
                        }, {"_id": 0, "id_new": 1}
                    )
                    for x in result:
                        remain_doc_id_list.append(x["id_new"])
                    # print(remain_doc_id_list)
                # 有开始无结束日期
                else:
                    result = self.collection_raw_data_10000.find({"update_date": {"$gt": query_start_time}}, {"_id": 0, "id_new": 1})
                    for x in result:
                        remain_doc_id_list.append(x["id_new"])
            # 没有开始时间
            else:
                # 没有开始有结束
                if query_end_time:
                    result = self.collection_raw_data_10000.find({"update_date": {"$lt": query_end_time}}, {"_id": 0, "id_new": 1})
                    for x in result:
                        remain_doc_id_list.append(x["id_new"])

            # author
            print("hello 271")
            remain_author_list = []
            mongo_condi = request2Condition(keyword=query, authors=author)
            # mongo_condi = authors2Regex(author)
            result = self.collection.find(mongo_condi)
            for x in result:
                remain_author_list.append(x["id_new"])

            # 求交集
            print("hello 280")
            if len(remain_doc_id_list) > 0:
                if len(remain_doc_id_list) > 0:
                    sorted_id = [x for x in sorted_id if x in remain_doc_id_list]
                if len(remain_author_list) > 0:
                    sorted_id = [x for x in sorted_id if x in remain_author_list]

            ####################
            return sorted_id
        else:
            return []



    def id2dict_search(self, id_list, cur_page=1, page_size=10):
        paper_list = []

        id_list = id_list[(cur_page-1)*page_size: cur_page*page_size]

        for paper_id in id_list:

            # 方法一
            # paper = self.collection_raw_data_10000.find_one({"id": int(paper_id)}, {"_id": 0, "title": 1, "authors": 1, "abstract": 1, "update_date": 1})
            # paper_list.append(paper)

            # 方法二
            for paper in self.collection_raw_data_10000.find({}, {"_id": 0, "title": 1, "authors": 1, "abstract": 1, "update_date": 1, "url": 1}).skip(int(paper_id)).limit(1):
                paper["isShown"] = 1
                paper_list.append(paper)

        return paper_list

    def tf(self, token, index, doc_ID):
        return index[token].count(doc_ID)

    def df(self, token, index):
        return len(set(index[token]))

    # 用户点了评价需要调用的函数
    # isAdd:    1: like        0: dislike
    def update_relevance(self, id, isAdd):
        # user like this document
        condition = {"id_new": id}
        document = self.collection.find_one(condition)

        if isAdd:
            document["relevance"] += 0.2
        else:
            document["relevance"] -= 0.2
            if document["relevance"] < -1:
                document["relevance"] = -1.0

        self.collection.update_one(condition, {"$set": document})

    # reset relevance
    def reset_relevance(self):
        relevance = self.collection.find({"id_new": {"$in": [i for i in range(self.doc_len)]}})
        for doc in tqdm(relevance):
            condition = {"id_new": doc["id_new"]}
            doc["relevance"] = 0
            self.collection.update_one(condition, {"$set": doc})


# 到时候要写成监听函数
if __name__ == "__main__":
    print(1)
    cur_page = 1
    page_size = 10

    start = time.time()
    generator = InvertIndexGenerator()
    # read data from json

    generator.readDocs('localhost', port=27017)
    # calculate inverted index and calculate tfidf values and write into mongodb
    # start = time.time()
    # generator.tfidf_lib()
    # generator.tfidf_lib_fast()
    # generator.reset_relevance()
    # generator.update_relevance(1437, 0)
    # end = time.time()
    query = "yellow image video"
    # start_day = "2007-06-02"
    # end_day = "2010-06-02"
    # author = "Ben, Ken"
    start_day = ""
    end_day = ""
    author = ""
    # sorted_docs = generator.tfidf_query(query)
    sorted_docs = generator.tfidf_query_full(query, start_day, end_day, author, 1)

    papers = generator.id2dict_search(sorted_docs, cur_page, page_size=100)
    # papers = generator.id2dict_next_page(sorted_docs, cur_page, page_size=10)
    end = time.time()
    print(sorted_docs)
    # end = time.time()
    print("time", end - start)
