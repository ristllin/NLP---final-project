#Libraries
import sys, os
import pandas as pd
from sklearn.model_selection import train_test_split

#Modules
file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from CNN import run_cnn
from RNN import run_rnn
from SVM import run_svm
from k_nearest_neighbor import run_kneighbors


def run_classifiers():
    print("running")
    csv = pd.read_csv('tweets_emojies.csv')
    csv = csv.dropna()
    csv_label_fields = list(csv.columns.values)
    csv_label_fields.pop(0)
    tweets = csv['tweet']
    labels = []
    print("loading DB")
    for i in range(len(tweets)):
        number = 0
        for j, label in enumerate(csv_label_fields):
            print(j,label)
            label_column = list(csv[label])
            number += (2 ^ j) * label_column[i]
        labels.append(number)
        print(i)
        # if i % 100 == 0: print("tweet:",i)
    map_label_to_index_label = {l:i for i,l in enumerate(set(labels))}
    index_labels = [map_label_to_index_label[l] for l in labels]
    num_lables = len(set(index_labels))
    print("splitting")
    X_train, X_test, y_train, y_test = train_test_split(tweets, index_labels, test_size=0.33, random_state=42)
    print("Running CNN")
    run_cnn(X_train, X_test, y_train, y_test, num_lables)
    print("Running RNN")
    run_rnn(X_train, X_test, y_train, y_test, num_lables)
    print("Running SVM")
    run_svm(X_train, X_test, y_train, y_test)
    print("Running K-neighbours")
    run_kneighbors(X_train, X_test, y_train, y_test)

if __name__ == '__main__':
    run_classifiers()
