
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
