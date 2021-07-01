from sklearn.cluster import KMeans
from Node import Node
from distance_final2 import min_distance, max_distance,min_max_distance
import timeit
from sklearn.cluster import MiniBatchKMeans, KMeans
import numpy
import operator



class Clustering:
    documentMap = {}
    centroids = {}


    def __init__(self, data, numberofCluster, numberofLevel):
        self.root = Node(None, 0, 1)
        self.root.elements = data
        self.root.numberOfElement = len(data)
        self.numberOfCluster = numberofCluster
        self.numberOfLevels= numberofLevel
        self.dismatrix = None

        for i in range(len(data)):
            d = data[i]
            self.documentMap[tuple(d)] = numpy.zeros(self.numberOfLevels+1, dtype=int)


        self.levelMatrix = numpy.empty(
            shape=(self.numberOfLevels + 1, self.numberOfCluster ** self.numberOfLevels + 1), dtype=Node)

    def buildTree(self,parent):
        #print(parent.elements)
        if parent.level == self.numberOfLevels:
            return




        start = timeit.default_timer()
        kmeans = KMeans(n_clusters=self.numberOfCluster, init='k-means++', max_iter=300, n_init=10, random_state=0)


        pred_y = kmeans.fit_predict(parent.elements)

        #centers = kmeans.cluster_centers_
        #print(centers)

        #print(len(centers))
        #for i in range(len(centers)):
        #    self.centroids[i] = centers[i]

        #print(self.centroids)

        stop = timeit.default_timer()

        #print('Time for kmeans: ', stop - start)



        for i in range(len(parent.elements)):
            self.documentMap[tuple(parent.elements[i])][parent.level] = parent.id

        parent.children = []
        for i in range(0,self.numberOfCluster):
            id =parent.id * self.numberOfCluster - self.numberOfCluster + 1  + i
            new_node = Node(parent,parent.level+1,id)
            new_node.elements = []
            new_node.numberOfChildren = 0
            parent.setChildren(new_node)

        j = -1
        pdict = {}
        v = 0
        for i in pred_y:
            if i in pdict:
                i = pdict.get(i)
            else:
                pdict[i] = v
                i = v
                v = v + 1
            j = j + 1
            c = parent.children[i]
            c.insertElement(parent.elements[j])
            self.documentMap[tuple(parent.elements[j])][c.level] = c.id

        #print("elements = ", parent.children[1].elements,"\n")
        for i in range (0,parent.numberOfChildren):
            self.buildTree(parent.children[i])






    def createLevelMatrix(self, currentNode):
        nodes = currentNode.children

        if currentNode.numberOfChildren == 0:
            return
        for node in currentNode.children:
            self.levelMatrix[currentNode.level + 1][node.id] = node
            self.createLevelMatrix(node)


    def createNodesCentroids(self, numberOfCluster, numberOfLevels):
        nodes = {}

        for i in range(1, numberOfCluster ** numberOfLevels + 1):

            nodes[self.levelMatrix[numberOfLevels][i].id] = (self.levelMatrix[numberOfLevels][i].elements)
        #print(nodes)
        for key in nodes.keys():
            sum = (0,0)
            for items in nodes[key]:
                sum = tuple(map(operator.add, sum, items))
                centers = [x / len(nodes[key]) for x in sum]

            #print(centers)
            self.centroids[key] = centers
        #print("centroids:", self.centroids)
        return self.centroids

            #res = sum / len(value)
            #print(res)


    def createNodes(self, numberOfCluster, numberOfLevels):
        self.nodes = {}

        for i in range(1, numberOfCluster ** numberOfLevels + 1):
            self.nodes[self.levelMatrix[numberOfLevels][i].id] = (self.levelMatrix[numberOfLevels][i].elements)

        #print(self.nodes)
        return self.nodes



    #dismatrix = None
    def createDistanceMatrix(self, numberOfCluster, numberOfLevels):
        #global dismatrix
    # print(max_matrix)
        self.dismatrix = numpy.empty(
        shape=(self.numberOfLevels + 1, self.numberOfCluster ** self.numberOfLevels + 1,
               self.numberOfCluster ** self.numberOfLevels + 1),
        dtype=tuple)
        for l in range(1,numberOfLevels + 1):
            for i in range(1,numberOfCluster**l + 1):
                for j in range(1,numberOfCluster**l + 1):
                    self.dismatrix[l, i, j] = min_max_distance(self.levelMatrix[l][i].elements, self.levelMatrix[l][j].elements)

        #print("dismatrixNode:", self.dismatrix)
        return self.dismatrix

    dismatrixitem = None



    def createDistanceMatrixforelements(self, numberOfCluster, numberOfLevels):
        global  dismatrixitem
        # print(max_matrix)
        self.dismatrixitem = numpy.empty(
            shape=(numberOfLevels + 1,  len(self.root.elements), numberOfCluster ** numberOfLevels + 1),
            dtype=tuple)
        for l in range(1, numberOfLevels + 1):
            for i in range(0, len(self.root.elements)):
                for j in range(1, numberOfCluster ** l + 1):
                    self.dismatrixitem[l, i , self.levelMatrix[l][j].id] = min_max_distance([self.root.elements[i]], self.levelMatrix[l][j].elements)


        # print(self.dismatrix)

        return self.dismatrixitem

