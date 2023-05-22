import random
from itertools import chain, combinations
import matplotlib.pyplot as plt
import numpy as np
from tqdm.notebook import tqdm


def read_transactions(filename):
    """
    Read a file containing transactions, one per line, with items separated by spaces.

    returns a list of itemsets
    """
    with open(filename) as f:
        transactions = [set(line.rstrip().split(" ")) for line in f]
    return transactions


def read_frequent_sets(filename, ndi=False):
    """
    Read a file containing frequent sets

    the expected file format consists of lines of the form
    item1 item2 item3 (support)

    if ndi is True the expected file format consists of lines of the form
    item1 item2 item3 (support) [boounds]

    returns a list of tuples (itemset, support)
    """
    with open(filename) as f:
        sets = [line.rstrip().split(" ") for line in f]
        final_index = -2 if ndi else -1
        sets = [(set(s[:final_index]), int(s[final_index][1:-1])) for s in sets]
    return sets


def write_transactions(filename, transactions):
    """
    Write transactions to a file, one per line, with items separated by spaces.
    """
    with open(filename, "w") as f:
        f.writelines(map(lambda s: " ".join(sorted(s)) + "\n", transactions))


def split_transactions(transactions, split_ratio=0.5):
    """
    For each transaction, split it into two parts based on the split ration

    return list of tuples (x, y) where x is the first part and y is the second part of the original transaction
    """
    results = []
    for t in transactions:
        y = set(random.sample(sorted(t), int(split_ratio * len(t))))
        x = t - y
        results.append((x, y))
    return results


def split_transactions2(transactions, leave_out=3, min_items=7):
    """
    For each transaction, split it into two parts by leaving a set number of transactions out
    Also assures that the transaction has at least a set number of items

    returns list of tuples (x, y) where x is the first part and y is the second part of the original transaction
    """
    results = []
    for t in transactions:
        if len(t) < min_items:
            continue
        y = set(random.sample(sorted(t), leave_out))
        x = t - y
        results.append((x, y))
    return results


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def association_rules(frequent_sets, min_confidence):
    fs_dict = {frozenset(s): sup for s, sup in frequent_sets}
    rules = []
    for itemset, support_itemset in frequent_sets:
        for subset in powerset(itemset):
            antecedent = frozenset(subset)
            consequent = itemset - antecedent
            if len(consequent) == 0 or len(antecedent) == 0:
                continue

            confidence = support_itemset / fs_dict[antecedent]
            if confidence >= min_confidence:
                rules.append((antecedent, consequent, support_itemset, confidence))
    return rules


def calculate_rules_dict(rules):
    rules_dict = {}
    for i, (a, _, _, _) in enumerate(rules):
        for item in a:
            if item not in rules_dict:
                rules_dict[item] = []
            rules_dict[item].append(i)
    return rules_dict


def evaluate_recommendations(test_data, recommender, top_n):
    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for input_items, true_items in test_data:
        # Get recommendations for the user
        recommended_items = set(recommender(input_items, top_n))
        true_items = set(true_items)
        true_positives += len(recommended_items.intersection(true_items))
        false_negatives += len(true_items - recommended_items)

    # Calculate precision, recall, and F1 score
    precision = true_positives / (len(test_data) * top_n)
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0
    )
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )
    return precision, recall, f1_score


def plot_grid(values, x_labels, y_labels, xlabel="", ylabel="", title=""):
    fig, ax = plt.subplots()
    im = ax.imshow(values, cmap=plt.cm.Greens)

    y_range, x_range = values.shape
    plt.xticks(np.arange(x_range), x_labels)
    plt.yticks(np.arange(y_range), y_labels)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    maxv = values.max()
    minv = values.min()

    half_point = minv + (maxv - minv) / 2

    for i in range(y_range):
        for j in range(x_range):
            s = (i, j)
            v = values[i, j]
            t = f"{v:1.3f}"
            c = "white" if v > half_point else "black"
            text = ax.text(j, i, t, ha="center", va="center", color=c, fontsize=8)


def plot_results(experiment_result, name):
    results, supp_list, conf_list = experiment_result
    plot_grid(
        results[:, :, 1],
        conf_list,
        supp_list,
        "Confidence",
        "Support",
        f"{name}",
    )


def run_experiment(supp_list, conf_list, data, recommender, top_n, ndi=False):
    results = np.zeros((len(supp_list), len(conf_list), 3))
    for i, supp in enumerate(supp_list):
        frequent_sets = read_frequent_sets(
            f"data/{'ndi' if ndi else 'apriori'}/{supp}.txt", ndi=ndi
        )
        for j, conf in enumerate(tqdm(conf_list)):
            rules = association_rules(frequent_sets, conf)
            rules_dict = calculate_rules_dict(rules)
            rec = lambda x, n: recommender(x, rules, rules_dict, top_n=n)
            results[i, j, :] = evaluate_recommendations(data, rec, top_n)

    return results, supp_list, conf_list


def sample_recommendations(supp, conf, data, recommender, ndi=False, top_n=3):
    frequent_sets = read_frequent_sets(
        f"data/{'ndi' if ndi else 'apriori'}/{supp}.txt", ndi=ndi
    )
    rules = association_rules(frequent_sets, conf)
    rules_dict = calculate_rules_dict(rules)
    for t0, t1 in data:
        print(recommender(t0, rules, rules_dict, top_n=top_n), t1)
