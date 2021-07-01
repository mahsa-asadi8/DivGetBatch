from pyclustering.utils import euclidean_distance_square
import numpy as np
import timeit
import math
import crab as cr






def distance_euclidean(x, y):

    m = len(x)
    i = 0
    d = 0


    while(i < m):
        tmp = x[i] - y[i]
        i = i + 1
        d += tmp * tmp
    return d


x = [6.71690023488524, 8.288551839797037]

y = [-9.221730408948588, -7.624742969810503]

distance_euclidean(x,y)

def min_distance(cluster1, cluster2):
    mindis = float('inf')
    for i in cluster1:
        for j in cluster2:
            dis = distance_euclidean(i, j)
            # if dis == 0:
            #     dis = 10000000
            if mindis > dis:
                mindis = dis
                item = (i, j)
    return mindis


def max_distance(cluster1, cluster2):
    maxdis = -1
    item = None
    for i in cluster1:
        for j in cluster2:
            dis = distance_euclidean(i, j)
            if maxdis < dis:
                maxdis = dis
                item = (i,j)
    return maxdis


import timeit
import scipy.spatial.distance

def min_max_distance(cluster1, cluster2):
    #start = timeit.default_timer()
    contributingElems = []
    Z = scipy.spatial.distance.cdist(cluster1, cluster2, 'euclidean')
    #print(Z.min()**2,Z.max()**2)
    #stop = timeit.default_timer()
    #print('Time for mmr: ', stop - start)
    min = 1000000000000000000000
    max = -1
    minindexi = 0
    minindexj = 0
    maxindexi= 0
    maxindexj = 0
    for i in range(0,len(cluster1)):
        for j in range(0,len(cluster2)):
            if i != j:
                dis = Z[i][j]
                if min > dis:
                    min = dis
                    minindexi = i
                    minindexj = j

                if max < dis:
                    max = dis
                    maxindexi = i
                    maxindexj = j


    contributingElems.append(cluster1[minindexi])
    contributingElems.append(cluster2[minindexj])
    contributingElems.append(cluster1[maxindexi])
    contributingElems.append(cluster2[maxindexj])



    return min**2,max**2, contributingElems


    mindis = float('inf')
    maxdis = -1
    for i in cluster1:
        for j in cluster2:
            dis = distance_euclidean(i, j)
            if mindis > dis:
                mindis = dis
                item = (i, j)
            if maxdis < dis:
                maxdis = dis
    return mindis,maxdis

# from sklearn.datasets.samples_generator import make_blobs
#
# X1,Y = make_blobs(n_samples=1000, centers=10, cluster_std=0.60, random_state=0)
# X2,Y = make_blobs(n_samples=1000, centers=10, cluster_std=0.60, random_state=1)
#
# min_max_distance(X1.tolist(),X2.tolist())



def max_disElement(element, cluster):
    maxdis = -1
    item = None
    for j in cluster:
        dis = distance_euclidean(element, j)
        if maxdis < dis:
            maxdis = dis
            item = (element,j)
    return maxdis



def min_disElement(element, cluster):
    mindis = float('inf')

    for j in cluster:
        dis = distance_euclidean(element, j)
            # if dis == 0:
            #     dis = 10000000
        if mindis > dis:
            mindis = dis
            item = (element, j)
    return mindis




def min_distance2(cluster1, cluster2):
    mindis = float('inf')
    for i in cluster1:
        for j in cluster2:
            dis = (i[0]- j[0])**2 + (i[1] - j[1])**2
            # if dis == 0:
            #     dis = 10000000
            if mindis > dis:
                mindis = dis
    return mindis


def max_distance2(cluster1, cluster2):
    maxdis = -1
    item = None
    for i in cluster1:
        for j in cluster2:
            dis = (i[0]- j[0])**2 + (i[1] - j[1])**2
            if maxdis < dis:
                maxdis = dis
                item = (i,j)
    return maxdis

