
from Utils.Utils import similarity
def MMR(lambda_score, q, data, k):

    docs_unranked = data

    docs_selected = []

    best = [0,0]
    for i in range (k):
        mmr = -100000000
        for d in docs_unranked:
            sim = 0
            for s in docs_selected:
                sim_current = similarity(d, s)
                if sim_current > sim:
                    sim = sim_current
                else:
                    continue

            rel = similarity(q, d)
            mmr_current = lambda_score * rel - (1 - lambda_score) * sim

            if mmr_current > mmr:
                mmr = mmr_current
                best = d
            else:
                continue


        docs_selected.append(best)
        docs_unranked.remove(best)

    return docs_selected