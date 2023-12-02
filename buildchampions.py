import os
import json
import time
import math
import heapq
import nltk
from nltk.stem import PorterStemmer
from utils import *


def get_doc_weight(idf, posting):
    tf_d = 1 + math.log10(posting[1])

    a = 0.5
    b = 0.7
    term_in_title_count = 0
    for p in posting[2]:
        for tp in posting[3]:
            if p >= tp[0] and p <= tp[1]:
                term_in_title_count += 1
    
    tf = math.log10(1 + term_in_title_count)
    tf_t = a + (b * tf)

    wd = tf_d * tf_t * idf

    return wd

if __name__ == "__main__":
    ''' Traverse the main index for each t
        capture top 40% of the size of every token's postings list
        weigh each document by its tfidf and log frequency of tokens in the title position'''

    ioi_file = open('main_index.json', 'r')
    ioi = json.load(ioi_file)
    ioi_file.close()

    id_file = open("id_url.json", 'r')
    id_url = json.load(id_file)
    id_file.close()
    
    index_file = open('main_index.txt', 'r', encoding= 'utf-8')
    champions_file = open('champions_index.txt', 'w', encoding= 'utf-8')
    lower_champions_file = open('lower_champions_index.txt', 'w', encoding= 'utf-8')

    N = len(id_url.keys())
    champions_ioi = {}
    lower_champions_ioi = {}

    for k in ioi.keys():
        og_byte_num = ioi.get(k)
        index_file.seek(og_byte_num)
        entry = index_file.readline().rstrip('\n').split(': ')
        term = entry[0]
        df = int(entry[1])
        idf = math.log10(N / (df + 1))
        pl = sorted(eval(entry[2]), key= lambda x : get_doc_weight(idf, x), reverse= True)
        cl = []
        if len(pl) < 50:
            tmp = pl
            pl = cl
            cl = sorted(tmp, key= lambda x : x[0])
        else:
            pl_length = len(pl)
            num_champions = pl_length // 5
            cl = sorted(pl[0:num_champions], key= lambda x : x[0])
            pl = sorted(pl[num_champions:], key= lambda x : x[0])
        champ_line = f'{term}: {df}: {cl}\n'
        l_champ_line = f'{term}: {df}: {pl}\n'

        b_num_c = champions_file.tell()
        champions_ioi[term] = b_num_c
        champions_file.write(champ_line)

        b_num_lc = lower_champions_file.tell()
        lower_champions_ioi[term] = b_num_lc
        lower_champions_file.write(l_champ_line)

        
    
    with open('champions_index.json', 'w') as champions_j_file:
        json.dump(champions_ioi, champions_j_file)

    with open('lower_champions_index.json', 'w') as lower_champions_j_file:
        json.dump(lower_champions_ioi, lower_champions_j_file)

    index_file.close()
    champions_file.close()
    lower_champions_file.close()