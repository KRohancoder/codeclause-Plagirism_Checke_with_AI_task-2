# -*- coding: utf-8 -*-
"""

Project Name : Plagiarism Detector in Python using Machine Learning Techniques

Program Description :
---------------------
The program reads text files from the folder, named as Docs under the current 
working directory. It reads all the text files having names Text_?.txt where ?
is to be replaced with any digit between 0 to 9.

The program applies word embedding techniques and first converts the textual 
data, read from the files, into an array of numbers (word vectors) using 
Term frequency-inverse document frequency (TF-IDF) method. For this purpose, 
TfidfVectorizer of scikit-learn built-in features is used.

All the pairs of word vecotrs are then processed for checking of any plagiarism 
between the corresponding text files. This is accomplished by computing the 
value of cosine similarity between the vectors representations of the concerned
text files.

Finally, a table of plagiarism percentage between every pair of files, read 
from the Docs folder is prepared along with presenting the result in Bar Graph.

Requirements :
--------------
The program requires scikit-learn to be installed in the machine.

References :
https://scikit-learn.org/
https://www.turing.com/kb/guide-on-word-embeddings-in-nlp
https://www.analyticsvidhya.com/blog/2017/06/word-embeddings-count-word2veec/
https://www.geeksforgeeks.org/word-embeddings-in-nlp/
https://dev.to/kalebu/how-to-detect-plagiarism-in-text-using-python-dpk
https://towardsdatascience.com/simple-plagiarism-detection-in-python-2314ac3aee88
https://www.geeksforgeeks.org/word-embeddings-in-nlp/
https://www.geeksforgeeks.org/cosine-similarity/

"""
#---------- Import the libraries.
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
    
import matplotlib.pyplot as plt
import numpy as np

#---------- Function for displaying the result in Bar Graph
def disp_bar(data):
    x = []
    y = []
    for data in result:
        s = data[0][:data[0].index('.txt')]+' vs. '+data[1][:data[1].index('.txt')]
        x.insert(0,s)
        y.insert(0,data[2])
    h = 1/len(x)-1
    plt.barh(x,y,height=h)
    plt.title('Percentage of Plagiarism')
    plt.ylabel('%')
    plt.xlabel('')
    plt.show()

#---------- Function for comparing documents
def compare_docs():
    global doc_vectors
    #table_scores = set()
    table_scores = []
    vec_len = len(doc_vectors)
    for index1 in range(vec_len-1):
        doc_1 = doc_vectors[index1][0]
        vector_1 = doc_vectors[index1][1]
        print(str(index1+1)+' \n Compairing the document file '+doc_1+' with rest of the files .....')
        for index2 in range(index1+1,vec_len):
            doc_2 = doc_vectors[index2][0]
            vector_2 = doc_vectors[index2][1]
            score = cosine_similarity([vector_1, vector_2])
            doc_pair_score = (doc_1, doc_2, 100*score[0][1])
            #print(doc_pair_score)
            #table_scores.add(doc_pair_score)
            table_scores.append(doc_pair_score)
    return table_scores

#---------- Find the files having names Text_?.txt from the folder, named as 
#---------- Docs, under the current working directory and create the list of files.

list_files = [f for f in os.listdir('.\\') if re.search("^Text_[0-9].txt",f)]
list_files.sort()
print('\n List of files found in the Docs folder under the current working directory .....\n')
print(list_files)

#---------- Load the documents from the text files.
list_docs = [open('.\\'+f, encoding='utf-8').read()
                 for f in list_files]

#---------- Create the model of word vectors (document-term matrix) using 
#---------- TF-IDF for all the loaded documents. 
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(list_docs).toarray()

print('\nShape of the vectors : ',str(vectors.shape))
print('\nList of distinct words found in all the documents .....\n')
print(vectorizer.get_feature_names_out())
#print(vectors)

#---------- Create the list combining the vectors with the respective file names.
doc_vectors = list(zip(list_files, vectors))

#---------- Compute the score for checking the percentage of plagiarism among
#---------- the loaded text files.
result = compare_docs()

#---------- Display the result.
print('\n------------------------------ Result ------------------------------')
print('\t {:27} \t\t\t {}'.format('       Document Pairs', "Plagiarism %"))
print('\t------------------------------------------------------')
for data in result:
    print('\t {:11}  vs.  {:11} \t\t\t {:8.5} %\n'.format(data[0], data[1], data[2]))

#---------- Draw the Bar Graph against the result.
disp_bar(result)

