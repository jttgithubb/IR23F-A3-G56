import os
import json
import nltk
from nltk.stem import PorterStemmer
from utils import *
nltk.download('punkt')

def get_stem(wordStr):
    porter = PorterStemmer()
    stemmed = porter.stem(wordStr)
    return stemmed

def merge_postings(postings1, postings2):
    merged_postings = []
    i, j = 0, 0

    if len(postings1) == 0:
        return postings2
    if len(postings2) == 0:
        return postings1

    while i < len(postings1) and j < len(postings2):
        doc_id1, tf1, pos1, tpos1 = postings1[i]
        doc_id2, tf2, pos2, tpos2 = postings2[j]

        if doc_id1 < doc_id2:
            merged_postings.append((doc_id1, tf1, pos1, tpos1))
            i += 1
        else:
            merged_postings.append((doc_id2, tf2, pos2, tpos2))
            j += 1

    while i < len(postings1):
        merged_postings.append(postings1[i])
        i += 1
    while j < len(postings2):
        merged_postings.append(postings2[j])
        j += 1

    return merged_postings

def create_main_index():
    main_ioi = {}
    main_index = open('main_index.txt', 'w', encoding= "utf-8")

    index1 = open('index1.txt', "r", encoding= "utf-8")
    index2 = open('index2.txt', "r", encoding= "utf-8")
    index3 = open('index3.txt', "r", encoding= "utf-8")

    i1json = open('index1.json', 'r')
    i2json = open('index2.json', 'r')
    i3json = open('index3.json', 'r')
    mapi1 = json.load(i1json)
    mapi2 = json.load(i2json)
    mapi3 = json.load(i3json)
    i1json.close()
    i2json.close()
    i3json.close()

    i1keys = set(mapi1.keys())
    i2keys = set(mapi2.keys())
    i3keys = set(mapi3.keys())
    all_keys = i1keys.union(i2keys, i3keys)
    for key in all_keys:
        term = ''
        df = 0
        pl1 = 0
        pl2 = 0
        pl3 = 0
        byte_num1 = mapi1.get(key)
        byte_num2 = mapi2.get(key)
        byte_num3 = mapi3.get(key)
        if byte_num1 == None:
            pl1 = []
        else:
            index1.seek(byte_num1)
            line =  index1.readline().rstrip('\n').split(': ')
            term = line[0]
            df += int(line[1])
            pl1 = eval(line[2])

        if byte_num2 == None:
            pl2 = []
        else:
            index2.seek(byte_num2)
            line =  index2.readline().rstrip('\n').split(': ')
            term = line[0]
            df += int(line[1])
            pl2 = eval(line[2])

        if byte_num3 == None:
            pl3 = []
        else:
            index3.seek(byte_num3)
            line =  index3.readline().rstrip('\n').split(': ')
            term = line[0]
            df += int(line[1])
            pl3 = eval(line[2])
        
        m1 = merge_postings(pl1, pl2)
        merged_pl = merge_postings(m1, pl3)
        current_byte = main_index.tell()
        main_ioi[term] = current_byte
        line = f"{term}: {df}: {merged_pl}\n"
        main_index.write(line)

    with open('main_index.json', 'w') as mioi_file:
        json.dump(main_ioi, mioi_file)
    
    index1.close()
    index2.close()
    index3.close()
    main_index.close()


if __name__ == '__main__':
    create_main_index()
    print("Finished creating main index!")
    