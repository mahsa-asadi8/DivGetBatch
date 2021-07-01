import gurobipy as gp
from gurobipy import *
from gurobipy import tuplelist
import gurobipy as gp
from gurobipy import *
from gurobipy import tuplelist
import itertools
import random
import math
import numpy
from distance_final import min_distance, max_distance,min_max_distance, min_disElement, max_disElement
from clustering_final import Clustering
import random
import timeit
from sklearn.datasets.samples_generator import make_blobs
import pandas as pd
from numpy import asarray
from numpy import savetxt

def euclideanDist(x, y):
    distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))
    return distance


numberofCluster = 50

numberofLevel = 1




center_box = (1, 10000)



#########################################################
# read dataset



df = pd.read_csv("makeblobs.csv", header= None)

X = df.iloc[:,:].values



############ read new data to insert


df2 = pd.read_csv("makeblobs-1000.csv", header= None)
S = df2.iloc[:, :].values





###############################################



cluster = Clustering(X, numberofCluster, numberofLevel)
cluster.buildTree(cluster.root)
cluster.createLevelMatrix(cluster.root)
simMatrixNode = cluster.createDistanceMatrix(numberofCluster, numberofLevel)
nodescentroids = cluster.createNodesCentroids(numberofCluster, numberofLevel)



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
N =len(S)



w, h = C, N
mindislist = [[0 for a in range(w)] for b in range(h)]


def mindis(S, Nodes):
    for item in range(N):
        for key in Nodes.keys():
            min = 1000000000000000000000
            for value in Nodes[key]:
                d = euclideanDist(S[item], value)**2
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
                d = euclideanDist(S[item], value)**2
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

for i in range(N):
    for j in range(C):
        for p in range(C):
            if (j != p):
                minT[i][j][p] = cmp(minSimMatrix[j][p], mindislist[i][p])





maxT = [[[0 for x3 in range(w2)] for y3 in range(l2)] for u3 in range(r2)]

for i in range(N):
    for j in range(C):
        for p in range(C):
            if (j != p):
                maxT[i][j][p] = cmp(maxdislist[i][p], maxSimMatrix[j][p])





################################################

# Declare and initialize model
m = gp.Model('mymodel')

Y = m.addVars(N,C,vtype=GRB.BINARY, name="Y")

z1 = m.addVars(C,C,vtype=GRB.CONTINUOUS,name='z1')
x1 = m.addVars(C,C,vtype=GRB.BINARY,name='x1')

z2 = m.addVars(C,C,vtype=GRB.CONTINUOUS,name='z2')
x2 = m.addVars(C,C,vtype=GRB.BINARY,name='x2')

for i in range(N):
    m.addConstr((gp.quicksum(Y[i,j] for j in range(C))) == 1)

for j in range(C):
    for k in range(C):
            m.addConstr(gp.quicksum((Y[i, j] * minT[i][j][k] + Y[i, k] * minT[i][k][j]) for i in range(N)) == z1[j, k])

for j in range(C):
    for k in range(C):
            m.addConstr(gp.quicksum((Y[i, j] * maxT[i][j][k] + Y[i, k] * maxT[i][k][j]) for i in range(N)) == z2[j, k])

for i in range(C):
    for j in range(C):
        m.addGenConstrIndicator(x1[i, j], 0, z1[i, j], GRB.LESS_EQUAL, 0.1)
        m.addGenConstrIndicator(x1[i, j], 1, z1[i, j], GRB.GREATER_EQUAL, 0.1)

for i in range(C):
    for j in range(C):
        m.addGenConstrIndicator(x2[i, j], 0, z2[i, j], GRB.LESS_EQUAL, 0.1)
        m.addGenConstrIndicator(x2[i, j], 1, z2[i, j], GRB.GREATER_EQUAL, 0.1)



ex = gp.quicksum((x1[i,j]+x2[i,j]) for i in range(C) for j in range(C) if i < j)


# Set objective
m.setObjective(ex, GRB.MINIMIZE)
m.optimize()

#

for v in m.getVars():
    print(v.varName, v.x)

#
Y2 = [[0 for x3 in range(C)] for y3 in range(N)]

for v in m.getVars():
    if v.varName.__contains__('Y'):

        first = v.varName.find(',')
        end = v.varName.find(']')

        i = v.varName[2:first]
        j = v.varName[first+1:end]
        i2 = int(i)
        j2 = int(j)
        Y2[i2][j2] = v.x




NewItems_Nodes = {}
for i in range(N):
    for j in range(C):
        if Y2[i][j] == 1:
            NewItems_Nodes[j] = S[i]





print('Total update:', m.objVal)



FinalNodes = {}
for key in set().union(Nodes, NewItems_Nodes):
    if key in Nodes: FinalNodes.setdefault(key, []).extend(Nodes[key])
    if key in NewItems_Nodes: FinalNodes.setdefault(key, []).extend(NewItems_Nodes[key])





stop = timeit.default_timer()

print('Time for IP: ', stop - start)

