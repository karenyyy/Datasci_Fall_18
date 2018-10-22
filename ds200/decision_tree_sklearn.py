import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report


class DT(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def load_dataset(self):
        dataset = pd.read_csv(self.dataset_path, sep=',', header=None)
        X = dataset.values[:, 1:]
        y = dataset.values[:, 0]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=100)
        return X, y, X_train, X_test, y_train, y_test

    def fit(self, criterion, X_train, y_train):
        clf = DecisionTreeClassifier(criterion=criterion,
                                     random_state=100, max_depth=3, min_samples_leaf=5)
        clf.fit(X_train, y_train)
        return clf

    def predict(self, clf, X_test):
        y_predicted = clf.predict(X_test)
        return y_predicted

    def accuracy(self, y_test, y_predicted):
        cm = confusion_matrix(y_test, y_predicted)
        score = accuracy_score(y_test, y_predicted) * 100
        report = classification_report(y_test, y_predicted)
        return cm, score, report


if __name__ == "__main__":
    dataset_path = 'https://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/balance-scale.data'
    dt = DT(dataset_path)
    X, y, X_train, X_test, y_train, y_test = dt.load_dataset()

    # gini
    clf = dt.fit(criterion='gini', X_train=X_train, y_train=y_train)
    y_pred = dt.predict(clf=clf, X_test=X_test)
    cm, score, report = dt.accuracy(y_test=y_test, y_predicted=y_pred)
    print(cm)
    print(score)
    print(report)

    # entropy
    clf = dt.fit(criterion='entropy', X_train=X_train, y_train=y_train)
    y_pred = dt.predict(clf=clf, X_test=X_test)
    cm, score, report = dt.accuracy(y_test=y_test, y_predicted=y_pred)
    print(cm)
    print(score)
    print(report)
