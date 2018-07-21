
import os
import re
import string
import pickle
import math
from pandas import DataFrame
path =r"C:\Users\Hasitha\Downloads\20_newsgroups"

# get the list of 20 news catagories....
def get_cat_list():
    return os.listdir(path)

# open the files from each catagories
def get_files_from_cat(cat):
    fileNameList = os.listdir(path+"\\"+cat)
    files=[]
    for a in fileNameList:
        file =open(path+"\\"+cat+"\\"+a)
        files.append(file)
    return files

# remove punctuations and clean the string
def remove_punctuations_and_clean(a):
    a = a.replace('\r', '').replace('\n', ' ')
    for c in string.punctuation:
        a= a.replace(c," ")
    a=re.sub(' +',' ',a)
    return a

# to create vocabulary, get words in given catagory
def list_words_in_cat(c):
    words=[]
    a= get_files_from_cat(c)
    for b in a:
        l=b.read()        
        l=remove_punctuations_and_clean(l)
        words=words+l.split()
    return words

# split the given string to words and clean  
def get_word_list_from_string(string):
    words=[]
    l=remove_punctuations_and_clean(string)
    words=words+l.split()
    return words

# read all documents from all catagories and create word corpos
def get_vocabulary():
    vocabulary={}
    for r in get_cat_list():
        w=list_words_in_cat(r)
        print(len(w))
        for a in w:
            vocabulary[a]=1
    return vocabulary

# create the p(o|H) values for all words
def get_prob_Poh(vocabulary):    
    cats = get_cat_list()
    p_word_given_cat={}
    for cat in cats:
        print(cat)
        word_list_from_cat= list_words_in_cat(cat)
        p_word_given_cat[cat]={}
        for word in vocabulary.keys():
             p_word_given_cat[cat][word]=1.0
        for word in word_list_from_cat:
            if word in vocabulary:
                 p_word_given_cat[cat][word] += 1.0
        for word in vocabulary.keys():
            p_word_given_cat[cat][word]=(p_word_given_cat[cat][word])/(len(vocabulary)+len(word_list_from_cat));
        print(len(p_word_given_cat[cat]))
    return p_word_given_cat
        
# create the tast data set
def list_strings_in_cat_test(cat,size):
    words_test={}
    a = get_files_from_cat(cat);
    counter =0
    for b in a[size:]:
        words_test[counter]=""
        l=b.read()    
        words_test[counter]=l
        counter+=1
    return words_test

# testing the accuracy from test dataset
def test_accuracy(size,prob_Poh,voc):
    cats=get_cat_list()
    overall=0
    length=0
    for cat in cats:
        test_data=list_strings_in_cat_test(cat,size)
        success_predicts=0
        for i in range (0,len(test_data)):
            a=classifier(test_data[i],prob_Poh,voc)
            if (a==cat):
                success_predicts+=1
        length+=len(test_data)
        overall+=success_predicts
    return (overall/(length))

# classifier
def classifier(text_to_classify,prob_Poh,vocabulary):
    max_group=""
    max_prob=1
    for candidate_group in get_cat_list():
        p=math .log(1/20)
        for word in get_word_list_from_string(text_to_classify):
            if word in vocabulary:
                p=p+math .log(prob_Poh[candidate_group][word])      
        if (p>max_prob or max_prob==1):            
            max_prob=p
            max_group=candidate_group    
    return max_group

# confusion matrix genarater
def confusion_matrix(size,prob_Poh,voc):
    cats=get_cat_list()
    c_matrix={}
    for cat in cats:
        c_matrix[cat]={}
        for catInside in cats:
            c_matrix[cat][catInside]=0
    for cat in cats:
        test_data=list_strings_in_cat_test(cat,size)        
        for i in range (0,len(test_data)):
            a=classifier(test_data[i],prob_Poh,voc)
            c_matrix[cat][a]+=1
    return c_matrix

# saving confusion matrix to a excel file
def save_confusion_matrix_to_excel_file(c):
    df = DataFrame(c)
    df.to_excel('test.xlsx', sheet_name='sheet1', index=False)


# ///////////// RUN

voc=get_vocabulary()
prob_Poh=get_prob_Poh(voc)

print(test_accuracy(980,prob_Poh,voc))

c=confusion_matrix(900,prob_Poh,voc)
save_confusion_matrix_to_excel_file(c)

