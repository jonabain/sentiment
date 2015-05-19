from languageModel import *

class BigramModel(LanguageModel):

    def __init__(self):
        """
        This is the constructor, don't worry about it. It's done.
        This allows BigramModel to also access LanguageModel functions
        """
        super(BigramModel, self).__init__()

    def __str__(self):
        """
        If you try to print a BigramModel object,
        this is the string that prints
        """
        return "This is a bigram language model"

    def trainText(self, text):
        """
        Requires: text is all the text to train on,
            a list of full-sentence strings
        Modifies: self.wordCounts, a 2D dictionary
            This model is one level more complicated
            than the UnigramModel. This model counts how
            often each word appears AFTER each other word.
            See section 2.3.4 for an example
            Effects: nothing
        """
        text = self.prepText(text) 
        for string in text: 
            sentenceList = string.split() 
            listLength = len(sentenceList) - 1
            #loops through range 
            for number in range(0, listLength): 
            	#if a word isn't found in wordCounts, sets a new spot in the dictionary for it 
                if not sentenceList[number] in self.wordCounts:
                    newWord = sentenceList[number]
                    self.wordCounts[newWord] = {}
                    followWord = sentenceList[number + 1]
                    self.wordCounts[newWord][followWord] = 1 
                #adds to word count only if word is already in wordCounts; sets frequency to 1 otherwise  
                else: 
                    oldWord = sentenceList[number]
                    followWord = sentenceList[number + 1]
                    if followWord in self.wordCounts[oldWord]:
                        self.wordCounts[oldWord][followWord] += 1
                    else:
                    	self.wordCounts[oldWord][followWord] = 1
     	    
    def nextToken(self, sentence):
        """
        Requires: sentence is the sentence so far
            hasKey(self, sentence) == True
        Modifies: nothing
        Effects: returns the next word to be added to the sentence
            This function is very similar to the function you wrote
            for UnigramModel.
            An example of this mechanism is available in Appendix B.2 of
            the spec, along with pictures.
        """
        #creates a cumulative value to add word counts to 
        cumulative = 0
     
        key1 = sentence[-1]
        
        secondKeys = self.wordCounts[key1].keys()
        
        countList = []
        #appends our empty countList by looping through key 
        for key2 in secondKeys:
            cumulative = cumulative + self.wordCounts[key1][key2]
            countList.append(cumulative)
            
        minimum = 0
        
        nextWordNum = random.randrange(minimum, cumulative + 1)
       
        #picks a next word based on its probability of appearing 
        for num in range(len(countList)):
            if nextWordNum <= countList[num]:
                
            	return secondKeys[num]
    
        return "HELLO"

    def hasKey(self, sentence):
        """
        Requires: sentence is the sentence so far
        Modifies: nothing
        Effects: Returns True iff this language model can be used
            for this sentence. For a bigram model, this is True
            as long as the model has seen the last word
            in the sentence before at the start of a bigram.
	"""
        if sentence[-1] in self.wordCounts:
            return True
        else:
            return False
