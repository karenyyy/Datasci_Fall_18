import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
import seaborn as sns
from sklearn.utils import resample
import pickle

SEED = 1234


class BankDataProcessPipeline(object):

    def __init__(self, df, classifier=None, option='normalize'):
        """

        :param df: the bank dataset
        :param classifier: Logistic Regression, MLP, Decision Tree
        :param option: normalize, unnormalize
        """
        self.seed = SEED
        self.option = option
        self.classifier = classifier
        self.df = df
        self.X = self.df.iloc[:, :20]
        self.df.y = self.df.y.replace('no', 0)
        self.df.y = self.df.y.replace('yes', 1)
        self.y = self.df.y
        self.categorical_cols = self.X.columns[self.X.dtypes == object]
        self.numerical_cols = self.X.columns[self.X.dtypes != object]
        self.integrate_cat_nume()

    def custom_split(self, X, y, train_index, test_index):
        return X.take(train_index).reset_index(drop=True), \
               X.take(test_index).reset_index(drop=True), \
               y.take(train_index).reset_index(drop=True), \
               y.take(test_index).reset_index(drop=True)

    def scale(self, cols, range_=(0, 1)):
        """

        :param cols: the column to be normalized
        :param range_:
            if the data > 0, then the normalize range is set to be (0,1);
            if the data < 0, then the normalize range is set to be (-1,0);
            if the data contains both positive and negative value, then the normalize range is set to be (-1,1);
        :return: the normalized column
        """
        min_max_scaler_p = MinMaxScaler(feature_range=range_)
        return min_max_scaler_p.fit_transform(self.X[cols])

    def one_hot_categorical(self):
        """

        :return: the one-hot encoding of the categorical columns
        """
        one_hot_encoded_cat = pd.DataFrame()
        for col in self.categorical_cols:
            one_hot_encoded_cat = pd.concat(
                [one_hot_encoded_cat, pd.get_dummies(self.X[col], prefix='{}_is'.format(col))], axis=1)
        return one_hot_encoded_cat

    def normalize_numerical(self):
        """

        :return: the normalized numerical columns
        """
        bank_numericals = self.X[self.numerical_cols]
        p_mask = list(map(lambda x: all(bank_numericals[x] >= 0), self.numerical_cols))
        n_mask = list(map(lambda x: all(bank_numericals[x] < 0), self.numerical_cols))
        p_n_mask = list(map(lambda x: not (all(bank_numericals[x] >= 0) or
                                           all(bank_numericals[x] < 0)), self.numerical_cols))
        p_cols = self.numerical_cols[p_mask]
        n_cols = self.numerical_cols[n_mask]
        p_n_cols = self.numerical_cols[p_n_mask]
        scaled_p = pd.DataFrame(self.scale(p_cols), columns=p_cols)
        scaled_n = pd.DataFrame(self.scale(n_cols, range_=(-1, 0)), columns=n_cols)
        scaled_p_n = pd.DataFrame(self.scale(p_n_cols, range_=(-1, 1)), columns=p_n_cols)
        scaled_bank_numericals = pd.concat([scaled_p, scaled_n, scaled_p_n], axis=1)
        return scaled_bank_numericals

    def integrate_cat_nume(self):
        if self.option == 'normalize':
            self.X = pd.concat([self.one_hot_categorical(), self.normalize_numerical()], axis=1)
        else:
            self.X = pd.concat([self.one_hot_categorical(), self.X[self.numerical_cols]], axis=1)

    def check_imbalance(self):
        no_cnt = self.y[self.y == 0].shape[0]
        yes_cnt = self.y[self.y == 1].shape[0]
        print('There are {} data entries labeled as yes, {} data entries labeled as no.'.format(yes_cnt, no_cnt))
        sns.countplot("y", data=pd.DataFrame(self.y, columns=['y']))
        plt.show()

    def feature_select(self, pickle_path):
        """

        :param pickle_path: use the selected features provided
        :return: the selected features
        """
        with open(pickle_path, 'rb') as f:
            data = pickle.load(f)
        feature_selected_X = pd.concat([pd.DataFrame(data['categorical'],
                                                     columns=['categorical_{}'.format(i) for i in
                                                              range(data['categorical'].shape[1])]),
                                        pd.DataFrame(data['numerical'],
                                                     columns=['numerical_{}'.format(i) for i in
                                                              range(data['numerical'].shape[1])])], axis=1)
        return feature_selected_X

    def fit(self, X_train, y_train):
        self.classifier.fit(X_train, y_train)

    def predict(self, X_test):
        return self.classifier.predict(X_test)

    def plot_cm(self, cm, cmap=plt.cm.Blues):
        sns.heatmap(cm, cmap=cmap, annot=True)
        plt.show()

    def eval_results(self, predicted_y_test, y_test):
        """

        :param predicted_y_test: the predicted value of y
        :param y_test: the ground truth of y
        :return:
            accuracy score;
            precision score;
            recall score;
            f1 score;
            confusion matrix;
        """
        accuracy_s = accuracy_score(y_test, predicted_y_test)
        precision_s = precision_score(y_test, predicted_y_test)
        recall_s = recall_score(y_test, predicted_y_test)
        f1_s = f1_score(y_test, predicted_y_test)
        cm = confusion_matrix(y_test, predicted_y_test)
        print("Accuracy Score:", accuracy_s)
        print("Precision Score:", precision_s)
        print("Recall Score:", recall_s)
        print("f1 Score:", f1_s)
        print('confusion_matrix is: \n', cm, '\n')
        return accuracy_s, precision_s, recall_s, f1_s, cm

    def resample(self, X_train, y_train, fold, option, downratio=1, upratio=1):
        """

        :param fold: the number of folds of the cross validation
        :param option: noresample, downsample, upsample
        :param downratio: majority/original minority
        :param upratio: minority/original majority
        :return:
            if the option is 'noresample', then return the original X_train, y_train;
            if the option is 'downsample', then return the downsampled X_train, downsample y_train;
            if the option is 'upsample', then return the upsampled X_train, upsampled y_train
        """
        tmp_df = pd.concat([X_train, y_train], axis=1)
        no_idx = tmp_df[tmp_df.y == 0].index
        yes_idx = tmp_df[tmp_df.y == 1].index
        df_majority = tmp_df.iloc[no_idx, :]
        df_minority = tmp_df.iloc[yes_idx, :]
        majority_cnt = df_majority.shape[0]
        minority_cnt = df_minority.shape[0]
        if option == 'downsample':
            df_majority_downsampled = resample(df_majority,
                                               replace=False,
                                               n_samples=minority_cnt * downratio,
                                               random_state=self.seed)
            df_downsampled = pd.concat([df_majority_downsampled, df_minority], axis=0)
            if fold == 1:
                print(
                    'After downsampling, there are {} data entries labeled as yes.\n There are {} data entries '
                    'labeled as no.'.format(
                        len(df_downsampled[df_downsampled.y == 1]),
                        len(df_downsampled[df_downsampled.y == 0])))

                plt.figure(figsize=(5, 5))
                sns.countplot("y", data=df_downsampled)
                plt.show()
            return df_downsampled.iloc[:, :-1], df_downsampled.y
        elif option == 'upsample':
            df_minority_upsampled = resample(df_minority,
                                             replace=True,
                                             n_samples=int(majority_cnt * upratio),
                                             random_state=self.seed)
            df_upsampled = pd.concat([df_minority_upsampled, df_majority])
            if fold == 1:
                print(
                    'After upsampling, there are {} data entries labeled as yes.\n There are {} data entries labeled '
                    'as no.'.format(
                        len(df_upsampled[df_upsampled.y == 1]),
                        len(df_upsampled[df_upsampled.y == 0])))
                plt.figure(figsize=(5, 5))
                sns.countplot("y", data=df_upsampled)
                plt.show()
            return df_upsampled.iloc[:, :-1], df_upsampled.y
        else:
            return X_train, y_train

    def k_fold_cross_val(self, fold, option='noresample', downratio=1, upratio=1, feature_engineered=False, topK=None):
        """

        :param fold: the number of folds of the cross validation
        :param option: noresample, downsample, upsample
        :param downratio: majority/original minority
        :param upratio: minority/original majority
        :param feature_engineered: True, False
        :param topK: the top k selected features
        :return: the metrics statistics of:
            accuracy score;
            precision score;
            recall score;
            f1 score;
        """
        f = 1
        accuracy = []
        precision = []
        recall = []
        f1 = []

        if feature_engineered:
            X = self.feature_select(pickle_path='feature_selection/feature_k={}.pkl'.format(topK))
        else:
            X = self.X
        y = self.y
        skf = StratifiedKFold(n_splits=fold, random_state=1, shuffle=True)

        print('The shape of training set is: ', X.shape, '\n')
        for train_index, test_index in skf.split(X, y):
            X_train, X_test, y_train, y_test = self.custom_split(X, y, train_index, test_index)
            X_train, y_train = self.resample(X_train, pd.DataFrame(y_train, columns=['y']), fold=f, option=option,
                                             downratio=downratio, upratio=upratio)

            self.fit(X_train, y_train)
            predicted_y_test = self.predict(X_test)
            accuracy_s, precision_s, recall_s, f1_s, cm = self.eval_results(predicted_y_test, y_test)

            accuracy.append(accuracy_s)
            precision.append(precision_s)
            recall.append(recall_s)
            f1.append(f1_s)
            self.plot_cm(cm)
            f += 1

        metrics_df = pd.DataFrame(
            {'accuracy': accuracy,
             'precision': precision,
             'recall': recall,
             'f1': f1}
        )
        metrics_df.plot()
        return metrics_df


