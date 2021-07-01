# import guppy
# import inspect
from pyclustering.utils import euclidean_distance_square
import pandas as pd
from sklearn.preprocessing import normalize
from sklearn.datasets.samples_generator import make_blobs


infinity = float("inf")


def checkResult(augGmmResult, gmmResult):
    if sorted(augGmmResult) == sorted(gmmResult):
        print("array equal")
    else:
        print("array not equal")
        for i in gmmResult:
            if i not in augGmmResult:
                print(i, " not in Aug GMM")

        for i in augGmmResult:
            if i not in gmmResult:
                print(i, " not in GMM")
def div(i,j):
    return euclidean_distance_square(i, j)
def InitialTwoRecordsInGMM(cluster):
    maxdis = 0
    selectedNode1 = None
    selectedNode2 = None

    for node1 in cluster.root.children:
        for node2 in cluster.root.children:
            distmin , distmax = cluster.dismatrix[1][node1.id][node2.id]
            if maxdis < distmax:
                maxdis = distmax
                selectedNode1 = node1
                selectedNode2 = node2
    candR = selectedNode1.elements + selectedNode2.elements

    maxdis = 0

    for i in candR:
        for j in candR:
            if i != j:
                dis = euclidean_distance_square(i, j)
                if maxdis < dis:
                    maxdis = dis
                    record1 = i
                    record2 = j

    selectedNode1.elements.remove(record1)
    selectedNode2.elements.remove(record2)

    return  (record1,record2)

def similarity(r1,r2):
    return 1/(1+euclidean_distance_square(r1, r2))



def createDisMatrix(X):
    d = []
    i = 0
    for p1 in X:
        dd = []
        for p2 in X:
            dist = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
            dd.append(dist)
        d.append(dd)
    return d

def createSimMatrix(q, X):
    r = {}
    i = 0
    for p in X:
        d = euclidean_distance_square(q,p)
        r[i] = 1/(1+d)
        i = i + 1
    return r

def topkitems(sortedrecitems, k):
    return sortedrecitems[0:k]



def yelp_data(numberofSample):
    print("running yelp")
    dataset=pd.read_csv(r'Dataset\business\business.csv' , nrows=numberofSample)
    D = dataset.iloc[:, [6,7,8]].values
    normalized_D = normalize(D, axis=0, norm='l2')*1000
    X = normalized_D

    return X

def movieLens_data(numberofSample):
    print("running movieLens")
    dataset=pd.read_csv(r'Dataset\ratings\ratings.csv', nrows=numberofSample)
    D = dataset.iloc[:, [2, 3]].values
    normalized_D = normalize(D, axis=0, norm='l2')*1000000
    X = normalized_D

    return X

def makeBlobs_data(numberofSample):
    print("running makeBlobs")
    X, Y = make_blobs(n_samples=numberofSample, centers=10, cluster_std=0.010, random_state=0)
    return X


#
# def get_object_size(obj):
#     h = guppy.hpy()
#     callers_local_vars = inspect.currentframe().f_back.f_locals.items()
#
#     vname = "Index size"
#
#     # for var_name, var_val in callers_local_vars:
#     #     if var_val == obj:
#     #         vname = str(var_name)
#
#     size = str("{0:.8f} MB".format(float(h.iso(obj).domisize) / (1024*1024)))
#
#     return str("{}: {}".format(vname, size))
