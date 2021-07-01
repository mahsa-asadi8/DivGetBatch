
from Utils.IndexTree import BuildIndex
import timeit
from Utils.Utils import yelp_data,makeBlobs_data,movieLens_data
from .AugMMR import AugMMR
from .MMR import MMR
from Utils.Utils import checkResult


def runMMR(sampleSize, arity,numberofLevel,k):
    print('dataset size: ', sampleSize, 'k:', k, 'number of arity: ',
          arity, 'number of level: ', numberofLevel)

    #X = movieLens_data(sampleSize)
    #X = yelp_data(sampleSize)
    X = makeBlobs_data(sampleSize)



    xin = X.tolist()
    iTree,indexMap = BuildIndex(xin,arity,numberofLevel,False)

    q = [2,5]
    lambda_score = 0.8

    Xmmr = X.tolist()
    start = timeit.default_timer()

    mmrResult = MMR(lambda_score, q, Xmmr, k)

    print("mmr", mmrResult)
    stop = timeit.default_timer()
    mmr_time = stop - start
    print('Time for mmr: ', mmr_time)


    start = timeit.default_timer()

    augmmrResult = AugMMR(iTree,numberofLevel,arity,q,lambda_score,k,indexMap)
    print("aug", augmmrResult)

    stop = timeit.default_timer()
    augmmr_time = stop - start
    print('Time for aug-mmr: ', augmmr_time)

    checkResult(augmmrResult, mmrResult)