if __name__ == '__main__':
    bank = pd.read_csv('bank-additional-full.csv', sep=';')

    '''
    Task 1
    '''
    classifier = LogisticRegression(random_state=SEED, solver='lbfgs')

    # Logistic Regression Model 1
    bdpp_logistic = BankDataProcessPipeline(bank, classifier)
    bdpp_logistic.k_fold_cross_val(fold=5)

    # Logistic Regression Model 2
    bdpp_logistic = BankDataProcessPipeline(bank, classifier, option='unnormalize')
    bdpp_logistic.k_fold_cross_val(fold=5)

    '''
    Task 2
    '''
    bdpp_logistic = BankDataProcessPipeline(bank, classifier)
    bdpp_logistic.check_imbalance()

    # Downsampling
    bdpp_logistic.k_fold_cross_val(fold=5, option='downsample')
    bdpp_logistic.k_fold_cross_val(fold=5, option='downsample', downratio=2)
    bdpp_logistic.k_fold_cross_val(fold=5, option='downsample', downratio=3)

    # Upsampling
    bdpp_logistic.k_fold_cross_val(fold=5, option='upsample')
    bdpp_logistic.k_fold_cross_val(fold=5, option='upsample', upratio=0.7)
    bdpp_logistic.k_fold_cross_val(fold=5, option='upsample', upratio=0.5)
    bdpp_logistic.k_fold_cross_val(fold=5, option='upsample', upratio=0.3)

    '''
    Task 3
    '''
    bdpp_logistic = BankDataProcessPipeline(bank, classifier)
    bdpp_logistic.k_fold_cross_val(fold=5, feature_engineered=True, topK=1)
    bdpp_logistic.k_fold_cross_val(fold=5, feature_engineered=True, topK=3)
    bdpp_logistic.k_fold_cross_val(fold=5, feature_engineered=True, topK=5)

    '''
    Task 4
    '''
    lr = LogisticRegression(random_state=SEED, solver='lbfgs')
    dt = DecisionTreeClassifier(criterion='entropy', random_state=SEED)
    mlp = MLPClassifier(random_state=SEED)

    # Unbalanced Dataset

    ## LogisticRegression
    bdpp_logistic = BankDataProcessPipeline(df=bank, classifier=lr)
    bdpp_logistic.k_fold_cross_val(fold=5)

    ## DecisionTree
    bdpp_dt = BankDataProcessPipeline(df=bank, classifier=dt)
    bdpp_dt.k_fold_cross_val(fold=5)

    ## MultilayerPerceptron
    bdpp_mlp = BankDataProcessPipeline(df=bank, classifier=mlp)
    bdpp_mlp.k_fold_cross_val(fold=5)

    # Balanced Dataset

    ## LogisticRegression
    bdpp_logistic = BankDataProcessPipeline(df=bank, classifier=lr)
    ### Downsample
    bdpp_logistic.k_fold_cross_val(fold=5, option='downsample')
    ### Upsample
    bdpp_logistic.k_fold_cross_val(fold=5, option='upsample')

    ## DecisionTree
    bdpp_dt = BankDataProcessPipeline(df=bank, classifier=dt)
    ### Downsample
    bdpp_dt.k_fold_cross_val(fold=5, option='downsample')
    ### Upsample
    bdpp_dt.k_fold_cross_val(fold=5, option='upsample')

    ## MultilayerPerceptron
    bdpp_mlp = BankDataProcessPipeline(df=bank, classifier=mlp)
    ### Downsample
    bdpp_mlp.k_fold_cross_val(fold=5, option='downsample')
    ### Upsample
    bdpp_mlp.k_fold_cross_val(fold=5, option='upsample')
