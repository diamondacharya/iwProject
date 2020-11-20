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
from statistics import mean


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
with open('slangCount_nepal.json', 'r') as f:
    slangCount_nepal = json.load(f)
with open('slangCount_us.json', 'r') as f:
    slangCount_us = json.load(f)
with open('commonWordCount_nepal.json', 'r') as f:
    commonWordCount_nepal = json.load(f)
with open('commonWordCount_us.json', 'r') as f:
    commonWordCount_us = json.load(f)

# most common content words from the American data
common_words = ['trump', 'biden', 'election', 'vote', 'president']
# things that didn't go in there -- [people, time, love, day, new, job]

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
def give_frequentWords_fileWise(n, tweetFiles):
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

# gives the n most frequent words from all the us tweet files
def give_frequentWords_all(n):
    l = [] # list to store all the tweets from all us files
    for tweetFile in usTweets:
        with open(tweetFile, 'r') as f:
            reader = csv.DictReader(f, ['timestamp', 'text'], delimiter=',', quotechar='"')
            tokenized = [] # stores tweets for each day's file
            for row in reader:
                textLower = row['text'].lower()
                tokens = word_tokenize(textLower)
                tokenized = tokenized + tokens
            filtered = filter_text(tokenized)
            f.close()
        l = l + filtered
    calculate_wordFreq(l, n)


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

# takes in a list 'l' of tweet files, and the country name. Then, prints to a json file a
# dictionary containing the common word name as key and the corresponding tweet count for each day
def print_commonWordCount(l, countryName):
    countDict = {} # dictionary to store word names as keys and a list of count as values
    # for each word in common_words
    for word in common_words:
        countList = []
        # for each day of tweets
        for tweetFile in l:
            with open(tweetFile, 'r') as f:
                reader = csv.DictReader(f, ['timestamp', 'text'], delimiter=',', quotechar='"')
                count = 0
                for row in reader:
                    textLower = row['text'].lower()
                    if (word in textLower):
                        count+= 1
                countList.append(count)
                f.close()
        countDict[word] = countList
    jsonDict = json.dumps(countDict)
    with open(f'commonWordCount_{countryName}.json', 'w') as f:
        f.write(jsonDict)


# calculates and plots the proportion of tweets containing the slangs for each decade (for US vs Nepal)
# also prints outs the average in each iteration
def plotSlangs_byDecade():
    for decade in slangs.keys():
        percentageList_us = [round(100 * (item1 / item2), 2) for item1, item2 in zip(slangCount_us[decade], tweetCount_us)]
        percentageList_nepal = [round(100 * (item1 / item2), 2) for item1, item2 in zip(slangCount_nepal[decade], tweetCount_nepal)]
        f = plt.figure()
        plt.xticks([0, 5, 10, 15, 20], ['oct 26', 'oct 31', 'nov 5', 'nov 10', 'nov 15', 'nov 20'])
        plt.xlabel('time')
        title = '19' + decade if decade[0] in ['6', '7', '8', '9'] else '20' + decade
        plt.title(title)
        plt.ylabel("% of tweets containing the slangs")
        axes = plt.gca()
        axes.set_ylim([0, 1])
        plt.plot(percentageList_us, label='us')
        plt.plot(percentageList_nepal, label='nepal')
        plt.legend(loc='upper right')
        plt.savefig(f'plots/slangs_{decade}.jpeg')
        f.clear()
        plt.close(f)
        print(f'{decade} -- nepal mean -- {round(mean(percentageList_nepal), 2)}')
        print(f'{decade} -- us mean -- {round(mean(percentageList_us), 2)}')

# calculates and plots the proportion of tweets containing the given common word (from common_words)
#  (for US vs Nepal). Does this for all the common words. Also prints outs the average in each iteration
def plotCommonWords():
    for word in common_words:
        percentageList_us = [round(100 * (item1 / item2), 2) for item1, item2 in zip(commonWordCount_us[word], tweetCount_us)]
        percentageList_nepal = [round(100 * (item1 / item2), 2) for item1, item2 in zip(commonWordCount_nepal[word], tweetCount_nepal)]
        f = plt.figure()
        plt.xticks([0, 5, 10, 15, 20], ['oct 26', 'oct 31', 'nov 5', 'nov 10', 'nov 15', 'nov 20'])
        plt.xlabel('time')
        title = word
        plt.title(title)
        plt.ylabel(f"% of tweets containing '{word}'")
        axes = plt.gca()
        axes.set_ylim([0, 16])
        plt.plot(percentageList_us, label='us', color='red')
        plt.plot(percentageList_nepal, label='nepal', color='green')
        plt.legend(loc='upper right')
        plt.savefig(f'plots/commonWords_{word}.jpeg')
        f.clear()
        plt.close(f)
        print(f'{word} -- nepal mean -- {round(mean(percentageList_nepal), 2)}')
        print(f'{word} -- us mean -- {round(mean(percentageList_us), 2)}')

