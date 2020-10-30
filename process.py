#!/usr/bin/env python
#--------------------------------------------------------
# code to process data
#--------------------------------------------------------
import json

def main():
    # tweetsJson = open('tweets_2020-10-22-1317.txt', 'r')
    # for tweet in tweetsJson:
    #     try:
    #         tweetObj = json.loads(tweet)
    #         print(tweetObj['text'], '\n')
    #     except:
    #         print('error')
    #     #     continue
    with open('tweets_NP_2020-10-26.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_NP_2020-10-27.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_NP_2020-10-28.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_NP_2020-10-29.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_US_2020-10-26.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_US_2020-10-27.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_US_2020-10-28.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

    with open('tweets_US_2020-10-29.csv', 'r') as f:
        lines = f.read()
        count = 0
        for char in lines:
            if char == '\n':
                count+=1
        print(count)

if __name__ == '__main__':
    main()