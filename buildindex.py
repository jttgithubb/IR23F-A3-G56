# Author: Jonathan Tran
# UCInetID: tranjt7
import os
import json
import nltk
from bs4 import BeautifulSoup

def create_index():
    parent_folder = os.getcwd() + '\developer\DEV'
    inverted_index = {}

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
                    pass

    



if __name__ == "__main__":
    print("Hello from main!")
    create_index()
