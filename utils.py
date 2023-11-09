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
    pass

def printAnalytics(unique_set, num_docs, folder_path):
    pass