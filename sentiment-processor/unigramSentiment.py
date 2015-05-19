from sentimentModel import *

class UnigramSentiment(SentimentModel):

    def __init__(self):
        """
        This is the constructor.
        """
        super(UnigramSentiment, self).__init__()
        
    def trainSentiment(self, sentiments):
        """
        Requires: sentiments are the positive and negative sentiments 
            to train on, a list of full-sentence strings beginning with 
            0 or 1
        Modifies: self.sentimentD[zero] and self.sentimentD[one],
            which are themselves 1D dictionaries with '0' or '1' as 
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
            for number in range(1, len(sentenceList)): 
                word = sentenceList[number]
                if sentenceList[0] == zero:
                    if not word in self.sentimentD[zero]:
                        self.sentimentD[zero][word] = 1
                    else:
                        self.sentimentD[zero][word] += 1
                else: 
                    if not word in self.sentimentD[one]:
                        self.sentimentD[one][word] = 1
                    else:
                        self.sentimentD[one][word] += 1
        
    def readSentiment(self, song):
        """
        Requires: song is a song that already exists or 
        was generated and loaded into a file.
        Modifies: sentimentStr, which then has the probability
        of the song having positive or negative sentiment.
        Effects: returns the sentiment that has been read from
        the inputted song.
        """
        downL = DataLoader()
        downL.loadMusicSentiment(song)
        prob = self.probabilities(downL.sentData)
        downL.clearSentData()
        return prob
        
    def probabilities(self, text):
        """
        Requires: Nothing
        Modifies: self.probabilitysD, a 2D dictionary whose innermost
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

        for word in self.sentimentD[zero]:
            if not word in self.probabilityD:
                self.probabilityD[word] = {} 
                if word in self.sentimentD[zero]:
                    zeroTweets = self.sentimentD[zero][word]
                if word in self.sentimentD[one]:
                    oneTweets = self.sentimentD[one][word]
                totalTweets = zeroTweets + oneTweets
                zeroProbability = float(zeroTweets) / float(totalTweets)
                oneProbability = float(oneTweets) / float(totalTweets)
                
                self.probabilityD[word][zero] = zeroProbability
                self.probabilityD[word][one] = oneProbability
        
        zeroProb = 0
        oneProb = 0
        
        for string in text:
            lyricList = string.split()
            listLength = len(lyricList) - 1
            for number in range(listLength):
                word = lyricList[number]
                if word in self.probabilityD:
                    if self.probabilityD[word][zero] > 0 and self.probabilityD[word][zero] < 1:
                        zeroProb += log(self.probabilityD[word][zero])
                        oneProb += log(self.probabilityD[word][one])
                    elif self.probabilityD[word][zero] == 0:
                        zeroProb += 0
                        oneProb += 1
                    else:
                        oneProb += 0
                        zeroProb += 1
                else:
                    oneProb += 0
                    zeroProb += 0
                
        prob = {'zero': zeroProb, 'one': oneProb}
        return prob
