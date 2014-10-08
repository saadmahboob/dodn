__author__ = 'Azatris'

import numpy as np


class Utils(object):
    @staticmethod
    def vectorize_digit(i):
        """ Return a 10-dimensional one-hot vector with a 1.0 in the ith
        position and zeroes elsewhere.  This is used to convert a digit into a
        corresponding desired output from the neural network."""

        vectorized_digit = np.zeros((10, 1))
        vectorized_digit[i] = 1.0
        return vectorized_digit


class CrossEntropyCost:
    def __init__(self):
        pass

    @staticmethod
    def fn(a, y):
        return np.nan_to_num(np.sum(-y*np.log(a) - (1 - y)*np.log(1 - a)))

    @staticmethod
    def delta(a, y):
        return a - y