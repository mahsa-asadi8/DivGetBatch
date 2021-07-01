
import heapq
from  Utils.Utils import topkitems,div


def Divcont(X, retlistkeys, i):
    diret = 0
    for j in retlistkeys:
        diret = diret + div(X[i], X[j])
    return diret

def SWAP(X,recitems,k,ub):
    swapnumber = 0
    SortedRecItems = sorted(recitems.items(), key=lambda x: x[1], reverse=True)
    retlist = topkitems(SortedRecItems, k)
    pos = k

    retlistkeys, retlistvalues = zip(*retlist)
    retlistkeys = list(retlistkeys)
    diretlist = []
    diretlistMap = {}
    for i in retlistkeys:
        diretval = Divcont(X, retlistkeys, i)
        t = (diretval, i)
        diretlist.append(t)
        diretlistMap[i] = diretval

    M = []
    for item in diretlist:
        heapq.heappush(M, item)

    i = heapq.heappop(M)

    while ((recitems[i[1]] - SortedRecItems[pos][1]) < ub):
        rlist = [item for item in retlist if item[0] == i[1]]
        retlist.remove(rlist[0])
        retlistkeys, retlistvalues = zip(*retlist)
        retlistkeys = list(retlistkeys)
        dsortedrec = Divcont(X, retlistkeys, SortedRecItems[pos][0])
        if (i[0] < dsortedrec):
            swapnumber = swapnumber + 1
            retlist.append(SortedRecItems[pos])
            retlistkeys.append(SortedRecItems[pos][0])
            heapq.heappush(M, (dsortedrec, SortedRecItems[pos][0]))
            # update d values

            diretlist = []
            diretlistMap = {}
            M = []
            for j in retlistkeys:
                diretval = Divcont(X, retlistkeys, j)
                # print("item ", i, " di = ", diretval)
                t = (diretval, j)
                diretlist.append(t)
                diretlistMap[j] = diretval
                heapq.heappush(M, t)
            i = heapq.heappop(M)
        else:
            retlist.append(rlist[0])
        pos = pos + 1
        if (pos == len(SortedRecItems)):
            break
    #print("number of swap ",swapnumber)
    return retlist
