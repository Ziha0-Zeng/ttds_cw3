from ast import keyword
from gettext import find
from sqlite3 import Cursor
from typing import Iterator

#from matplotlib.pyplot import text
from myapp.preprocess.MongoDBHandler import MongoDbHandler
import re
import numpy as np
from datetime import datetime
from myapp.preprocess.processOrigin_processed_data import time_process
from myapp.preprocess.processOrigin_processed_data import text_process
from myapp.preprocess.processOrigin_processed_data import author_process

def advancedQuery2Condition(**kwargs):
    condition = {}
    if "authors" in kwargs.keys():
        condition["authors_array"] = authors2Regex(kwargs["authors"])
    if "startDate" in kwargs.keys() and kwargs["startDate"]:

        if "update_date" not in condition.keys():
            condition["update_date"] = {"$gt": kwargs["startDate"]}
        else:
            condition["update_date"]['$gt'] = kwargs["startDate"]
    if "endDate" in kwargs.keys() and kwargs["endDate"]:
        if "update_date" not in condition.keys():
            condition["update_date"] = {"$lt": kwargs["endDate"]}
        else:
            condition["update_date"]['$lt'] = kwargs["endDate"]
    return condition


def authors2Regex(authors, operator="$in"):
    if type(authors) == str:
        # return re.compile("(^|\s)" + authors + "(^|\s)", re.IGNORECASE)
        return re.compile(authors, re.IGNORECASE)
    if type(authors) == list:
        regex = []
        for author in authors:
            regex.append(authors2Regex(author))
        return {operator: regex}


def request2Condition(verbose=False, **kwargs):
    if verbose:
        print("input:")
        print("\t", kwargs)
    # try:
    #     query = text_process(kwargs["keyword"])
    #     kwargs["keyword"] = ""
    # except KeyError:
    #     print("no querry")

    for k, v in kwargs.items():
        if v == "":
            kwargs[k] = None
        elif k == "authors":
            kwargs[k] = author_process(v).split()
        elif k == "endDate" or k == "startDate":
            kwargs[k] = time_process(v)

    condition = advancedQuery2Condition(**kwargs)

    if verbose:
        print("output:")
        # print("\t query:", query)
        print("\t condition:", condition)
    # return query, condition
    return condition


if __name__ == "__main__":
    print(request2Condition(verbose=True, keyword="caluculas", authors="bal", startDate="2002-03-14", endDate=""))
    print()
    print(request2Condition(verbose=True, keyword="caluculas"))

    # 
    # db = MongoDBHandler('localhost','root', '123456')
    # cursor = db.find(verbose=verbose,**kwargs)
    # db.close(
