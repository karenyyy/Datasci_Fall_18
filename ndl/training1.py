import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split



class LinearRegression(object):
    def __init__(self, filepath):
        self.data = pd.read_csv(filepath)
        self.X = self.data.X.values
        self.n_samples = self.X.size
        self.w = np.zeros((2, 1))
        self.X = np.hstack((np.ones((self.n_samples, 1)),
                            self.X.reshape((self.n_samples, 1))))
        self.y = self.data.y.values
        self.y = self.y.reshape((self.n_samples, 1))
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                test_size=0.2,
                                                                                random_state=100)
        self.learning_rate = 0.01
        self.num_iter = 1500

    def predict(self, X):
        return np.matmul(X, self.w)

    def cost_func(self, y_pred, y):
        return np.divide(0.5 * np.sum((y_pred - y) ** 2), self.n_samples)

    def gradient(self, X, y_pred, y):
        return np.divide(np.matmul(X.T, (y_pred - y)), self.n_samples)

    def main(self):
        for iter in range(self.num_iter):
            logit = self.predict(self.X_train)
            g = self.gradient(self.X_train, logit, self.y_train)
            self.w -= self.learning_rate * g
            logit = self.predict(self.X_train)
            c = self.cost_func(logit, self.y_train)
            plt.scatter(iter, c, c='r')
        plt.show()
        plt.scatter(self.X[:, 1], self.y[:, 0])
        y_pred = self.predict(self.X_test)
        plt.plot(self.X_test[:, 1], y_pred[:, 0], c='r')
        plt.show()


if __name__ == '__main__':
    filepath = 'data/linear_regression_data.csv'
    lr = LinearRegression(filepath)
    lr.main()

