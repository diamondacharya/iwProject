#!/usr/bin/env python
#--------------------------------------------------------
# code to process data
#--------------------------------------------------------
import json
import os
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from collections import Counter
from tweetLists import nepaliTweets
from tweetLists import usTweets
from slangs import slangs
import plotly.express as px
import matplotlib.pyplot as plt


# compiling the stopwords
eng_stopwords = list(stopwords.words('english'))
punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', '/', ':', ';', '<',
                '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ',', '’',
                "''", "“", "”"]
function_words = ['i', 'we', 'us', 'a', 'an', 'the']
others = ['http', 'https', "'s", '``', "n't", 'amp', '...']
stopwords = eng_stopwords + punctuation + function_words + others

# extracting constants counts
with open('tweetCount_nepal.json', 'r') as f:
    tweetCount_nepal = json.load(f)
with open('tweetCount_us.json', 'r') as f:
    tweetCount_us = json.load(f)

# helper for give_frequentWords
# removes all the stop words from the tokenized list 'l' and returns the filtered list
def filter_text(l):
    ret_list = [item for item in l if not item in stopwords]
    return ret_list

# helper for give_frequentWords
# takes in a list of words 'l' and prints the n most common words with their frequencies
def calculate_wordFreq(l, n):
    counter = Counter(l)
    most_occur = counter.most_common(n)
    # print(most_occur)
    for item in most_occur:
        print(item[0], '\n')

# does all the data processing in the list of tweet files 'tweetFiles' and gives the 'n' most
# frequent words in each file
def give_frequentWords(n, tweetFiles):
    for tweetFile in tweetFiles:
        print(tweetFile, '\n')
        with open(tweetFile, 'r') as f:
            reader = csv.DictReader(f, ['timestamp', 'text'])
            l = [] # list of words in the file (bag of words)
            for row in reader:
                tokenized = word_tokenize(row['text'])
                l = l + tokenized
            lowered = [word.lower() for word in l]
            filtered = filter_text(lowered)
        calculate_wordFreq(filtered, n)
        print(80 * '-')

# takes in a list 'l' of tweet files and the country name and prints the no. of tweets in a new file
def print_tweetCount(l, countryName):
    counts = []
    for i in range(len(l)):
        fh = open(l[i], 'r')
        fileObj = csv.reader(fh, delimiter=',', quotechar='"')
        tweetCount = sum(1 for row in fileObj)
        counts.append(tweetCount)
    countsJson = json.dumps(counts)
    with open(f'tweetCount_{countryName}.json', 'w') as writeFile:
        writeFile.write(countsJson)

# takes in a list 'l' of tweet files, and the country name. Then, prints to a json file a
# dictionary containing the decade name as the key and the slang counts for each day
def print_slangCount(l, countryName):
    countDict = {} # dict with decade names as keys and a list of slang count for all days as values
    decades = slangs.keys()
    # for each decade
    for decade in decades:
        countList = [] # list to track slang counts for each day (for slangs from this decade)
        # for each day of tweets
        for tweetFile in l:
            with open(tweetFile, 'r') as f:
                reader = csv.DictReader(f, ['timestamp', 'text'], delimiter=',', quotechar='"')
                count = 0
                for row in reader:
                    textLower = row['text'].lower()
                    if (any(slang in textLower for slang in slangs[decade])):
                        count+=1
                countList.append(count)
                f.close()
        countDict[decade] = countList
    jsonDict = json.dumps(countDict)
    with open(f'slangCount_{countryName}.json', 'w') as f:
        f.write(jsonDict)

def plotSlangs_byDecade():
    plt.plot([1, 2, 3])
    plt.savefig('plots/test.jpeg')


def main():
    # print_tweetCount(usTweets, 'us')
    # give_frequentWords(10, usTweets)
    # print_slangCount(usTweets, 'us')
    # with open('tweetCount_nepal.json', 'r') as f:
    #     jsonObj = json.load(f)



if __name__ == '__main__':
    main()