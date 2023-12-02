import os
import json
import nltk
from nltk.stem import PorterStemmer
from utils import *
nltk.download('punkt')


def merge_sorted_lists(list1, list2):
    merged_list = []
    i, j = 0, 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1
    merged_list.extend(list1[i:])
    merged_list.extend(list2[j:])
    return merged_list

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

def evaluate(query):
    file1 = open("index1.txt", "r", encoding= "utf-8")
    file2 = open("index2.txt", "r", encoding= "utf-8")
    file3 = open("index3.txt", "r", encoding= "utf-8")

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

    idxmerges = []
    for token in query_stemmed:
        merged_docs = []
        byte_pos1 = idx1.get(token)
        byte_pos2 = idx2.get(token)
        byte_pos3 = idx3.get(token)
        if byte_pos1 != None:
            file1.seek(byte_pos1)
            line = file1.readline()
            entry = line.split(": ")
            postings = eval(entry[2])
            docs = get_docs_only(postings)
            merged_docs = merge_sorted_lists(merged_docs, docs)
        if byte_pos2 != None:
            file2.seek(byte_pos2)
            line = file2.readline()
            entry = line.split(": ")
            postings = eval(entry[2])
            docs = get_docs_only(postings)
            merged_docs = merge_sorted_lists(merged_docs, docs)
        if byte_pos3 != None:
            file3.seek(byte_pos3)
            line = file3.readline()
            entry = line.split(": ")
            postings = eval(entry[2])
            docs = get_docs_only(postings)
            merged_docs = merge_sorted_lists(merged_docs, docs)
        idxmerges.append(merged_docs)
    file1.close()
    file2.close()
    file3.close()
    if len(idxmerges) == 0:
        return result
    elif len(idxmerges) == 1:
        return idxmerges[0]
    else:
        merge_count = len(idxmerges)-1
        while merge_count > 0:
            result = idxmerges.pop(0)
            result = interesect_docs(result, idxmerges[0])
            merge_count -= 1
        return result

def printResults(results):
    url_file = open("id_url.json", "r")
    id_urlData = json.load(url_file)
    url_file.close()
    for id in results:
        print(id_urlData.get(id))
    return



def runBoolSearch():
    print("Welcome to G56 Boolean Search Engine!")
    while (1):
        try:
            query = input("> ")
            results = evaluate(query)
            printResults(results)

        except EOFError:
            exit(0)
        

if __name__ == "__main__":
    runBoolSearch()