from pyclustering.utils import euclidean_distance_square
from sklearn.datasets.samples_generator import make_blobs

import heapq
import timeit
from  Utils.Utils import topkitems,div
from  Utils.Utils import  infinity



def Divcont(X, retlistkeys, i):
    diret = 0
    for j in retlistkeys:
        diret = diret + div(X[i], X[j])
    return diret

def CalculateBoundUpdate(cluster,l,minmaxDitc,insid,delid,id):
    maxdf, mindf = minmaxDitc[id]
    minin,maxin = cluster.dismatrixitem[l][insid][id]
    minddel,maxdel  = cluster.dismatrixitem[l][delid][id]
    maxdf = maxdf + maxin - maxdel
    mindf = mindf + minin - minddel
    minmaxDitc[id] = (maxdf, mindf)
    return (maxdf, mindf)



def CalculateBound(cluster,l,retlistkeys,id):
    maxdf, mindf = (0.0, 0.0)
    for j in retlistkeys:
        mind,maxd = cluster.dismatrixitem[l][j][id]
        mindf = mindf + mind
        maxdf = maxdf + maxd
    return (maxdf, mindf)


def DivGetBatch(cluster,minmaxDitc, i, retlistkeys,itdel,itin):
    skipElements = {-1}
    if itin is None or itdel is None:
        for node in cluster.root.children:
            maxdis, mindis = CalculateBound(cluster, 1, retlistkeys, node.id)
            minmaxDitc[node.id] = (maxdis,mindis)
            if maxdis < i[0]:
                skipElements.add(node.id)
    else:
        for node in cluster.root.children:
            maxdis, mindis = CalculateBoundUpdate(cluster, 1,minmaxDitc,itin,itdel, node.id)
            if maxdis < i[0]:
                # print("prune")
                skipElements.add(node.id)
    return skipElements


def AugSWAP(X,cluster,recitems,k,ub):
    swapnumber = 0
    skip = 0
    DivGetBatchTime = 0.0
    SortedRecItems = sorted(recitems.items(), key=lambda x: x[1], reverse=True)
    retlist = topkitems(SortedRecItems, k)
    pos = k


    retlistkeys, retlistvalues = zip(*retlist)
    retlistkeys = list(retlistkeys)
    diretlist = []
    diretlistMap = {}
    for i in retlistkeys:
        diretval = Divcont(X, retlistkeys, i)
        # print("item ", i, " di = ", diretval )
        t = (diretval, i)
        diretlist.append(t)
        diretlistMap[i] = diretval

    M = []
    for item in diretlist:
        heapq.heappush(M, item)

    # print(M)

    i = heapq.heappop(M)
    #print(i)

    recalSkipList = True
    skipList = {}
    minmaxdic = {}
    newitem = None
    while ((recitems[i[1]] - SortedRecItems[pos][1]) < ub):
        rlist = [item for item in retlist if item[0] == i[1]]
        retlist.remove(rlist[0])
        retlistkeys, retlistvalues = zip(*retlist)
        retlistkeys = list(retlistkeys)


        if recalSkipList:
            start = timeit.default_timer()
            if newitem is None:
                DivGetBatch(cluster, minmaxdic, i, retlistkeys, None, None)

            else:
                skipList = DivGetBatch(cluster,minmaxdic,i,retlistkeys,i[1],newitem[0])

            stop = timeit.default_timer()
            DivGetBatchTime = DivGetBatchTime + stop -start



        if cluster.documentMap[tuple(X[SortedRecItems[pos][0]])][1] not in  skipList:
            dsortedrec = Divcont(X, retlistkeys, SortedRecItems[pos][0])
        else:
            skip = skip + 1
            pos = pos+1
            recalSkipList = False
            retlist.append(rlist[0])
            if (pos == len(SortedRecItems)):
                break
            continue

        if (i[0] < dsortedrec):
            recalSkipList = True
            swapnumber = swapnumber + 1
            retlist.append(SortedRecItems[pos])
            newitem = SortedRecItems[pos]
            retlistkeys.append(SortedRecItems[pos][0])

            minval = infinity
            candItem = None
            for j in retlistkeys:
                diretval = Divcont(X, retlistkeys, j)
                t = (diretval, j)
                if minval > diretval:
                    minval = diretval
                    candItem = t

            i = candItem

        else:
            recalSkipList = False
            retlist.append(rlist[0])
        pos = pos + 1
        if (pos == len(SortedRecItems)):
            break
    print("awg swap number ",swapnumber)
    print("skip ",skip)
    print("DivGetBatch Time = ",DivGetBatchTime)
    return retlist





