from itertools import chain


def join_set(itemsets, k):
    return set(
        [
            itemset1.union(itemset2)
            for itemset1 in itemsets
            for itemset2 in itemsets
            if len(itemset1.union(itemset2)) == k
        ]
    )


def itemsets_support(transactions, itemsets, min_support):
    support_count = {itemset: 0 for itemset in itemsets}
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_count[itemset] += 1
    n_transactions = len(transactions)
    return {
        itemset: support / n_transactions
        for itemset, support in support_count.items()
        if support / n_transactions >= min_support
    }


def apriori(transactions, min_support):
    items = set(chain(*transactions))
    itemsets = [frozenset([item]) for item in items]
    itemsets_by_length = [set()]
    k = 1
    while itemsets:
        support_count = itemsets_support(transactions, itemsets, min_support)
        itemsets_by_length.append(set(support_count.keys()))
        k += 1
        itemsets = join_set(itemsets, k)
    frequent_itemsets = set(chain(*itemsets_by_length))
    return frequent_itemsets, itemsets_by_length
