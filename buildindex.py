# Author: Jonathan Tran
# UCInetID: tranjt7
import os
import json
import nltk
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
    docid_urlMap = {} 
    

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
                        index_file = 'index' + str(index_fileCount) + '.txt'
                        ioi_file = 'index' + str(index_fileCount) + '.json'
                        indexOfIndex = {}
                        with open(index_file, 'w', encoding= 'utf-8') as i_file:
                            for term,pl in inverted_index.items():
                                doc_freq = len(pl)
                                pl = sorted(pl, key=lambda x: x[0])
                                line = f"{term}: {doc_freq}: {pl}\n"
                                current_byte = i_file.tell()
                                indexOfIndex[term] = current_byte
                                i_file.write(line)
                            inverted_index.clear()
                            index_size = 0
                        with open(ioi_file, 'w') as i2_file:
                            json.dump(indexOfIndex, i2_file)

                    with open(file_path, 'r') as open_file:
                        json_data = json.load(open_file)
                        url = json_data['url']
                        content = json_data['content']
                        encoding = json_data['encoding']
                        content_bytes = content.encode(encoding, errors= 'replace')
                        content_str = content_bytes.decode(encoding, errors= 'replace')
                        doc_id = indexed_docCount
                        docid_urlMap[doc_id] = url
                        content_soup = BeautifulSoup(content_str, 'html.parser')
                        content_text = content_soup.get_text()
                        tokens = tokenize(content_text)
                        stemmed_tokens = [porter.stem(token) for token in tokens]
                        token_freqDict = computeWordFrequencies(stemmed_tokens)
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
    index_file = 'index' + str(index_fileCount) + '.txt'
    ioi_file = 'index' + str(index_fileCount) + '.json'
    indexOfIndex = {}
    with open(index_file, 'w', encoding= 'utf-8') as i_file:
        for term,pl in inverted_index.items():
            doc_freq = len(pl)
            pl = sorted(pl, key=lambda x: x[0])
            line = f"{term}: {doc_freq}: {pl}\n"
            current_byte = i_file.tell()
            indexOfIndex[term] = current_byte
            i_file.write(line)
        inverted_index.clear()
        index_size = 0
    with open(ioi_file, 'w') as i2_file:
        json.dump(indexOfIndex, i2_file)
    
    # Display index analytics
    index_folder_path = os.getcwd()
    printAnalytics(unique_wordsSet, indexed_docCount, index_folder_path)

    # Create the .json map for docid:url
    with open('id_url.json', 'w') as mapfile:
        json.dump(docid_urlMap, mapfile)
    
    # Produced 3 index .txt files, 3 .json files for indexing .txt files, and 1 .json for mapping id to url

if __name__ == "__main__":
    create_index()
