import copy
import csv
import math
import random
import collections
import matplotlib.pyplot as plt


def euclideanDistance(p1, p2):
    d1 = p2[1] - p1[1]
    d2 = p2[2] - p1[2]
    return math.sqrt(d1*d1 + d2*d2)


def pointsMean(points):
    sum_x = 0
    sum_y = 0
    for p in points:
        sum_x += p[1]
        sum_y += p[2]
    return 'mean', sum_x/len(points), sum_y/len(points)


# The K-means function
def kmeans(points, k, no_of_iterations):

    # Randomly choose K centroids
    centroids = []
    while len(centroids) < k:
        randPoint = random.choice(points)
        if randPoint not in centroids:
            centroids.append(randPoint)

    clusters = []
    for i in range(k):
        clusters.append([])

    prev_clusters = copy.deepcopy(clusters)

    for it in range(no_of_iterations):
        if it != 0:
            # Recalculate the center of each cluster (find the means / centroids again)
            centroids.clear()
            for cluster in clusters:
                new_centroid = pointsMean(cluster)
                centroids.append(new_centroid)
                cluster.clear()

        # For each point, find the distances to all centroids, then assign it to the list of the nearest one
        for p in points:
            nearestCentroidIdx = 0
            mini = euclideanDistance(p, centroids[0])
            for i in range(1,k):   # find the index of the nearest centroid
                d = euclideanDistance(p, centroids[i])
                if d < mini:
                    mini = d
                    nearestCentroidIdx = i
            clusters[nearestCentroidIdx].append(p)

        # check if the clusters changed
        nothingChanged = True
        for i in range(len(clusters)):
            if collections.Counter(prev_clusters[i]) != collections.Counter(clusters[i]):
                nothingChanged = False

        if nothingChanged:  # exit if the clusters are the same
            print("Finished @ iteration",it)
            break
        prev_clusters = copy.deepcopy(clusters)

    return clusters, centroids


def readPoints():
    _points = []
    with open('dataset.csv') as file:
        rows = csv.reader(file)
        first = True
        for row in rows:
            if not first:
                point = (row[0], float(row[1]), float(row[2]))
                # print(point)
                _points.append(point)
            first = False
    return _points


def computeCorrectClassified(totalPoints, clusters):
    for cluster in clusters:
        label = cluster[0][0]
        for point in cluster:
            if point[0] != label:
                totalPoints -= 1
    return totalPoints


def computeScore(cluster,allPoints):
    label = cluster[0][0]

    # get correctly guessed points in this cluster
    correctly_guessed = len(list(filter(lambda point: point[0] == label, cluster)))
    # get total no. of points with this label
    totalPoints = len(list(filter(lambda point: point[0] == label, allPoints)))

    P = correctly_guessed/totalPoints  # the probability that a positive classified example is relevant
    print("\n" + label)
    print("Precision is", P)

    R = correctly_guessed/len(cluster)  # the probability that a positive example is correct classified
    print("Recall is", R)

    S = 2*P*R/(P+R)
    print("Score is", S)


def plot(clusters, clusters_centroids):
    colors = {"A": "red","B": "green","C": "blue","D": "yellow"}
    print("The points are being plotted...")
    k = len(clusters)
    for i in range(k):
        label = clusters[i][0][0]
        for point in clusters[i]:
            plt.scatter(point[1], point[2], c=colors[label], marker='.')
        plt.scatter(clusters_centroids[i][1], clusters_centroids[i][2], c="black", marker='x')
    plt.plot()
    # plt.savefig("kmeans-plot.png")
    plt.show()


if __name__ == "__main__":
    # Read the data
    thePoints = readPoints()
    noOfPoints = len(thePoints)

    K = 4
    # noOfIterations = int(input("No. of iterations: "))
    noOfIterations = 420

    # Cluster the data
    print("\nClustering is running, please wait ...")
    resulted_clusters, centroids = kmeans(thePoints, K, noOfIterations)

    for cl in resulted_clusters:
        print(cl)

    # Print the statistics
    cc = computeCorrectClassified(noOfPoints, resulted_clusters)
    print("\nAccuracy is",cc,'/',noOfPoints,'=',cc/noOfPoints)

    for cl in resulted_clusters:
        computeScore(cl,thePoints)

    plot(resulted_clusters, centroids)


