import os
import json
import time
import math
import heapq
import numpy as np
from nltk.stem import PorterStemmer
from utils import *


def binary_search_tuple(postings_list, target_doc):
    low = 0
    high = len(postings_list) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_tuple = postings_list[mid]

        if mid_tuple[0] == target_doc:
            return mid_tuple  
        elif mid_tuple[0] < target_doc:
            low = mid + 1
        else:
            high = mid - 1

    return None 

# Only for query weights
def normalize_q(weights):
    magnitude = sum([math.pow(w, 2) for w in weights])
    normalized_w = [w/magnitude for w in weights]

    return normalized_w

# Only for doc weights
def normalize_d(weights):
    magnitude = sum([math.pow(w[1], 2) for w in weights])
    normalized_w = [(w[0], w[1]/magnitude) for w in weights]

    return normalized_w

def intersect_sorted_lists(list1, list2):
    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1
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

def binary_search(sorted_list, target):
    left, right = 0, len(sorted_list) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_value = sorted_list[mid]

        if mid_value == target:
            return mid  
        elif mid_value < target:
            left = mid + 1  
        else:
            right = mid - 1 

    return -1 

def calc_title_tf(posting):
    a = 0.5
    b = 0.7
    term_in_title_count = 0
    for p in posting[2]:
        for tp in posting[3]:
            if p >= tp[0] and p <= tp[1]:
                term_in_title_count += 1
    
    tf = math.log10(1 + term_in_title_count)
    tf_t = a + (b * tf)
    return tf_t


if __name__ == "__main__":

    mioi = open("champions_index.json", 'r')
    ioi = json.load(mioi)
    mioi.close()
    id_file = open("id_url.json", 'r')
    id_url = json.load(id_file)
    id_file.close()

    index = open("champions_index.txt", 'r', encoding= 'utf-8')
    porter = PorterStemmer()
    N = len(id_url)
    # Start of the query
    print("Welcome to G56 Search Engine!")
    while True:
        scores = {}
        query_input = input("> ")
        query = query_input.rstrip('\n')
        start = time.time()
        query_terms = tokenize(query)
        query_terms = [porter.stem(t) for t in query_terms]
        terms = list(set(query_terms))
        terms_w = []
        terms_pl = []
        terms_idf = []

        for t in terms:
            # Find the weight of t in q, get pl for t
            b_num = ioi.get(t)
            index.seek(b_num)
            entry = index.readline().rstrip('\n').split(': ')
            term = entry[0]
            df = int(entry[1])
            idf = math.log10(N / (df + 1))
            if idf <= 0.4:
                continue 
            pl = eval(entry[2])
            tf_q = 1 + math.log10(query_terms.count(t))
            w_q = tf_q * idf
            terms_w.append(w_q)
            terms_pl.append(pl)
            terms_idf.append(idf)
        norm_qw = normalize_q(terms_w)
        for i in range(len(norm_qw)):
            w_q = norm_qw[i]
            idf = terms_idf[i]
            for posting in terms_pl[i]:
                tf_d = 1 + math.log10(posting[1])
                tf_title = calc_title_tf(posting)
                w_d = tf_d * tf_title * idf              # added title weight
                scores.setdefault(posting[0], 0.0)
                scores[posting[0]] += w_q * w_d

        scores_array = np.array(list(scores.values()))
        length = np.linalg.norm(scores_array)
        for d in scores.keys():
            scores[d] = scores[d] / length
        
        scores_list = [(-score, d) for d,score in scores.items()]
        heapq.heapify(scores_list)
        scores_list_len = len(scores_list)

        top20hp = []
        if scores_list_len >= 20:
            top_20hp = sorted([scores_list[i] for i in range(20)])
            for i in range(10):
                v, d = top_20hp[i]
                print(f'Result {i+1}: {id_url.get(str(d))}')
        else:
            top_20hp = sorted(scores_list)
            for i in range(scores_list_len):
                v, d = top_20hp[i]
                print(f'Result {i+1}: {id_url.get(str(d))}')

        end = time.time()
        elapsed_time = end - start
        print(f'Start time: {start}')
        print(f'End time: {end}')
        print(f'Elapsed time: {elapsed_time}')

    index.close()
