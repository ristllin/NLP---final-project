#Libraries
import sys, os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import csv
import random
import string

#Modules
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from CNN import run_cnn
from RNN import run_rnn
from SVM import run_svm
from k_nearest_neighbor import run_kneighbors
from Bert import run_bert
import os

bert_folder = os.path.join("Bert-Multi-Label-Text-Classification-master","pybert","dataset")

def run_classifiers():
    print("running")
    input_csv = pd.read_csv('tweets_emojies.csv')
    input_csv = input_csv.dropna()
    tweets = input_csv['tweet']
    print("loading DB")
    labels = LabelEncoder().fit_transform(input_csv['label'])
    num_labels = len(list(set(labels)))
    label_list = [str(num) for num in list(set(labels))]
    print("splitting")
    X_train, X_test, y_train, y_test = train_test_split(tweets, labels, test_size=0.33, random_state=42)
    with open('classifiers_results.csv', mode='w',  encoding="utf-8") as cls_res_file:
        writer = csv.DictWriter(cls_res_file, fieldnames=list(['Tweet', 'Bert', 'CNN', 'RNN', 'SVM', 'KNeighbors']))
        writer.writeheader()
        print("Running Bert")
        bert_test_res = run_bert(X_train, X_test, y_train, y_test, label_list)
        print("Running CNN")
        cnn_test_res = run_cnn(X_train, X_test, y_train, y_test, num_labels)
        print("Running RNN")
        rnn_test_res = run_rnn(X_train, X_test, y_train, y_test, num_labels)
        print("Running SVM")
        svm_test_res = run_svm(X_train, X_test, y_train, y_test)
        print("Running K-neighbours")
        kneighbors_test_res = run_kneighbors(X_train, X_test, y_train, y_test)
        for tweet, bert_res, cnn_res, rnn_res, svm_res, kneighbors_res in zip(X_test, bert_test_res, cnn_test_res, rnn_test_res, svm_test_res, kneighbors_test_res):
            writer.writerow({'Tweet':tweet, 'Bert':bert_res ,'CNN':cnn_res, 'RNN':rnn_res, 'SVM':svm_res, 'KNeighbors':kneighbors_res})



if __name__ == '__main__':
    run_classifiers()
