from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def run_kneighbors(X_train, X_test, y_train, y_test):
    """
    Create K Neighbors model using X_train y_train data and evaluate the model
    using X_test and y_test
    :param: X_train - train data
            X_test - test data
            y_train - train labels
            y_test - test labels
    :return: None
    """
    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', KNeighborsClassifier()),
                        ])
    text_clf.fit(X_train, y_train)
    predicted = text_clf.predict(X_test)
    print(predicted)
    print(metrics.classification_report(y_test, predicted))