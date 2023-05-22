from itertools import chain


def support(itemset, transactions):
    return len([t for t in transactions if itemset.issubset(t)])


def join_and_prune(L, k):
    return set(
        [
            itemset1.union(itemset2)
            for itemset1 in L
            for itemset2 in L
            if len(itemset1.union(itemset2)) == k + 1
        ]
    )
    # CC = C.copy()
    # for item in C:
    #     subsets = combinations(item, k)
    #     for subset in subsets:
    #         # if the subset is not in previous K-frequent get, then remove the set
    #         if frozenset(subset) not in L:
    #             CC.remove(item)
    #             break
    # return CC


def apriori(transactions, min_support):
    # final result
    frequent_itemsets = set()

    # get frequent itemsets containing single item
    C = {frozenset([item]) for item in set(chain(*transactions))}
    L = {c for c in C if support(c, transactions) >= min_support}
    frequent_itemsets.update(L)

    k = 1
    while L:
        # get candidate from previous frequent itemsets
        C = join_and_prune(L, k)
        # discards candidates with low support
        L = {c for c in C if support(c, transactions) >= min_support}
        frequent_itemsets.update(L)
        k += 1

    return frequent_itemsets
