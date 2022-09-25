from math import sqrt


def largest_prime(k: int) -> int:
    """
    Returns the largest prime number strictly less than k.
    Note that k will always be larger than 2 and at most 100,000
    The algorithm for this method was inspired by the Sieve of Eratosthenes

    :param k: an integer
    :return: a prime number that is strictly less than k
    :complexity: O(Nlog*log N)
    """
    if k <= 2:
        raise ValueError("k must be equal or greater than 2")

    lst = [True for _ in range(k + 1)]  # creates a list of size k+1 and sets each element to True

    root_k = sqrt(k)
    p = 2  # smallest prime number

    while p <= root_k:
        if lst[p] is True:
            for i in range(p * p, k + 1, p):  # cross out the multiples of 2, 3, 5, 7, 11 etc.
                lst[i] = False
        p += 1

    index = 0
    for i in range(2, len(lst) - 1):  # loop from index 2 until k (excluding k)
        if lst[i]:
            index = i
    return index

# **largest_prime() reference from: https://www.wikiwand.com/en/Sieve_of_Eratosthenes