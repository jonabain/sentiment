from sentimentModel import *

class BigramSentiment(SentimentModel):

    def __init__(self):
        """
        This is the constructor.
        """
        super(BigramSentiment, self).__init__()

    def trainSentiment(self, sentiments):
        """
        Requires: sentiments are the positive and negative sentiments 
            to train on, a list of full-sentence strings beginning with 
            0 or 1
        Modifies: self.sentimentD[zero] and self.sentimentD[one],
            which are themselves 2D dictionaries with '0' or '1' as 
            the first keys that ultimately contain word: frequency 
            pairs. This serves to count frequencies of positive- and 
            negative- sentiment words.
        Effects: nothing
        """
        zero = '0'
        one = '1'
        
        self.sentimentD[zero] = {}
        self.sentimentD[one] = {}

        for string in sentiments: 
            sentenceList = string.split() 
            for number in range(1, len(sentenceList) - 1): 
                word1 = sentenceList[number]
                word2 = sentenceList[number + 1]
                if sentenceList[0] == zero:
                    if not word1 in self.sentimentD[zero]:
                        self.sentimentD[zero][word1] = {}
                        self.sentimentD[zero][word1][word2] = 1
                    elif not word2 in self.sentimentD[zero][word1]:
                        self.sentimentD[zero][word1][word2] = 1
                    else:
                        self.sentimentD[zero][word1][word2] += 1
                else: 
                    if not word1 in self.sentimentD[one]:
                        self.sentimentD[one][word1] = {}
                        self.sentimentD[one][word1][word2] = 1
                    elif not word2 in self.sentimentD[one][word1]:
                        self.sentimentD[one][word1][word2] = 1
                    else:
                        self.sentimentD[one][word1][word2] += 1
        
        
    def probabilities(self, text):
        """
        Requires: Nothing
        Modifies: self.probabilityD, a 3D dictionary whose innermost 
            dictionaries that are words with the keys '0' and '1' 
            and values that are probabilities. 
        Effects: returns a sentiment string of positive or negative
            probabilities
        """
        zero = '0'
        one = '1'

        zeroTweets = 0
        oneTweets = 0
        totalTweets = 0

        for word1 in self.sentimentD[zero]:
            for word2 in self.sentimentD[zero][word1]:
                if not word1 in self.probabilityD:
                    self.probabilityD[word1] = {} 
                    self.probabilityD[word1][word2] = {}
                elif not word2 in self.probabilityD[word1]:
                    self.probabilityD[word1][word2] = {}
                if word1 in self.sentimentD[zero]:
                    if word2 in self.sentimentD[zero][word1]:
                        zeroTweets = self.sentimentD[zero][word1][word2]
                if word1 in self.sentimentD[one]:
                    if word2 in self.sentimentD[one][word1]:
                        oneTweets = self.sentimentD[one][word1][word2]
                totalTweets = zeroTweets + oneTweets
                zeroProbability = float(zeroTweets) / float(totalTweets)
                oneProbability = float(oneTweets) / float(totalTweets)
                
                self.probabilityD[word1][word2][zero] = zeroProbability
                self.probabilityD[word1][word2][one] = oneProbability
       
        zeroProb = 0
        oneProb = 0
        
        for string in songText:
            lyricList = string.split()
            for number in range(len(lyricList) - 1):
                word1 = lyricList[number]
                word2 = lyricList[number + 1]
                if word1 in self.probabilityD:
                    if word2 in self.probabilityD[word1]:
                        if self.probabilityD[word1][word2][zero] > 0 and self.probabilityD[word1][word2][zero] < 1:
                            zeroProb += log(self.probabilityD[word1][word2][zero])
                            oneProb += log(self.probabilityD[word1][word2][one])
                        elif self.probabilityD[word1][word2][zero] == 0:
                            zeroProb += 0
                            oneProb += 1
                        else:
                            oneProb += 0
                            zeroProb += 1
                    else:
                        oneProb += 0
                        zeroProb += 0
                else:
                    oneProb += 0
                    zeroProb += 0
                
        prob = {'zero': zeroProb, 'one': oneProb}
        return prob
