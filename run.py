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
    populate(sentimentModel)
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
                file = readDirectoryName()
            #analyzes and prints the sentiment analysis of the song based off of tweet & review sentiments      
            sentimentModel.trainSentiment(download.tweetData)
            sentimentStr = readForEmotion(sentimentModel, file)
            print sentimentStr, '\n'
            print
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
def readDirectoryName():
    print "input directory: "
    string = raw_input()
    return string 
                
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
