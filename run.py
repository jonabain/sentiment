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
    SOURCEDIRECTORY = ["Tweets"]
    for dir in SOURCEDIRECTORY:
        download = DataLoader()
        download.loadTweets(dir)
    print "* All Twitter Sentiments Have Been Loaded. *", '\n'
    
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
        #quits program if user selects option 3   
        elif choice in ['2']:
            printBye()
            done = True
        else:
            junk = 'do stuff'
            done = False
            
def welcomeMessage():
    print 'Welcome.'
    
def printMenu():
    print '\n', '***************Menu Options***************'
    print '1) Enter 1 to analyze a directory.'
    print '2) Enter 2 to exit.'
    
    choice = raw_input('Your choice (1, or 2): ')
    if choice in ['1', '2']:
        return choice
    else:
        print 'Invalid entry! Only except 1 or 2.'
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
    
def populateCommonWords(instance, F):
    F = open(F, 'r')
    words = F.readlines()
    instance.commonWords = words

def populate(unigramSentiment):
    populateCommonWords(unigramSentiment, 'commonwords.txt')
    
if __name__=='__main__':
    main()
