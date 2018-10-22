from sklearn import datasets, linear_model
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_squared_log_error


def load_dataset(all_features=True, dim=2):
    diabetes = datasets.load_diabetes()
    y = diabetes.target
    if all_features:
        X = diabetes.data
    else:
        X = diabetes.data[:, np.newaxis, dim]
    return X, y


def split_dataset(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test


def regressor(model='linear', neighbors=5, metric='euclidean'):
    if model == 'linear':
        regressor_model = linear_model.LinearRegression()
    elif model == 'knn':
        regressor_model = KNeighborsRegressor(n_neighbors=neighbors, weights='uniform', algorithm='auto', metric=metric)
    return regressor_model


def fit(regressor_model, X, y):
    regressor_model.fit(X=X, y=y)
    return regressor_model


def predict(regressor_model, X):
    return regressor_model.predict(X=X)


def loss(y_real, y_pred, metric='mse'):
    if metric == 'mse':
        error = mean_squared_error(y_true=y_real, y_pred=y_pred)
    elif metric == 'mse_log':
        error = mean_squared_log_error(y_true=y_real, y_pred=y_pred)
    elif metric == 'mse_abs':
        error = mean_absolute_error(y_true=y_real, y_pred=y_pred)
    return error


def plot_scatter(X_train, y_train, X_test, y_test):
    cmap = plt.get_cmap('viridis')
    m1 = plt.scatter(X_train, y_train, color=cmap(0.9), s=10)
    m2 = plt.scatter(X_test, y_test, color=cmap(0.5), s=10)
    plt.legend((m1, m2), ("Training data", "Test data"), loc='lower right')
    return plt


def plot_line(X, y_pred, plt, error, linewidth=2, model='linear', metric='mse', color='black'):
    plt.plot(X, y_pred, color=color, linewidth=linewidth, label="Prediction")
    plt.title(model + "-" + metric + ": {0:.7g}\n".format(error), fontsize=10)


def grid_search_comparison(X_train, X_test, y_train, y_test,
                           lr_err, metric='mse', neighbors=200):
    kr_errs = []
    for neighbor in range(3, neighbors):
        kr = regressor(model='knn', neighbors=neighbor)
        kr = fit(regressor_model=kr, X=X_train, y=y_train)
        kr_y_pred = predict(regressor_model=kr, X=X_test)
        kr_err = loss(y_real=y_test, y_pred=kr_y_pred, metric=metric)
        kr_errs.append(kr_err)

    fig = plt.figure(figsize=(8, 8))
    plt.plot(range(3, neighbors), kr_errs)
    plt.hlines(lr_err, xmin=1, xmax=neighbors, colors='red')
    plt.title('Loss: {} Neighbors: {}'.format(metric, neighbors))
    return fig


def test_all_features():
    X, y = load_dataset()
    X_train, X_test, y_train, y_test = split_dataset(X, y)

    lr = regressor()

    lr = fit(regressor_model=lr, X=X_train, y=y_train)

    lr_y_pred = predict(regressor_model=lr, X=X_test)

    lr_mse = loss(y_real=y_test, y_pred=lr_y_pred)
    lr_mse_log = loss(y_real=y_test, y_pred=lr_y_pred, metric='mse_log')
    lr_mse_abs = loss(y_real=y_test, y_pred=lr_y_pred, metric='mse_abs')
    lr_err = [lr_mse, lr_mse_log, lr_mse_abs]

    metric = ['mse', 'mse_log', 'mse_abs']
    for idx, m in enumerate(metric):

        fig = grid_search_comparison(X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
                                         lr_err=lr_err[idx], metric=m)
        fig.savefig(fname='plots/{}.png'.format(m))


def test_single_feature():
    n_features = 10
    metric = ['mse', 'mse_log', 'mse_abs']
    for d in range(2, n_features):
        X, y = load_dataset(all_features=False, dim=d)
        X_train, X_test, y_train, y_test = split_dataset(X, y)
        fig = plt.figure(figsize=(8, 8))
        plt_ = plot_scatter(X_train, y_train, X_test, y_test)

        lr = regressor()
        lr = fit(regressor_model=lr, X=X_train, y=y_train)
        lr_y_pred = predict(regressor_model=lr, X=X_test)

        kr = regressor(model='knn', neighbors=20)
        kr = fit(regressor_model=kr, X=X_train, y=y_train)
        kr_y_pred = predict(regressor_model=kr, X=X_test)

        for me in metric:
            lr_err = loss(y_real=y_test, y_pred=lr_y_pred, metric=me)
            kr_err = loss(y_real=y_test, y_pred=kr_y_pred, metric=me)
            plot_line(X=X_test, y_pred=lr_y_pred, plt=plt_, model='linear',
                      metric=me, error=lr_err, color='black')
            plot_line(X=X_test, y_pred=kr_y_pred, plt=plt_, model='knn',
                      metric=me, error=kr_err, color='red', linewidth=0.1)
            fig.savefig(fname='out_pred_plots/' + me + '-feature{}.png'.format(d))


if __name__ == '__main__':
    # test_all_features()
    test_single_feature()
