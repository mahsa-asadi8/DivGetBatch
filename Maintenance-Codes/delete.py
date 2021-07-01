import itertools
import random
import math
import numpy
from distance_final2 import min_distance, max_distance,min_max_distance
from clustering_final import Clustering
import random
import timeit
import pandas as pd
import numpy as np
from numpy import asarray
from numpy import savetxt
import scipy.spatial.distance




df = pd.read_csv("randomData10k.csv", header= None)


X = df.iloc[:,:].values




numberofCluster =10
numberofLevel = 1


# delete items from random data

df2 = pd.read_csv("delrandom-10.csv", header= None)

S = df2.iloc[:, :].values



cluster = Clustering(X, numberofCluster, numberofLevel)
cluster.buildTree(cluster.root)

Sids = {}

for i in S:
    id = cluster.documentMap[tuple(i)][numberofLevel]
    Sids[tuple(i)] = id

cluster.createLevelMatrix(cluster.root)
simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)
Nodes = cluster.createNodes(numberofCluster, numberofLevel)




print("simMatrixNode created")


start = timeit.default_timer()





keys = []
for key, l in Nodes.items():
    for elements in l:
        for item in S:
            if np.array_equal(item,elements):

                index = np.where(l == item)[0][0]

                l = np.delete(l,index,0)
    Nodes[key] = l



print("item deleted")


# update simmatrixnode

for item in S:
    j = Sids[tuple(item)]
    for p in range(1 , numberofCluster+1):
        if j != p:
            for elem in simMatrixNode[1][j][p][2]:
                if item[0] == elem[0]  and item[1] == elem[1]:

                    simMatrixNode[1, j, p] = min_max_distance(Nodes[j], Nodes[p])



print("simMatrixNode updated")




stop = timeit.default_timer()

print('Time: ', stop - start)

