import random
import math
import sys


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


def main():
    args = sys.argv
    filename = args[1]
    k = int(args[2])
    iterations = int(args[3])
    k_means_clustering(filename, k, iterations)


main()
