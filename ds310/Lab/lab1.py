import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import mean_squared_error, roc_curve, auc

SEED = 1234
SPLIT_RATIO = 0.2

absent_df = pd.read_csv('Absenteeism_at_work.csv', sep=',')


class Model(object):
    def __init__(self, X=None, y=None):
        self.seed = SEED
        self.split_ratio = SPLIT_RATIO
        self.model = None
        self.X = X
        self.y = y

    def simple_split(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X,
                                                            self.y,
                                                            test_size=self.split_ratio,
                                                            random_state=self.seed)
        return X_train, X_test, y_train, y_test

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        return self.model.predict(X_test)

    def loss(self, X_train, X_test, y_train, y_test):
        return NotImplemented

    def cross_val_evaluate(self, fold=None, cross_val=False):
        return NotImplemented


class KNNClassifier(Model):
    def __init__(self):
        super(KNNClassifier, self).__init__(X=load_breast_cancer().data,
                                            y=load_breast_cancer().target)
        self.model = KNeighborsClassifier(n_neighbors=5)

    def fit(self, X_train, y_train):
        return super(KNNClassifier, self).fit(X_train, y_train)

    def predict(self, X_test):
        return super(KNNClassifier, self).predict(X_test)

    def loss(self, X_train, X_test, y_train, y_test):
        self.fit(X_train, y_train)
        y_pred = self.predict(X_test)
        fpr, tpr, thresholds = roc_curve(y_true=y_test, y_score=y_pred)
        auc_value = auc(fpr, tpr)
        return fpr, tpr, auc_value

    def plot_roc(self, fpr, tpr, auc_value, fold=None):
        plt.figure()
        plt.plot(fpr, tpr, color='red',
                 lw=2, label='ROC curve (area = %0.2f)' % auc_value)
        plt.plot([0, 1], [0, 1], lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        if fold != None:
            plt.title('ROC plot of fold {}, auc = {}'.format(fold, auc_value))
        else:
            plt.title('ROC plot, auc = {}'.format(auc_value))
        plt.legend(loc="lower right")
        plt.grid(True)
        plt.show()

    def cross_val_evaluate(self, fold=None, cross_val=False):
        if not cross_val:
            X_train, X_test, y_train, y_test = self.simple_split()
            _, _, auc_value = self.loss(X_train, X_test, y_train, y_test)
            return auc_value
        else:
            auc_lst = []
            skf = StratifiedKFold(n_splits=fold, random_state=self.seed, shuffle=True)
            fold = 1
            for train_index, test_index in skf.split(self.X, self.y):
                if self.X.__class__.__name__ == 'DataFrame':
                    X_train, X_test, y_train, y_test = self.X.iloc[train_index, :], self.X.iloc[test_index, :], self.y[train_index], self.y[
                        test_index]
                else:
                    X_train, X_test, y_train, y_test = self.X[train_index, :], self.X[test_index, :], self.y[train_index], self.y[
                        test_index]
                fpr, tpr, auc_value = self.loss(X_train, X_test, y_train, y_test)
                self.plot_roc(fpr, tpr, auc_value, fold=fold)
                auc_lst.append(auc_value)
                fold += 1
            return auc_lst, np.mean(auc_lst)


class LinearRegressionModel(Model):
    def __init__(self):
        super(LinearRegressionModel, self).__init__(X=absent_df.iloc[:, :-1],
                                                    y=absent_df.iloc[:, -1])
        self.model = LinearRegression(fit_intercept=True, normalize=True)

    def fit(self, X_train, y_train):
        super(LinearRegressionModel, self).fit(X_train, y_train)

    def predict(self, X_test):
        return super(LinearRegressionModel, self).predict(X_test)

    def loss(self, X_train, X_test, y_train, y_test):
        self.fit(X_train, y_train)
        y_pred = self.predict(X_test)
        return np.sqrt(mean_squared_error(y_true=y_test, y_pred=y_pred))

    def cross_val_evaluate(self, fold=None, cross_val=False):
        if not cross_val:
            X_train, X_test, y_train, y_test = self.simple_split()
            return self.loss(X_train, X_test, y_train, y_test)
        else:
            rmse_lst = []
            skf = StratifiedKFold(n_splits=fold, random_state=self.seed, shuffle=True)
            for train_index, test_index in skf.split(self.X, self.y):
                if self.X.__class__.__name__ == 'DataFrame':
                    X_train, X_test, y_train, y_test = self.X.iloc[train_index, :], self.X.iloc[test_index, :], self.y[train_index], self.y[
                        test_index]
                else:
                    X_train, X_test, y_train, y_test = self.X[train_index, :], self.X[test_index, :], self.y[train_index], self.y[
                        test_index]
                rmse = self.loss(X_train, X_test, y_train, y_test)
                rmse_lst.append(rmse)
            return rmse_lst, np.mean(rmse_lst)


class KNNRegressionModel(Model):
    def __init__(self,
                 dist='minkowski',
                 weights='distance',
                 algorithm='auto',
                 max_k=10,
                 max_p=10):
        super(KNNRegressionModel, self).__init__(X=absent_df.iloc[:, :-1],
                                                 y=absent_df.iloc[:, -1])
        self.X = absent_df.iloc[:, :-1]
        self.y = absent_df.iloc[:, -1]
        self.dist = dist
        self.weights = weights
        self.algorithm = algorithm
        self.max_k = max_k
        self.max_p = max_p
        self.model = None

    def knn_regression_model(self, k, p):
        return KNeighborsRegressor(n_neighbors=k,
                                   weights=self.weights,
                                   algorithm=self.algorithm,
                                   metric=self.dist,
                                   p=p)

    def fit(self, X_train, y_train):
        return super(KNNRegressionModel, self).fit(X_train, y_train)

    def predict(self, X_test):
        return super(KNNRegressionModel, self).predict(X_test)

    def loss(self, X_train, X_test, y_train, y_test):
        self.fit(X_train, y_train)
        y_pred = self.predict(X_test)
        return np.sqrt(mean_squared_error(y_true=y_test, y_pred=y_pred))

    def cross_val_evaluate(self, fold=None, cross_val=False):
        fold_lst = []
        k_lst = []
        p_lst = []
        rmse_lst = []
        skf = StratifiedKFold(n_splits=fold, random_state=self.seed, shuffle=True)
        fold = 1
        for train_index, test_index in skf.split(X, y):
            if self.X.__class__.__name__ == 'DataFrame':
                X_train, X_test, y_train, y_test = self.X.iloc[train_index, :], self.X.iloc[test_index, :], self.y[
                    train_index], self.y[
                                                       test_index]
            else:
                X_train, X_test, y_train, y_test = self.X[train_index, :], self.X[test_index, :], self.y[train_index], \
                                                   self.y[
                                                       test_index]
            for k in range(1, self.max_k + 1):
                for p in range(1, self.max_p + 1):
                    self.model = self.knn_regression_model(k, p)
                    rmse = self.loss(X_train, X_test, y_train, y_test)
                    fold_lst.append(fold)
                    k_lst.append(k)
                    p_lst.append(p)
                    rmse_lst.append(rmse)
            fold += 1
        df = pd.DataFrame({
            'fold': fold_lst,
            'k': k_lst,
            'p': p_lst,
            'rmse': rmse_lst
        })

        min_rmse_indexes = df.groupby(by=df['fold']).apply(lambda x: x.rmse.values.argmin())
        min_rmse_df = pd.DataFrame(
            df[df.fold == fold].iloc[min_rmse_indexes[fold], :] for fold in range(1, len(min_rmse_indexes) + 1))
        return df, min_rmse_df


if __name__ == '__main__':
    # auc_lst, avg_auc = KNNClassifier().cross_val_evaluate(fold=5, cross_val=True)
    # plt.plot(range(1, 6), auc_lst)
    # plt.title('The auc of 10-fold validation on the test data')
    # plt.show()
    # print('The average auc of the 10-fold cross validation is: {}.'.format(avg_auc))
    rmse_lst, avg_rmse = LinearRegressionModel().cross_val_evaluate(fold=10, cross_val=True)
    print(avg_rmse)
    # df, min_rmse_df = KNNRegressionModel().cross_val_evaluate(fold=10, cross_val=True)
    # print(min_rmse_df)
