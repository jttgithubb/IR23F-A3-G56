# IR23F-A3-G56
Jonathan Tran tranjt7 13147853

Steps for Building the Final Index
1. Make sure that the corpus "developer/DEV" is included within the directory.
2. Run the buildindex.py file which will create 3 partial indexes with their respective json files called index1.txt, index2.txt, and index3.txt. The json file mapping docids to urls is also created.
3. Run the mergeindex.py file which will merge the partial indexes and create a main index file and its respective json file for access.
4. Run the buildchampions.py file which will create the final index called champions_index.txt and a lower tier index called lower_champions_index.txt. Their json files are also created for easy access. These are two final indexes that will be used in combination during query evaluation.

Steps for Running the Ranked Retrieval Search System
1. Run the rankedsearch.py file.
2. Type any query into the console input after the '> ' symbol.
3. Top 10 search results will be displayed and the process can be repeated.
