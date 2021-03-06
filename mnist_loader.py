from utils import Utils

__author__ = 'Azatris'

import cPickle
import gzip
import numpy as np


def load_data():
    """ Returns MNIST data as a 3-tuple containing the training data,
    the validation data and the test data. (ref:
    http://www.deeplearning.net/tutorial/gettingstarted.html,
    http://neuralnetworksanddeeplearning.com/chap1.html)

    ``training_data`` is a 2-tuple.
    First of the tuple contains 50,000 training images (numpy ndarray
    with 50,000 entries), each of which has 28*28 pixels (numpy ndarray
    with 784 values).
    Second of the tuple contains 50,000 labels for the training images,
    respectively (numpy ndarray with 50,000 values) where each is a
    a single digit from 0 to 9.

    ``validation_data`` and ``test_data`` are similar to
    ``training_data``, but instead having 10,000 images each. """

    with gzip.open('data/mnist.pkl.gz', 'rb') as f:
        training_data, validation_data, test_data = cPickle.load(f)
        return training_data, validation_data, test_data


def load_data_revamped():
    """ Return MNIST data as a 3-tuple containing the training data,
    the validation data and the test data in a revamped form
    more suitable for training neural networks. (ref:
    http://neuralnetworksanddeeplearning.com/chap1.html)

    ``training data`` is an ndarray of 50,000 tuples of (x, y)
    where x is a ndarray of size 784 representing the training image,
    and where y is the corresponding label in a one-hot form of
    ndarray of size 10.

    ``validation_data`` and ``test_data`` are similar to
    ``training_data``, but instead having 10,000 tuples of (x, y)
    and where y remains a single digit from 0 to 9. """

    raw_tr_data, raw_va_data, raw_te_data = load_data()

    training_inputs = np.asarray([np.reshape(x, 784) for x in raw_tr_data[0]])
    training_results = np.asarray(
        [Utils.vectorize_digit(y) for y in raw_tr_data[1]]
    )
    training_data = (training_inputs, training_results)

    validation_inputs = np.asarray([np.reshape(x, 784) for x in raw_va_data[0]])
    validation_data = (validation_inputs,  raw_va_data[1])

    test_inputs = np.asarray([np.reshape(x, 784) for x in raw_te_data[0]])
    test_data = (test_inputs, raw_te_data[1])

    return training_data, validation_data, test_data