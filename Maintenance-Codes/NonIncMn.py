from pyclustering.utils import euclidean_distance_square
from sklearn.datasets.samples_generator import make_blobs
from clustering_final import Clustering
from distance_final import min_distance, max_distance
import numpy as np
import timeit
import pandas as pd
from sklearn.preprocessing import normalize
import timeit
from numpy import asarray
from numpy import savetxt



numberofCluster = 50
numberofLevel = 1


##################################################################
df = pd.read_csv("makeblobs.csv", header= None)

X1 = df.iloc[:,:].values

#start = timeit.default_timer()

#dataset=pd.read_csv('ratings.csv' , nrows=50000)

#X = df.iloc[:,:].values
#X1 = dataset.iloc[:, [2,3]].values


#df = pd.read_csv("makeblobs-1M.csv", header= None)

#X1 = df.iloc[:,:].values



#dataset=pd.read_csv('business.csv' , nrows=50000)
#dataset=pd.read_csv('ratings.csv' , nrows=numberofSample)

#X1 = dataset.iloc[:, [2,3]].values
#X1 = dataset.iloc[:, [6,7,8]].values



cluster1 = Clustering(X1, numberofCluster, numberofLevel)
cluster1.buildTree(cluster1.root)
cluster1.createLevelMatrix(cluster1.root)
simMatrixNode1 = cluster1.createDistanceMatrix(numberofCluster, numberofLevel)

#stop = timeit.default_timer()

#print('Time: ', stop - start)



start = timeit.default_timer()

#df2 = pd.read_csv("makeblobs-100k.csv", header= None)
#S = df2.iloc[:, :].values

#df2 = pd.read_csv("random100kML.csv", header= None)
#S = df2.iloc[:, :].values

#1000
df2 = pd.read_csv("makeblobs-1000.csv", header= None)
S = df2.iloc[:, :].values

#df2 = pd.read_csv("makeblobs-100k.csv", header= None)
#S = df2.iloc[:, :].values


X2 = np.concatenate((X1, S))





cluster2 = Clustering(X2, numberofCluster, numberofLevel)
cluster2.buildTree(cluster2.root)
cluster2.createLevelMatrix(cluster2.root)
simMatrixNode2 = cluster2.createDistanceMatrix(numberofCluster, numberofLevel)

stop = timeit.default_timer()

print('Time: ', stop - start)

ScratchNodes = cluster2.createNodes(numberofCluster, numberofLevel)



minUpdates = 0
maxUpdates = 0


x = 0
y = 0
for i in range(1, numberofCluster+1):
    for j in range(1,numberofCluster+1):
        if i < j:
            if(abs((simMatrixNode1[1][i][j][0] - simMatrixNode2[1][i][j][0])) > 0.001):
                minUpdates = minUpdates +1
                x = i
                y = j
                #print("x", x)
                #print("y", y)
            if (abs((simMatrixNode1[1][i][j][1] - simMatrixNode2[1][i][j][1])) > 0.001):
                maxUpdates = maxUpdates +1
                #x = i
                #y = j
                #print("x", x)
                #print("y", y)



print("min:", minUpdates)
print("max:",maxUpdates)



totalUpdates = minUpdates + maxUpdates

print("total updates:",totalUpdates)








