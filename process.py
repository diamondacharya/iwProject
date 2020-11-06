#!/usr/bin/env python
#--------------------------------------------------------
# code to process data
#--------------------------------------------------------
import json
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
from collections import Counter

nepaliTweets = ['tweets_NP_2020-10-26.csv', 'tweets_NP_2020-10-27.csv', 'tweets_NP_2020-10-28.csv',
                'tweets_NP_2020-10-29.csv', 'tweets_NP_2020-10-30.csv', 'tweets_NP_2020-10-31.csv',
                'tweets_NP_2020-11-01.csv', 'tweets_NP_2020-11-02.csv', 'tweets_NP_2020-11-03.csv',
                'tweets_NP_2020-11-04.csv']

usTweets = ['tweets_US_2020-10-26.csv', 'tweets_US_2020-10-27.csv', 'tweets_US_2020-10-28.csv',
            'tweets_US_2020-10-29.csv', 'tweets_US_2020-10-30.csv', 'tweets_US_2020-10-31.csv',
            'tweets_US_2020-11-01.csv', 'tweets_US_2020-11-02.csv', 'tweets_US_2020-11-03.csv',
            'tweets_US_2020-11-04.csv']

eng_stopwords = list(stopwords.words('english'))
punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', '.', '/', ':', ';', '<',
                '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', ',', '’',
                "''", "“", "”"]
function_words = ['i', 'we', 'us', 'a', 'an', 'the']
others = ['http', 'https', "'s", '``', "n't", 'amp', '...']
stopwords = eng_stopwords + punctuation + function_words + others

# takes in a list 'l' of tweet files and prints the no. of tweets in each one of those files
def print_tweetNo(l):
    for i in range(len(l)):
        with open(l[i], 'r') as f:
            tweets = f.read().splitlines()
            print(l[i], ' -- ', len(tweets))

# removes all the stop words from the tokenized list 'l' and returns the filtered list
def filter_text(l):
    ret_list = [item for item in l if not item in stopwords]
    return ret_list

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


def main():
    # print_tweetNo(nepaliTweets)
    # print_tweetNo(usTweets)
    give_frequentWords(10, usTweets)


if __name__ == '__main__':
    main()