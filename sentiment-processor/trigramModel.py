from languageModel import *

class TrigramModel(LanguageModel):

    def __init__(self):
        """
        This is the constructor, don't worry about it. It's done.
        This allows the TrigramModel to access LanguageModel functions
        """
        super(TrigramModel, self).__init__()

    def __str__(self):
        """
        If you try to print a TrigramModel object
        this is the string that prints
        """
        return "This is a trigram language model"

    def trainText(self, text):
        """
        Requires: text is all the text to train on,
            a list of full-sentence strings
        Modifies: self.wordCounts, a 3D dictionary
            This model is one level more complicated than
            the BigramModel. This model counts 3-word phrases
            instead of 2-word phrases like the BigramModel did.
            See Section 2.3.4 of the spec for an example.
        Effects: Nothing
        """
        newText = self.prepText(text)
        for string in newText:
            sentenceList = string.split()
            
            #loops through range; -2 ensures number does not go out of bounds
            for number in range((len(sentenceList) - 2)):
            	word1 = sentenceList[number]
            	word2 = sentenceList[number + 1]
            	word3 = sentenceList[number + 2]
            	
            	#creates a word count for a new word1
            	if not word1 in self.wordCounts:
                    self.wordCounts[word1] = {}
                    self.wordCounts[word1][word2] = {}
                    self.wordCounts[word1][word2][word3] = 1
                #creates a word count for a new word2
                elif not word2 in self.wordCounts[word1]:
                    self.wordCounts[word1][word2] = {}
                    self.wordCounts[word1][word2][word3] = 1
                #creates a word count for a new word3    
                elif not word3 in self.wordCounts[word1][word2]:
                    self.wordCounts[word1][word2][word3] = 1
                #adds to word count if word is already in wordCounts
                else:
                    self.wordCounts[word1][word2][word3] += 1
        
    def nextToken(self, sentence):
        """
        Requires: sentence is the sentence so far
            hasKey(self, sentence) == True
        Modifies: nothing
        Effects: returns the next word to be added to the sentence
            This function is very similar to the function you wrote
            for BigramModel.
            An example of this mechanism is available is Appendix B.2
            of the spec, along with pictures.
        """
        #creates a cumulative value to add word counts to
        cumulative = 0
        
        key1 = sentence[-2]
        key2 = sentence[-1]
        
        thirdKeys = self.wordCounts[key1][key2].keys()
        
        countList = []
        
        #appends our empty countList by looping through key
        for key in thirdKeys:
            cumulative = cumulative + self.wordCounts[key1][key2][key]
            countList.append(cumulative)
        
        minimum = 0
        
        nextWordNum = random.randrange(minimum, cumulative + 1)
        
        #picks a next word based on its probability of appearing
        for num in range(len(countList)):
            if nextWordNum <= countList[num]:
                return thirdKeys[num]
                        
    def hasKey(self, sentence):
        """
        Requires: sentence is the sentence so far
        Modifies: nothing
        Effects: Returns True iff this language model can be used
            for this sentence. For a trigram model, this is True
            as long as the model as seen the last two words
            together before.
        """
        lastWord = sentence[-1]
        secondLast = sentence[-2]
        if secondLast in self.wordCounts:
            if lastWord in self.wordCounts[secondLast]:
                return True
            else:
                return False
        else:
            return False
