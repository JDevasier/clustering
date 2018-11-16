import random
import math


def read_file(fname):
    lines = []
    with open(fname) as f:
        for line in f:
            lines.append(list(map(float, line.split())))

    return lines


def mean_of_set(s):
    n = len(s)
    d = len(s[0])
    mean = [0] * d
    for i in range(d):
        col_mean = 0
        for x in s:
            col_mean += x[i]
        mean[i] = col_mean / n
    return mean


def compute_means(S):
    means = []
    for s in S:
        means.append(mean_of_set(s))
    return means


def distance(a, b):
    d = 0
    for i in range(len(a)):
        d += (a[i] - b[i])**2
    return math.sqrt(d)


def compute_new_clusters(X, means, k):
    S = [[] for _ in range(k)]

    for x in X:
        closest = (-1, math.inf)
        # Get closest mean
        for m in range(len(means)):
            dist = distance(means[m], x)
            if dist < closest[1]:
                closest = (m, dist)

        S[closest[0]].append(x)

    return S


def error(S, means):
    err = 0
    k = len(S)
    for i in range(k):
        for x in S[i]:
            err += distance(x, means[i])
    return err


def k_means_clustering(data_file, k, iterations):
    X = [x[:-1] for x in read_file(data_file)]
    S = [[] for _ in range(k)]
    means = []

    # Randomly apply x to a set
    for x in X:
        r = random.randrange(0, k)
        S[r].append(x)

    means = compute_means(S)
    err = error(S, means)
    print("After initialization: error = {:.4f}".format(err))

    prev_err = err
    for i in range(iterations):
        S = compute_new_clusters(X, means, k)
        means = compute_means(S)
        err = error(S, means)
        print("After iteration {:d}: error = {:.4f}".format(
            i, err))

        # Arbitrary value of 0.0001 to determine if it converged
        if abs(err - prev_err) < 0.0001:
            print("Algorithm has converged")
            break

        prev_err = err


def medoid_of_set(s):
    amin = (None, math.inf)
    for _s in s:
        xsum = 0

        for x in s:
            xsum += distance(_s, x)

        if xsum < amin[1]:
            amin = (_s, xsum)

    return amin[0]


def compute_medoids(S):
    medoids = []
    for s in S:
        medoids.append(medoid_of_set(s))
    return medoids


def compute_new_medoid_clusters(X, medoids, k):
    S = [[] for _ in range(k)]

    for x in X:
        closest = (-1, math.inf)
        # Get closest mean
        for m in range(len(medoids)):
            dist = distance(medoids[m], x)
            if dist < closest[1]:
                closest = (m, dist)

        S[closest[0]].append(x)

    return S


def k_medoid_clustering(data_file, k, iterations):
    X = [x[:-1] for x in read_file(data_file)]
    S = [[] for _ in range(k)]
    medoids = []

    # Randomly apply x to a set
    for x in X:
        r = random.randrange(0, k)
        S[r].append(x)

    medoids = compute_medoids(S)
    err = error(S, medoids)
    print("After initialization: error = {:.4f}".format(err))

    last_err = err
    for i in range(iterations):
        S = compute_new_medoid_clusters(X, medoids, k)
        medoids = compute_medoids(S)
        err = error(S, medoids)
        print("After iteration {:d}: error = {:.4f}".format(
            i, err))

        if abs(err - last_err) < 0.0001:
            print("Algorithm has coverged")
            break
        last_err = err


#k_means_clustering("yeast_test.txt", 3, 50)
#k_medoid_clustering("yeast_test.txt", 3, 50)
