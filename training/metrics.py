import math


def precision_at_k(recommended, relevant, k=10):
    selected = recommended[:k]
    return sum(item in relevant for item in selected) / len(selected) if selected else 0.0


def recall_at_k(recommended, relevant, k=10):
    return (
        sum(item in relevant for item in recommended[:k]) / len(relevant)
        if relevant
        else 0.0
    )


def mrr(recommended, relevant):
    for index, item in enumerate(recommended, start=1):
        if item in relevant:
            return 1.0 / index
    return 0.0


def ndcg_at_k(relevances, k=10):
    def dcg(values):
        return sum(
            (2**relevance - 1) / math.log2(index + 2)
            for index, relevance in enumerate(values)
        )

    values = relevances[:k]
    ideal = sorted(relevances, reverse=True)[:k]
    denominator = dcg(ideal)
    return dcg(values) / denominator if denominator else 0.0
