import sys, os
import pandas as pd
from sklearn.model_selection import train_test_split
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from CNN import run_cnn
from RNN import run_rnn
from SVM import run_svm
from K-nearest_Neighbors import run_kneighbors

def run_classifiers():
    csv = pd.read_csv('tweets_emojies.csv')
    csv = csv.dropna()
    csv_label_fields = list(csv.columns.values)
    csv_label_fields.pop(0)
    tweets = csv['tweet']
    labels = []
    for i in range(len(tweets)):
        number = 0
        for j, label in enumerate(csv_label_fields):
            number += (2 ^ j) * csv[label][i]
        labels.append(number)
    X_train, X_test, y_train, y_test = train_test_split(tweets, labels, test_size=0.33, random_state=42)
    run_cnn(X_train, X_test, y_train, y_test)
    run_rnn(X_train, X_test, y_train, y_test)
    run_svm(X_train, X_test, y_train, y_test)
    run_kneighbors(X_train, X_test, y_train, y_test)

if __name__ == '__main__':
    run_classifiers()
