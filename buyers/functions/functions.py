from numpy.random import binomial
from otree.api import *

def calculate_earnings(quality, p):
    turn = binomial(1, p)
    if (turn == 1 and quality == 0) or (turn == 0 and quality == 1):
        return False
    else:
        return True


def is_set(x, n):
    return x & 1 << n != 0

# def add_posRating(subsession, item):
#     session = subsession.session
#     session.positive_quality[item] += 1
#     print(session.positive_quality)
#     pass


# def add_negRating(subsession, item):
#     session = subsession.session
#     session.negative_quality[item] += 1
#     print(session.negative_quality)
#     pass
