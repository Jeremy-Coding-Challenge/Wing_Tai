from itertools import combinations


def count_pairs(input_array, minimum_difference, maximum_difference):
    unique_pairs = list(combinations(set(input_array), 2))
    pairs_within_limit = [
        (i, j)
        for i, j in unique_pairs
        if minimum_difference <= abs(i - j) <= maximum_difference
    ]
    return len(pairs_within_limit)


if __name__ == "__main__":
    # Feel free to add new test cases here
    assert count_pairs([1, 1, 2, 2], 1, 2) == 1
    assert count_pairs([1, 1, 2, 2, 3], 2, 4) == 1
    assert count_pairs([1, 2, 1, 6, 3], 2, 4) == 3
    assert count_pairs([1, 2, 1, 6, 3], 1, 4) == 5

    print("Pass all given test case")
