
import timeit
from Utils.Utils import createSimMatrix, topkitems, div
from .SWAP import SWAP
from  .AugSWAP import AugSWAP
from Utils.IndexTree  import BuildIndex
from Utils.Utils import checkResult
from Utils.Utils import yelp_data,makeBlobs_data,movieLens_data


def runSWAP(sampleSize, arity, numberofLevel, k):

    print('dataset size: ', sampleSize, 'k:', k, 'number of arity: ',
          arity, 'number of level: ', numberofLevel)

    X = yelp_data(sampleSize)
    #X = makeBlobs_data(sampleSize)
    # X = movieLens_data(sampleSize)


    X = X.tolist()
    query = [1, -1, 1]
    r = createSimMatrix(query, X)
    ub = 1000000

    start = timeit.default_timer()
    res = SWAP(X, r, k, ub)
    stop = timeit.default_timer()
    print('Time for calculate swap: ', stop - start)

    # print("swap: ",res)

    iTree,indexMap = BuildIndex(X, arity, numberofLevel,True)

    start = timeit.default_timer()
    augres = AugSWAP(X, iTree, r, k, ub)
    stop = timeit.default_timer()
    print('Time for calculate Aug swap: ', stop - start)

    # print("AugSwap: ",augres)

    checkResult(augres, res)

