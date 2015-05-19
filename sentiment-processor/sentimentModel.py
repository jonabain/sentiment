from math import log

class SentimentModel(object):

    def __init__(self):
        """
        just a simple constructor. this class is pretty pointless.
        """
        self.sentimentD = {}
        self.probabilityD = {}
