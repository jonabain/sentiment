from languageModel import *

class UnigramModel(LanguageModel):

    def __init__(self):
        """
        This is the constructor, don't worry about it. It's done.
        This allows UnigramModel to also access LanguageModel functions
        """
        super(UnigramModel, self).__init__()

    def __str__(self):
        """
        If you try to print a UnigramModel object,
        this is the string that prints
        """
        return "This is a unigram language model"

    def trainText(self, text):
        """
        Requires: text is all the text to train on,
            a list of full-sentence strings
        Modifies: self.wordCounts, a dictionary of {word: frequency}
            pairs. Before training, this dictionary exists
            but it is empty. In this function we want to
            populate it with the frequency information
            for whatever text you are using to train.
        Effects: nothing
        """
        #adds the starting and ending symbols to every sentence in text
        text = self.prepText(text) 
        for string in text:
            for word in string.split():
                if not word in self.wordCounts:
                    #introduces the word to self.wordCounts dictionary
                    self.wordCounts[word] =  1 
                else:
                    self.wordCounts[word] += 1
        		    
    def nextToken(self, sentence):
        """
        Requires: sentence is the sentence so far
        Modifies: nothing
        Effects: Returns the next word to be added to the sentence
        """
        cumulative = 0
        countList = {}
        
        key = sentence[-1] 
        
        for key in self.wordCounts:
            countList[key] = self.wordCounts[key]
        #generates the sum of frequency of all words
        for key in countList: 	    
            countList[key] = countList[key] + cumulative
            #updates cumulative 
            cumulative = cumulative + self.wordCounts[key]
		
        minimum = 0
        nextWordNum = random.randrange(minimum, cumulative)
        for key in countList:
            if nextWordNum < countList[key]:
                return key

    def hasKey(self, sentence):
        """
        Requires: sentence is the sentence so far
        Modifies: nothing
        Effects: Returns True iff this language model can be use
            for this sentence. For a unigram model
            this is True as long as the model knows about
            any words (i.e. has been trained at all)
        """
        length = len(self.wordCounts)
        if length > 0:
            return True
        else:
            return False
