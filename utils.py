import os
from hashlib import sha256
from urllib.parse import urlparse


def get_urlhash(url):
    parsed = urlparse(url)
    return sha256(
        f"{parsed.netloc}/{parsed.path}/{parsed.params}/"
        f"{parsed.query}/{parsed.fragment}".encode("utf-8")).hexdigest()

def computeWordFrequencies(tokenList):
    wordFreqDict = {}
    for token in tokenList:
        wordFreqDict.setdefault(token, 0)
        wordFreqDict[token] += 1
    return wordFreqDict

def calc_file_size(file_path):
    if (not os.path.exists(file_path)):
        return 0
    byte_file_size = os.path.getsize(file_path)
    kb__file_size = byte_file_size / 1024
    return kb__file_size

def printAnalytics(unique_set, num_docs, folder_path):
    print("Index Analytics:")
    print("\tNumber of indexed documents:", num_docs)
    print("\tNumber of unique words:", len(unique_set))
    total_index_size = 0
    for file_name in os.listdir(folder_path):
        if (file_name.endswith('.txt')):
            file_path = os.path.join(folder_path, file_name)
            if (os.path.isfile(file_path)):
                kb_size = calc_file_size(file_path)
                total_index_size += kb_size
    print("\tTotal size of index on disk:", total_index_size, "kilobytes")
    