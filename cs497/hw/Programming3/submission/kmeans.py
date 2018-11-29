# kmeans.py

import numpy as np
from sklearn.metrics import f1_score, normalized_mutual_info_score

THRESHOLD = 1e-5

def norm(x):
    """
    >>> Function you should not touch
    """
    max_val = np.max(x, axis=0)
    x = x / max_val
    return x


def rand_center(data, k):
    """
    >>> Function you need to write
    >>> Select "k" random points from "data" as the initial centroids.
    """
    n_samples, n_features = np.shape(data)
    centroids = np.zeros((k, n_features))
    for i in range(k):
        centroid = data[np.random.choice(range(n_samples))]
        centroids[i] = centroid
    print(">>> initial centroids")
    print(centroids)
    return centroids


def converged(centroids1, centroids2):
    """
    >>> Function you need to write
    >>> check whether centroids1==centroids
    >>> add proper code to handle infinite loop if it never converges
    """
    diff = np.sum(np.abs(np.sum(centroids1 - centroids2, axis=1)), axis=0)
    if np.equal(centroids1, centroids2).all():
        return True
    elif diff < THRESHOLD:
        return True
    else:
        return False


def euclidean_dist(x1, x2):
    return np.sqrt(np.sum(np.square(x1 - x2), axis=1))


def closest_centroid(val, centroids):
    return np.argmin(np.sqrt(np.sum(np.square(val - centroids), axis=1)))


def update_centroids(data, centroids, k=3):
    """
    >>> Function you need to write
    >>> Assign each data point to its nearest centroid based on the Euclidean distance
    >>> Update the cluster centroid to the mean of all the points assigned to that cluster
    """
    n_samples = np.shape(data)[0]
    n_features = np.shape(data)[1]
    clusters = [[] for _ in range(k)]
    labels = np.zeros((n_samples))

    for idx, val in enumerate(data):
        val_label = closest_centroid(val, centroids)
        clusters[val_label].append(val)
        labels[idx] = val_label
    centroids = np.zeros((k, n_features))
    for idx, cluster_val in enumerate(clusters):
        centroid = np.mean(cluster_val, axis=0)
        centroids[idx] = centroid
    return centroids, labels


def kmeans(data, k=3):
    """
    >>> Function you should not touch
    """
    # step 1:
    centroids = rand_center(data, k)
    converge = False
    iteration = 0
    while not converge:
        old_centroids = np.copy(centroids)
        # step 2 & 3
        centroids, label = update_centroids(data, old_centroids)
        # step 4
        converge = converged(old_centroids, centroids)
        iteration += 1
    print('number of iterations to converge: ', iteration)
    print(">>> final centroids")
    print(centroids)
    return centroids, label


def evaluation(predict, ground_truth):
    """
    >>> use F1 and NMI in scikit-learn for evaluation
    """
    f1 = f1_score(y_true=ground_truth, y_pred=predict, average='weighted')
    nmi = normalized_mutual_info_score(labels_true=ground_truth, labels_pred=predict)
    return f1, nmi


def gini(predict, ground_truth):
    """
    >>> use the ground truth to do majority vote to assign a flower type for each cluster
    >>> accordingly calculate the probability of missclassifiction and correct classification
    >>> finally, calculate gini using the calculated probabilities
    """
    labels = np.unique(ground_truth)
    num_labels = len(labels)
    cluster_p, cluster_g = [0 for _ in range(num_labels)], [0 for _ in range(num_labels)]
    gini_index = 0
    for i in labels:
        cluster_p[i], cluster_g[i] = np.array(predict[predict==i].shape[0]), np.array(ground_truth[ground_truth==i].shape[0])
        if cluster_p[i]<cluster_g[i]:
            correct_prob = cluster_p[i]/cluster_g[i]
            incorrect_prob = (cluster_g[i] - cluster_p[i])/cluster_g[i]
            gini_index += 1 - np.square(correct_prob) - np.square(incorrect_prob)
    gini_index /= num_labels
    print('Gini Index :', gini_index)
    return gini_index


def SSE(centroids, data):
    """
    >>> Calculate the sum of squared errors for each cluster
    """
    clusters = [[] for _ in centroids]
    num_centroids = len(centroids)
    for val in data:
        clusters[closest_centroid(val, centroids)].append(val)
    sse_each_cluster = [np.sum(np.sum(np.square(clusters[i] - centroids[i]), axis=1)) for i in range(num_centroids)]
    print('SSE_each_cluster: ', sse_each_cluster)
    return sse_each_cluster

