def spearman_correlation(itr1, itr2):
    """
    Calculates the correlation between two lists.

    :param itr1: first iterator
    :param itr2: second iterator
    :return: Spearman correlation (from 0 to 1)
    """
    dict1 = {element: index for index, element in enumerate(itr1)}
    dict2 = {element: index for index, element in enumerate(itr2)}
    sqr_dists_sum = sum(map(lambda diff: diff ** 2, map(lambda element: dict1[element] - dict2[element], itr1)))
    return 1 - ((6 * sqr_dists_sum) / (len(dict1) * (len(dict1) - 1)))