# calculates, prints, and plots the proportion of tweets containing all the common words combined
# also prints the mean
def plotCommonWords_all():
    dayLength = len(commonWordCount_nepal['trump'])
    percentageList_us = []
    percentageList_nepal = []
    for i in range(dayLength):
        sum = 0
        for word in common_words:
            sum += commonWordCount_nepal[word][i]
        percent = round(100 * (sum / tweetCount_nepal[i]), 2)
        percentageList_nepal.append(percent)
        sum2 = 0
        for word in common_words:
            sum2 += commonWordCount_us[word][i]
        percent2 = round(100 * (sum2 / tweetCount_us[i]), 2)
        percentageList_us.append(percent2)
    print(percentageList_nepal)
    print(percentageList_us)
    plt.xticks([0, 5, 10, 15, 20], ['Oct 26', 'Oct 31', 'Nov 5', 'Nov 10', 'Nov 15', 'Nov 20'])
    plt.xlabel('Time')
    title = 'All Election words'
    plt.title(title)
    plt.ylabel("% of tweets containing all election words")
    axes = plt.gca()
    axes.set_ylim([0, 50])
    plt.plot(percentageList_us, label='us', color='red')
    plt.plot(percentageList_nepal, label='nepal', color='green')
    plt.legend(loc='upper right')
    plt.savefig(f'plots/commonWords_all.jpeg')
    print(f'nepal mean -- {round(mean(percentageList_nepal), 2)}')
    print(f'us mean -- {round(mean(percentageList_us), 2)}')

# calculates, prints, and plots the proportion of tweets containing all the slangs combined
# also prints the mean
def plotSlangs_all():
    dayLength = len(slangCount_nepal['60s'])
    percentageList_us = []
    percentageList_nepal = []
    for i in range(dayLength):
        sum = 0
        for decade in slangCount_nepal.keys():
            sum += slangCount_nepal[decade][i]
        percent = round(100 * (sum / tweetCount_nepal[i]), 2)
        percentageList_nepal.append(percent)
        sum2 = 0
        for decade in slangCount_us.keys():
            sum2 += slangCount_us[decade][i]
        percent2 = round(100 * (sum2 / tweetCount_us[i]), 2)
        percentageList_us.append(percent2)
    print(percentageList_nepal)
    print(percentageList_us)
    plt.xticks([0, 5, 10, 15, 20], ['Oct 26', 'Oct 31', 'Nov 5', 'Nov 10', 'Nov 15', 'Nov 20'])
    plt.xlabel('Time')
    title = 'All Slangs'
    plt.title(title)
    plt.ylabel("% of tweets containing the slangs")
    axes = plt.gca()
    axes.set_ylim([0, 1.2])
    plt.plot(percentageList_us, label='us')
    plt.plot(percentageList_nepal, label='nepal')
    plt.legend(loc='upper right')
    plt.savefig(f'plots/slangs_all.jpeg')
    print(f'nepal mean -- {round(mean(percentageList_nepal), 2)}')
    print(f'us mean -- {round(mean(percentageList_us), 2)}')

# main method
def main():
    # print_tweetCount(usTweets, 'us')
    # give_frequentWords_all(100)
    # print_slangCount(usTweets, 'us')
    # print_commonWordCount(usTweets, 'us')
    # plotSlangs_byDecade()
    plotSlangs_all()
    # with open('tweetCount_nepal.json', 'r') as f:
    #     jsonObj = json.load(f)
    # print(mean(tweetCount_nepal))
    # print(mean(tweetCount_us))
    # print(commonWordCount_nepal)
    # print(commonWordCount_us)
    # plotCommonWords()
    # plotCommonWords_all()



if __name__ == '__main__':
    main()