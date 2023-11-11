# Author: Jonathan Tran
# UCInetID: tranjt7
import os
import json
import nltk
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from bs4 import BeautifulSoup
from utils import *
nltk.download('punkt')


def create_index():
    parent_folder = os.getcwd() + '\developer\DEV'
    inverted_index = {}
    index_size = 0
    index_fileCount = 0
    porter = PorterStemmer() 

    # Variables for logging analytics
    unique_wordsSet = set()
    indexed_docCount = 0

    ''' Walk through all json files and add them to the inverted index.
        Once 20,000 json files have been processed, create a partial index file and clear the inverted_index.
        At the end, 3 partial indexes will be created. 
    '''
    for subfolder in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, subfolder)
        for filename in os.listdir(folder_path):
            if (filename.endswith('.json')):
                file_path = os.path.join(folder_path, filename)
                if (os.path.isfile(file_path)):
                    if (index_size >= 20000):
                        index_fileCount += 1
                        index_file = 'index' + str(index_fileCount) + '.json'
                        with open(index_file, 'w') as i_file:
                            json.dump(inverted_index, i_file)
                            inverted_index.clear()
                            index_size = 0

                    with open(file_path, 'r') as open_file:
                        json_data = json.load(open_file)
                        url = json_data['url']
                        content = json_data['content']
                        #encoding = json_data['encoding']
                        doc_id = get_urlhash(url)
                        content_soup = BeautifulSoup(content, 'lxml')
                        content_text = content_soup.get_text()
                        tokens = word_tokenize(content_text)
                        #stemmed_tokens = [porter.stem(token) for token in tokens]
                        token_freqDict = computeWordFrequencies(tokens)
                        for term, freq in token_freqDict.items():
                            inverted_index.setdefault(term, list())
                            posting = (doc_id, freq)
                            inverted_index[term].append(posting)
                            # Logging
                            unique_wordsSet.add(term)
                        index_size += 1
                        # Logging
                        indexed_docCount += 1

    index_fileCount += 1
    index_file = 'index' + str(index_fileCount) + '.json'
    with open(index_file, 'w') as i_file:
        json.dump(inverted_index, i_file)
        inverted_index.clear()
        index_size = 0
    
    # Display index analytics
    index_folder_path = os.getcwd()
    printAnalytics(unique_wordsSet, indexed_docCount, index_folder_path)
    

if __name__ == "__main__":
    create_index()
