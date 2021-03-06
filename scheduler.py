from abc import ABCMeta, abstractmethod
import copy
import logging

__author__ = 'Azatris'

log = logging.root


class Scheduler(object):
    """ Abstract Scheduler. """
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def compute_next_learning_rate(self):
        """ Updates the information for the stopper and makes
        a decision whether training should be stopped yet. Is called every
        epoch. """

        pass

    @abstractmethod
    def get_learning_rate(self):
        """ Returns the current learning rate. Should be computed first for a
        particular epoch. """

        pass


class ListScheduler(Scheduler):
    """ Scheduler where learning rates are taken from a list for every epoch.
    """
    def __init__(self, learning_rates=None, max_epochs=30):
        if learning_rates is None:
            self.learning_rates = [0.1]
        else:
            self.learning_rates = learning_rates
        self.max_epochs = max_epochs
        self.epoch = 0
        self.learning_rate = self.learning_rates[0]

        super(Scheduler, self).__init__()

    def compute_next_learning_rate(self, accuracy=None, network=None):
        if self.epoch >= self.max_epochs:
            self.learning_rate = 0
        else:
            if len(self.learning_rates) <= self.epoch:
                self.learning_rate = self.learning_rates[-1]
            else:
                self.learning_rate = self.learning_rates[self.epoch]
        self.epoch += 1

    def get_learning_rate(self):
        return self.learning_rate


class DecayScheduler(Scheduler):
    """ Decays/lessens the training when no improvement in a defined threshold
    of epochs has been seen or stops training completely. Depends on evaluator,
    the programmer is trusted to pass the necessary data.
    """

    def __init__(
            self, init_learning_rate=0.1,
            decay_threshold=3, decay=0.01,
            stop_threshold=10, max_epochs=99
    ):
        self.learning_rate = init_learning_rate
        self.decay_threshold = decay_threshold
        self.decay = decay
        self.stop_threshold = stop_threshold
        self.max_epochs = max_epochs

        self.no_improvements_stop = 0
        self.no_improvements_decay = 0
        self.highest_accuracy = 0
        self.highest_accuracy_network = None
        self.epoch = 0

        super(Scheduler, self).__init__()

    def compute_next_learning_rate(self, accuracy=None, network=None):
        # Update no-improvements counter
        if accuracy > self.highest_accuracy:
            self.highest_accuracy = accuracy
            log.info("Highest accuracy network so far: %s", accuracy)
            self.highest_accuracy_network = copy.deepcopy(network)
            self.no_improvements_stop = 0
            self.no_improvements_decay = 0
        else:
            self.no_improvements_stop += 1
            self.no_improvements_decay += 1

        # Change learning rate or stop completely
        if self.no_improvements_stop >= self.stop_threshold or \
                self.epoch >= self.max_epochs:
            self.learning_rate = 0
        elif self.no_improvements_decay >= self.decay_threshold:
            self.learning_rate *= self.decay
            self.no_improvements_decay = 0
            log.info("Learning rate decayed: %s", repr(self.learning_rate))
            print

        self.epoch += 1

    def get_learning_rate(self):
        return self.learning_rate
