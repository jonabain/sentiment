from dataLoader import *
from unigramSentiment import *
from bigramSentiment import *
from trigramSentiment import *

class SentimentReader(object):
    
    def __init__(self):
        """
        Constructor. Creates instances of all sentiment classes that use tweets.
        """
        self.unigramS = UnigramSentiment()
        self.bigramS = BigramSentiment()
        self.trigramS = TrigramSentiment()
        
    def trainSentiment(self, sentiments):
        """
        Trains text for all the instances below. This just populates self.sentimentD in each file.
        self.sentimentD is used to calculate probabilities eventually.
        """
        self.unigramS.trainSentiment(sentiments)
        self.bigramS.trainSentiment(sentiments)
        self.trigramS.trainSentiment(sentiments)
        
    def readSentiment(self, file):
        """
        This function loads a file into a list of full sentence strings and passed it
        to the probabilities() function for each class. This uses self.sentimentD to calculate
        the probabilities with the Naive Bayes approach.
        """
        file = self.read(file)
        uProb = self.unigramS.probabilities(file)
        bProb = self.bigramS.probabilities(file)
        tProb = self.trigramS.probabilities(file)
        
        songZeroProb = 0
        songOneProb = 0
        
        probs = []
        probs.append(uProb)
        probs.append(bProb)
        probs.append(tProb)
        
        for item in probs:
            for key in item:
                if key == 'zero':
                    songZeroProb += item[key]
                else:
                    songOneProb += item[key]
                    
        if songZeroProb > songOneProb:
            return "Using tweet data, the SenTAYments say this song has negative sentiment."
        elif songZeroProb < songOneProb:
            return "Using tweet data, the SenTAYments say this song has positive sentiment."
        elif songZeroProb == songOneProb:
            return "Using tweet data, the SenTAYments say this song is neutral."
        else:
            return "An error occurred. Sentiment test inconclusive."

    def read(self, song):
        """
        Takes a file name and makes a list of full sentence strings of all the words that appear in that
        song file. Clears self.sentData into an empty list at the end
        """
        
        downL = DataLoader()
        downL.loadMusicSentiment(song)
        song = downL.sentData
        downL.clearSentData()
        return song
