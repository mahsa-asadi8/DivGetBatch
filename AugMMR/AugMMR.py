from Utils.Utils import similarity
from Utils.distance import min_max_distance


def CalculateBound(iTree,level,arity,q,lambda_score,S,simmap,indexMap,candNodes):
    lastItem = None
    if len(S) != 0:
        lastItem = S[-1]

    lbMMRList = []
    ubMMRList = []

    for nodeId in range(1,arity**level+1):
        node = iTree.levelMatrix[level][nodeId]
        if lastItem is not None:
            #########cluster to iTree distance##########
            recordId = iTree.documentMap[tuple(lastItem)][level]
            mincdis, maxcdis = iTree.dismatrix[level][recordId][node.id]

            # ######### item to iTree distance ############
            # recordId = indexMap[tuple(lastItem)]
            # mincdis, maxcdis = iTree.dismatrixitem[level][recordId][node.id]

            sim_current_max = 1 / (1 + mincdis)
            sim_current_min = 1 / (1 + maxcdis)

            if sim_current_max < simmap[(node.id,level)][1]:
                sim_current_max = simmap[(node.id,level)][1]
            if sim_current_min > simmap[(node.id,level)][0]:
                sim_current_min = simmap[(node.id,level)][0]
            simmap[(node.id, level)] = (sim_current_min,sim_current_max)

        mindis,maxdis = min_max_distance([q], node.elements)

        relmax = 1 / (1 + mindis)
        relmin = 1 / (1 + maxdis)

        lbMMR = 0
        ubMMR = 0
        if lastItem is None:
            lbMMR = lambda_score * relmin
            ubMMR = lambda_score * relmax
        else:
            lbMMR = lambda_score * relmin - (1 - lambda_score) * simmap[(node.id,level)][1]
            ubMMR = lambda_score * relmax - (1 - lambda_score) * simmap[(node.id,level)][0]

        if node in candNodes:
            lbMMRList.append(lbMMR)
            ubMMRList.append(ubMMR)
    return  (lbMMRList,ubMMRList)



def skipNodes(lbMMRList,ubMMRList,candNodes):
    maxofMin = max(lbMMRList)
    remainCluster = []
    i = 0

    for it in ubMMRList:
        if it >= maxofMin:
            if len(candNodes[i].children) == 0:
                remainCluster.append(candNodes[i])
            else:
                remainCluster.extend(candNodes[i].children)
        i = i + 1
    candNodes = remainCluster
    return candNodes


def DivGetBatch(iTree,L,arity,q,lambda_score,S,simmap,indexMap):
    candNodes = iTree.root.children

    for level in range(1,L+1):
        lbMMRList, ubMMRList = CalculateBound(iTree,level,arity,q,lambda_score,S,simmap,indexMap,candNodes) #calculateBound(iTree,C,indexMap,iTreeArray,l)
        candNodes = skipNodes(lbMMRList,ubMMRList,candNodes)
    candR = []
    for node in candNodes:
        candR.extend(node.elements)
    #print("number of returned items by DivGetBatch: ", len(candR))
    return candR



def AugMMR(iTree,L,arity,q,lambda_score,k,indexMap):

    S = []
    simmap = {}
    L = 1
    for level in range(1, L + 1):
        for nodeId in range(1, arity ** level + 1):
            node = iTree.levelMatrix[level][nodeId]
            simmap[(node.id, level)] = (1000000, -100000)

    for i in range (k):
        mmr = -100000000
        candR = DivGetBatch(iTree,L,arity,q,lambda_score,S,simmap,indexMap)

        for item in S:
            if item in candR:
                candR.remove(item)


        nextBest = None

        for d in candR:
            sim = 0
            for s in S:
                if similarity(d, s) == 0:
                    continue
                sim_current = similarity(d, s)
                if sim_current > sim:
                    sim = sim_current
                else:
                    continue

            rel = similarity(q, d)
            mmr_current = lambda_score * rel - (1 - lambda_score) * sim

            if mmr_current > mmr:
                mmr = mmr_current
                nextBest = d
            else:
                continue

        S.append(nextBest)
    return S




