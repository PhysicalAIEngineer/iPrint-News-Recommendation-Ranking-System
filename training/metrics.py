import math
def precision_at_k(recommended,relevant,k=10):
    x=recommended[:k]; return sum(i in relevant for i in x)/len(x) if x else 0.0
def recall_at_k(recommended,relevant,k=10):
    return sum(i in relevant for i in recommended[:k])/len(relevant) if relevant else 0.0
def mrr(recommended,relevant):
    for i,item in enumerate(recommended,1):
        if item in relevant:return 1.0/i
    return 0.0
def ndcg_at_k(relevances,k=10):
    def dcg(xs): return sum((2**r-1)/math.log2(i+2) for i,r in enumerate(xs))
    v=relevances[:k]; ideal=sorted(relevances,reverse=True)[:k]; denom=dcg(ideal)
    return dcg(v)/denom if denom else 0.0
