from Utils.Utils import div

def CalculateBound(iTree,level,arity,S,minMap,indexMap,candNodes):
    lastItem = S[-1]
    lBGMM = []
    uBGMM = []

    for nodeId in range(1,arity**level+1):
        node = iTree.levelMatrix[level][nodeId]

        #########cluster to iTree distance##########
        nid = iTree.documentMap[tuple(lastItem)][level]
        distmin, distmax = iTree.dismatrix[level][nid][node.id]

        # ######### item to iTree distance ############
        # recordId = indexMap[tuple(lastItem)]
        # distmin, distmax = iTree.dismatrixitem[level][recordId][node.id]

        minmax = minMap[(node.id,level)][0]
        minmin = minMap[(node.id,level)][1]
        if minmax > distmax:
            minmax = distmax

        if minmin > distmin:
            minmin = distmin

        minMap[(node.id,level)] = (minmax, minmin)
        if node in candNodes:
            lBGMM.append(minmin)
            uBGMM.append(minmax)
    return  (lBGMM,uBGMM)



def skipNodes(lBGMM,uBGMM,candNodes):
    maxofMin = max(lBGMM)
    remainCluster = []
    i = 0

    for it in uBGMM:
        if it >= maxofMin:
            if len(candNodes[i].children) == 0:
                remainCluster.append(candNodes[i])
            else:
                remainCluster.extend(candNodes[i].children)
        i = i + 1
    candNodes = remainCluster
    return candNodes


def DivGetBatch(iTree, L,arity,S, minMap, indexMap):
    candNodes = iTree.root.children
    lastItem = S[-1]
    for level in range(1,L+1):
        lBGMM,uBGMM = CalculateBound(iTree,level,arity,S,minMap,indexMap,candNodes) #calculateBound(iTree,C,indexMap,iTreeArray,l)
        candNodes = skipNodes(lBGMM,uBGMM,candNodes)
    candR = []
    for node in candNodes:
        candR.extend(node.elements)
    #print("number of returned items by DivGetBatch: ", len(candR))
    return candR


def AugGMM(iTree,L,arity, R, K, indexMap ,initRecords):

    S = []
    S.extend(list(initRecords))
    R.remove(initRecords[0])
    R.remove(initRecords[1])


    minMap = {}

    for level in range(1, L+1):
        for nodeId in range(1,arity**level+1):
            node = iTree.levelMatrix[level][nodeId]
            ##########record to node distance##########

            # recordId = indexMap[tuple(initRecords[0])]
            # distmin, distmax = iTree.dismatrixitem[level][recordId][node.id]
            # minMap[(node.id, level)] = (distmax, distmin)

            ##########node to node distance##########

            id = iTree.documentMap[tuple(initRecords[0])][level]
            distmin, distmax = iTree.dismatrix[level][id][node.id]
            minMap[(node.id, level)] = (distmax,distmin)


    for k in range(K - 2):
        candR = DivGetBatch(iTree,L,arity, S, minMap, indexMap)
        minArray = []
        maxval = 0
        maxitem = None
        for i in candR:
            min = float("inf")
            for j in S:
                dist = div(i, j)
                if min >= dist:
                    min = dist
                if min <= maxval:
                    break
            if min >= maxval:
                maxval = min
                maxitem = i
            minArray.append(min)

        S.append(maxitem)
        R.remove(maxitem)
    return S


