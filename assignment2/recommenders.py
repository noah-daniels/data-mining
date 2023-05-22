def recommend_average_confidence(input_items, rules, rules_dict, top_n=5):
    """
    Original: average confidence
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, support, confidence = rules[index]
        if antecedent.issubset(input_items):
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = []
                recommendations[item].append((confidence, support))
    recommendations = {
        item: (
            sum(conf for conf, _ in item_rules) / len(item_rules),
            sum(sup for _, sup in item_rules) / len(item_rules),
        )
        for item, item_rules in recommendations.items()
    }
    sorted_recommendations = sorted(
        recommendations.items(), key=lambda x: (-x[1][0], -x[1][1])
    )
    return [item for item, _ in sorted_recommendations[:top_n]]


def recommend_popularity(input_items, rules, rules_dict, top_n=5):
    # top-20 most popular items in training data
    popular_items = [
        "39",
        "48",
        "38",
        "41",
        "32",
        "65",
        "89",
        "225",
        "170",
        "237",
        "36",
        "110",
        "310",
        "101",
        "475",
        "271",
        "438",
        "413",
        "147",
        "1327",
        "2238",
        "270",
        "79",
        "60",
        "255",
        "533",
        "12925",
        "1146",
        "9",
        "185",
        "14098",
        "16010",
        "123",
        "338",
        "604",
        "16217",
        "592",
        "824",
        "740",
        "249",
        "301",
        "1393",
        "15832",
        "548",
        "286",
        "201",
        "49",
        "37",
        "1004",
        "589",
        "677",
        "78",
        "161",
        "13041",
        "258",
        "117",
        "179",
        "522",
        "19",
        "783",
        "3270",
        "175",
        "31",
        "264",
        "479",
        "405",
        "956",
        "10515",
        "45",
        "2958",
        "242",
        "1578",
        "76",
        "649",
        "18",
        "389",
        "544",
        "549",
        "1600",
        "229",
        "156",
        "976",
        "570",
        "766",
        "812",
        "703",
        "103",
        "1344",
        "371",
        "334",
        "107",
        "664",
        "23",
        "1435",
        "806",
        "772",
        "449",
        "488",
        "55",
        "12929",
    ]
    result = []
    for item in popular_items:
        if item not in input_items:
            result.append(item)
    return result[:top_n]


def recommend_number_rules(input_items, rules, rules_dict, top_n=5):
    """
    Rank by number of rules
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, _, _ = rules[index]
        if antecedent.issubset(input_items):
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += 1

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])

    return [item for item, _ in sorted_recommendations[:top_n]]


def recommend_total_confidence(input_items, rules, rules_dict, top_n=5):
    """
    Total confidence
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, _, confidence = rules[index]
        if antecedent.issubset(input_items):
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += confidence

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])

    return [item for item, _ in sorted_recommendations[:top_n]]


def recommend_total_support(input_items, rules, rules_dict, top_n=5):
    """
    Total support
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, support, _ = rules[index]
        if antecedent.issubset(input_items):
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += support

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])

    return [item for item, _ in sorted_recommendations[:top_n]]


def recommend_weighted_confidence(input_items, rules, rules_dict, top_n=5):
    """
    Total confidence weighted by number of items in consequent that match history
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, _, confidence = rules[index]
        if antecedent.issubset(input_items):
            w = 1 + len(consequent.intersection(input_items))
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += w * confidence

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])

    return [item for item, _ in sorted_recommendations[:top_n]]


def recommend_popularity_discount(input_items, rules, rules_dict, top_n=5):
    """
    Total confidence, discounted by popularity
    """
    relevant_rules = set()
    for item in input_items:
        if item in rules_dict:
            relevant_rules.update(rules_dict[item])

    recommendations = dict()
    for index in relevant_rules:
        antecedent, consequent, support, confidence = rules[index]
        if antecedent.issubset(input_items):
            for item in consequent - input_items:
                if item not in recommendations:
                    recommendations[item] = 0
                recommendations[item] += confidence

    bases = {i: 0 for i in recommendations.keys()}
    for a, c, sup, conf in rules:
        for i in c:
            if i in bases:
                bases[i] += 1

    recommendations = {item: v / bases[item] for item, v in recommendations.items()}

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])

    return [item for item, _ in sorted_recommendations[:top_n]]
