import itertools
import random
import math
import numpy
from distance_final import min_distance, max_distance,min_max_distance
from clustering_final import Clustering
import random
import timeit
import pandas as pd




df = pd.read_csv("makeblobs.csv", header= None)

X = df.iloc[:,:].values

############ read new data to insert



df2 = pd.read_csv("makeblobs-1000.csv", header= None)
S = df2.iloc[:, :].values




numberofCluster = 50

numberofLevel = 1

cluster = Clustering(X, numberofCluster, numberofLevel)
cluster.buildTree(cluster.root)
cluster.createLevelMatrix(cluster.root)
simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)



start = timeit.default_timer()

Nodes = cluster.createNodes(numberofCluster, numberofLevel)


ww, hh = numberofCluster, numberofCluster
minSimMatrix = [[0 for x in range(ww)] for y in range(hh)]
maxSimMatrix = [[0 for x in range(ww)] for y in range(hh)]


for i in range (numberofCluster):
    for j in range(numberofCluster):
        minSimMatrix[i][j] = simMatrixNode[1][i+1][j+1][0]
        maxSimMatrix[i][j] = simMatrixNode[1][i+1][j+1][1]





C = numberofCluster
N = len(S)


w, h = C, N
mindislist = [[0 for a in range(w)] for b in range(h)]


def mindis(S, Nodes):
    for item in range(N):
        for key in Nodes.keys():
            min = 1000000000000000000000
            for value in Nodes[key]:
                d = (S[item][0]- value[0])**2 + (S[item][1] - value[1])**2
                #d = euclideanDist(S[item], value)**2
                if min > d:
                    min = d
            mindislist[item][int(key)-1] = min

    return mindislist


mindis(S, Nodes)

maxdislist = [[0 for c in range(w)] for d in range(h)]


def maxdis(S, Nodes):
    for item in range(N):
        for key in Nodes.keys():
            max = -1
            for value in Nodes[key]:
                d = (S[item][0]- value[0])**2 + (S[item][1] - value[1])**2
                #d = euclideanDist(S[item], value)**2
                if max < d:
                    max = d
            maxdislist[item][int(key-1)] = max

    return maxdislist


maxdis(S, Nodes)



def cmp(a, b):
    x = 1
    y = 0
    if a > b:
        return x
    if a <= b:
        return y


w2, l2, r2 = C, C, N

minT = [[[0 for x2 in range(w2)] for y2 in range(l2)] for u2 in range(r2)]
maxT = [[[0 for x3 in range(w2)] for y3 in range(l2)] for u3 in range(r2)]
total = [[[0 for x3 in range(w2)] for y3 in range(l2)] for u3 in range(r2)]

for i in range(N):
    for j in range(C):
        for p in range(C):
            if (j != p):
                minT[i][j][p] = cmp(minSimMatrix[j][p], mindislist[i][p])
                maxT[i][j][p] = cmp(maxdislist[i][p], maxSimMatrix[j][p])
                total[i][j][p] = minT[i][j][p] + maxT[i][j][p]



final = {}
updates = {}
for i in range(N):
    min = 10000000000000
    for j in range(C):
        sumval = sum(total[i][j][:])
        if min > sumval:
            min = sumval
            jid = j
    final[i] = jid
    updates[i] = min

print(final)
print(updates)

totalupdates = 0
for key,value in updates.items():
    totalupdates = value + totalupdates

print("total updates:", totalupdates)



stop = timeit.default_timer()

print('Time: ', stop - start)


