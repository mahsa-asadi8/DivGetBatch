
from pyclustering.utils import euclidean_distance_square

import numpy as np

def GMM(D, K,initRecords):
    S = []
    S.extend(list(initRecords))
    D.remove(initRecords[0])
    D.remove(initRecords[1])
    minMap = {}

    for i in D:
        dist = euclidean_distance_square(i, initRecords[0])
        minMap[tuple(i)] = dist
    nextItem = initRecords[1]

    for k in range(K - 2):
        L = []
        for i in D:
            min = minMap[tuple(i)]
            dist = euclidean_distance_square(i, nextItem)
            if min > dist:
                min = dist
                minMap[tuple(i)] = min
            L.append(min)
        index_max = np.argmax(L)
        nextItem = D[index_max]
        S.append(D[index_max])
        D.remove(D[index_max])
    return S
