#!/usr/bin/env python
#--------------------------------------------------------
# code to process data
#--------------------------------------------------------
import json

def main():
    tweetsJson = open('tweets_2020-10-22-1317.txt', 'r')
    for tweet in tweetsJson:
        try:
            tweetObj = json.loads(tweet)
            print(tweetObj['text'], '\n')
        except:
            print('error')
        #     continue
    # with open('tweets_20201022-1228.json') as f:
    #     myfile = json.load(f)
    #     print(myfile)


if __name__ == '__main__':
    main()