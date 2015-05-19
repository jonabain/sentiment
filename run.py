import sys
sys.path.append('./lm')
sys.path.append('./Reach')

from dataLoader import *
from unigramModel import *
from bigramModel import *
from trigramModel import *
from sentimentReader import *
from movieSentiment import *

def main():
    sentimentModel = SentimentReader()
    movieSentiment = MovieSentiment()
    populate(sentimentModel, movieSentiment)
    welcomeMessage()
    
    #loads all music, tweet, and review sentiments 
    SOURCEDIR = ["taylor_swift"]
    SOURCEDIRECTORY = ["Tweets"]
    for dir in SOURCEDIR:
        dl = DataLoader()
        dl.loadMusic(dir)
    print '\n', "* All Taylor Swift Music Has Been Loaded *", '\n'
    for dir in SOURCEDIRECTORY:
        download = DataLoader()
        download.loadTweets(dir)
    print "* All Twitter Sentiments Have Been Loaded. *", '\n'
    download.loadMovieData("Reviews")
    print "* All Movie Review Sentiments Have Been Loaded. *", '\n'
    
    #gives code for the 3 options the menu prompts users to choose from 
    done = False
    choice = 1
    while (done == False):
        choice = printMenu()
        
        if choice in ['1']:
            
            file = readTaySong()
            while (file == 'invalid'):
                print '\n', 'Error!', '\n'
                file = readTaySong()
            #analyzes and prints the sentiment analysis of the song based off of tweet & review sentiments      
            movieSentiment.trainSentiment(download.posMovieData, download.negMovieData)
            movieSentimentStr = readMovieForEmotion(movieSentiment, file)
            sentimentModel.trainSentiment(download.tweetData)
            sentimentStr = readForEmotion(sentimentModel, file)
            print sentimentStr, '\n'
            print
            print movieSentimentStr, '\n'
            done == False
        #generates a new TaySwift song   
        elif choice in ['2']:
            movieSentiment.trainSentiment(download.posMovieData, download.negMovieData)
            sentimentModel.trainSentiment(download.tweetData)
            unigram = UnigramModel()
            unigram.trainText(dl.data)
            bigram = BigramModel()
            bigram.trainText(dl.data)
            trigram = TrigramModel()
            trigram.trainText(dl.data)
            models = [trigram, bigram, unigram]
            chorus = []
            verse1 = []
            verse2 = []
            verse3 = []
            songParts = []
            songParts.append(verse1)
            songParts.append(chorus)
            songParts.append(verse2)
            songParts.append(verse3)
            songFile = open("newTaySong.txt", 'w')
            for i in range(4):
                for j in range(4):
                    newSentence = generateSentence(models, 8)
                    songFile.write(newSentence)
                    songFile.write('\n')
                    songParts[i].append(newSentence)
            songFile.close()
            print 'The SenTAYments original song for you is:', '\n'
            for sentence in songParts[1]:
                print '    ', sentence
            print '\n'
            for sentence in songParts[0]:
                print '    ', sentence
            print '\n'
            for sentence in songParts[2]:
                print '    ', sentence
            print '\n'
            for sentence in songParts[0]:
                print '    ', sentence
            print '\n'
            for sentence in songParts[3]:
                print '    ', sentence
            print '\n' 
            for sentence in songParts[0]:
                print '    ', sentence
            print '\n'
            sentimentStr = readForEmotion(sentimentModel, "newTaySong.txt")
            movieSentimentStr = readMovieForEmotion(movieSentiment, "newTaySong.txt")
            
            print sentimentStr, '\n'
            print movieSentimentStr, '\n'
            done = False
        #quits program if user selects option 3   
        elif choice in ['3']:
            printBye()
            done = True
        else:
            junk = 'do stuff'
            done = False
            
def welcomeMessage():
    print 'Welcome.'
    

def printMenu():
    print '\n', '***************SenTAYment Menu Options***************'
    print '1) Enter 1 to analyze a TaySwift song.'
    print '2) Enter 2 to generate your own TaySwift song.'
    print '3) Enter 3 to exit.'
    
    choice = raw_input('Your choice (1, 2 or 3): ')
    if choice in ['1', '2', '3']:
        return choice
    else:
        print 'Invalid entry! The SenTAYments only except 1, 2 or 3!'
        return '5'
#if user selects option 1, this prompts them to choose which song they want to analyze 
def readTaySong():
    print "Which would you like to analyze?",'\n', "  ", "1) Shake it Off" 
    print "  ", "2) Blank Space", '\n', "  ", "3) You're Not Sorry"
    print "  ", "4) Bad Blood", '\n', "  ", "5) Am I Ready for Love?" 
    print "  ", "6) State of Grace" 
    song = 0
    song = raw_input('Enter 1 through 6 please: ')
    print 
    if song in ['1']:
        title = 'shake_it_off.txt'
    elif song in ['2']:
        title = 'blank_space.txt'
    elif song in ['3']:
        title = "you're_not_sorry.txt"
    elif song in ['4']:
        title = 'bad_blood.txt'
    elif song in ['5']:
        title = 'am_i_ready_for_love.txt'
    elif song in ['6']:
        title = 'state_of_grace.txt'
    else:
        return 'invalid'
    return title   
                
def printBye():
    print 'That is all.'

def readForEmotion(model, song):
     sentimentStr = model.readSentiment(song)
     return sentimentStr

def readMovieForEmotion(model, file):
    sentimentStr = model.readSentiment(file)
    return sentimentStr
    
#generates the sentences in order to create a new song 
def generateSentence(models, length):
    sentence = ["^::^", "^:::^"]
    while not(over(length, len(sentence))) and sentence[-1] != "$:::$" :
        sentence.append(backOff(models, sentence).nextToken(sentence))
    #removes the unwanted beginning and end strings	    
    while '^::^' in sentence:
        sentence.remove('^::^')
    while '^:::^' in sentence:
        sentence.remove('^:::^')
    while '$:::$' in sentence:
        sentence.remove('$:::$')
    #capitalizes the first word
    if len(sentence) > 0:
        sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence)

#selects the best (first) possible model that can be used.
def backOff(models, sentence):

    if models[0].hasKey(sentence) == True:
        return models[0]
    elif models[1].hasKey(sentence) == True:
        return models[1]
    elif models[2].hasKey(sentence) == True:
    	return models[2]
    else:
        return None
        
#returns a boolean of whether or not to end the sentence based solely on length.  
def over(maxLength, currentLength):
    STDEV = 1 
    val = random.gauss(currentLength, STDEV)
    return val > maxLength
    
def populateCommonWords(instance, F):
    F = open(F, 'r')
    words = F.readlines()
    instance.commonWords = words

def populate(unigramSentiment, movieSentiment):
    populateCommonWords(unigramSentiment, 'commonwords.txt')
    populateCommonWords(movieSentiment, 'commonwords.txt')
    
if __name__=='__main__':
    main()
