import os
import json
import nltk
from nltk.stem import PorterStemmer
from utils import *
nltk.download('punkt')


def get_docs_only(postings):
    result = []
    for id,tf in postings:
        result.append(id)
    return result

def interesect_docs(list1, list2):
    result = []
    i, j = 0, 0
    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            result.append(list1[i])
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1
    return result

def eval(query):
    file1 = open("index1.txt", "r", encoding= "utf-8")
    file2 = open("index2.txt", "r", encoding= "utf-8")
    file3 = open("index3.txt", "r", encoding= "utf-8")

    url_file = open("id_url.json", "r")
    id_urlData = json.load(url_file)
    url_file.close()

    idx1_file = open("index1.json", "r")
    idx1 = json.load(idx1_file)
    idx1_file.close()

    idx2_file = open("index2.json", "r")
    idx2 = json.load(idx2_file)
    idx2_file.close()

    idx3_file = open("index3.json", "r")
    idx3 = json.load(idx3_file)
    idx3_file.close()

    porter = PorterStemmer()
    query_tokens = tokenize(query)
    query_stemmed = [porter.stem(token) for token in query_tokens]
    result = []

    word = query_stemmed[0]

    file1.close()
    file2.close()
    file3.close()
    return result

def printResults(results):
    pass


def runBoolSearch():
    print("Welcome to G56 Boolean Search Engine!")
    while (1):
        try:
            query = input("> ")
            results = eval(query)
            printResults(results)

        except EOFError:
            exit(0)
        

if __name__ == "__main__":
    runBoolSearch()