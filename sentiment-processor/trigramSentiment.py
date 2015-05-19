from sentimentModel import *

class TrigramSentiment(SentimentModel):

    def __init__(self):
        super(TrigramSentiment, self).__init__()

    def trainSentiment(self, sentiments):
        zero = '0'
        one = '1'
        
        self.sentimentD[zero] = {}
        self.sentimentD[one] = {}
        for string in sentiments: 
            sentenceList = string.split() 
            for number in range(1, len(sentenceList) - 2): 
                word1 = sentenceList[number]
                word2 = sentenceList[number + 1]
                word3 = sentenceList[number + 2] 
                if sentenceList[0] == zero:
                    if not word1 in self.sentimentD[zero]:
                        self.sentimentD[zero][word1]= {} 
                        self.sentimentD[zero][word1][word2] = {}
                        self.sentimentD[zero][word1][word2][word3] = 1
                    elif not word2 in self.sentimentD[zero][word1]:
                        self.sentimentD[zero][word1][word2] = {}  
                        self.sentimentD[zero][word1][word2][word3] = 1
                    elif not word3 in self.sentimentD[zero][word1][word2]:
                        self.sentimentD[zero][word1][word2][word3] = 1
                    else:
                        self.sentimentD[zero][word1][word2][word3] += 1
                else: 
                    if not word1 in self.sentimentD[one]:
                        self.sentimentD[one][word1]= {} 
                        self.sentimentD[one][word1][word2] = {}
                        self.sentimentD[one][word1][word2][word3] = 1
                    elif not word2 in self.sentimentD[one][word1]:
                        self.sentimentD[one][word1][word2] = {} 
                        self.sentimentD[one][word1][word2][word3] = 1
                    elif not word3 in self.sentimentD[one][word1][word2]:
                        self.sentimentD[one][word1][word2][word3] = 1
                    else:
                        self.sentimentD[one][word1][word2][word3] += 1
        
        
    def probabilities(self, songText):
        zero = '0'
        one = '1'

        zeroTweets = 0
        oneTweets = 0
        totalTweets = 0

        for word1 in self.sentimentD[zero]:
            for word2 in self.sentimentD[zero][word1]:
                for word3 in self.sentimentD[zero][word1][word2]: 
                    if not word1 in self.probabilityD:
                        self.probabilityD[word1] = {} 
                        self.probabilityD[word1][word2] = {}
                        self.probabilityD[word1][word2][word3] = {} 
                    elif not word2 in self.probabilityD[word1]:
                        self.probabilityD[word1][word2] = {}
                        self.probabilityD[word1][word2][word3] = {}
                    elif not word3 in self.probabilityD[word1][word2]:
                        self.probabilityD[word1][word2][word3] = {} 
                    if word1 in self.sentimentD[zero]:
                        if word2 in self.sentimentD[zero][word1]:
                            if word3 in self.sentimentD[zero][word1][word2]: 
                                zeroTweets = self.sentimentD[zero][word1][word2][word3] 
                    if word1 in self.sentimentD[one]:
                        if word2 in self.sentimentD[one][word1]:
                            if word3 in self.sentimentD[one][word1][word2]: 
                                oneTweets = self.sentimentD[one][word1][word2][word3]
                    totalTweets = zeroTweets + oneTweets
                    zeroProbability = float(zeroTweets) / float(totalTweets)
                    oneProbability = float(oneTweets) / float(totalTweets)
                
                    self.probabilityD[word1][word2][word3][zero] = zeroProbability
                    self.probabilityD[word1][word2][word3][one] = oneProbability
    
        songZeroProb = 0
        songOneProb = 0
        
        for string in songText:
            lyricList = string.split()
            for number in range(len(lyricList) - 2):
                word1 = lyricList[number]
                word2 = lyricList[number + 1]
                word3 = lyricList[number + 2] 
                if word1 in self.probabilityD:
                    if word2 in self.probabilityD[word1]:
                        if word3 in self.probabilityD[word1][word2]: 
                            if self.probabilityD[word1][word2][word3][zero] > 0 and self.probabilityD[word1][word2][word3][zero] < 1:
                                songZeroProb += log(self.probabilityD[word1][word2][word3][zero])
                                songOneProb += log(self.probabilityD[word1][word2][word3][one])
                            elif self.probabilityD[word1][word2][word3][zero] == 0:
                                songZeroProb += 0
                                songOneProb += 1
                            else:
                                songOneProb += 0
                                songZeroProb += 1
                        else:
                            songOneProb += 0
                            songZeroProb += 0
                    else:
                        songOneProb += 0
                        songZeroProb += 0
                
        prob = {'zero': songZeroProb, 'one': songOneProb}
        return prob
