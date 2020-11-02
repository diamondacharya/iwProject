#!/usr/bin/env python
#--------------------------------------------------------
# code to stream location-based tweets with the Streaming API
#--------------------------------------------------------
import time
import tweepy
import json
import keys # local
import nepalTracker # local
import re
import csv

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, us_count):
        self.us_count = us_count

    def on_connect(self):
        print('Connection to the server established!')

    def handle_messages(self, message):
        if 'limit' in message: # present for a limit notice
            print(f"Limit message at {time.strftime('%H:%M %p')}: {message}")
        elif 'disconnect' in message: # present for a disconnect notice
            print(f"Disconnect message at {time.strftime('%H:%M %p')}: {message}")

    def on_data(self, raw_data):
        tweet = json.loads(raw_data)
        self.handle_messages(tweet) # catches non-tweet messages like disconnection notices
        try:
            created_at = tweet['created_at']
            text = tweet['text']
            user_id_str = tweet['user']['id_str'] # user id string
            followers_count = tweet['user']['followers_count'] # no. of followers of the user
            user_location = tweet['user']['location'] # profile location
            user_description = tweet['user']['description'] # profile bio
            lang = tweet['lang']
            reply = tweet['in_reply_to_status_id']
        except KeyError as error:
            print(error, '\n', raw_data)
            return True # just continue with another round in this case

        matcher = '.*[nN][eE][pP][aA][lL].*' # regex matcher


        if 'extended_tweet' in tweet: # get the full text
            text = tweet['extended_tweet']['full_text']
        # if it's a quote tweet, append the original tweet with the quote tweet
        if 'quoted_status' in tweet:
            quote_text = tweet['quoted_status']['text']
            if 'extended_tweet' in tweet['quoted_status']:
                quote_text = tweet['quoted_status']['extended_tweet']['full_text']
            text = text + quote_text
        # get the full text if it's a retweet
        if 'retweeted_status' in tweet:
            # text = tweet['retweeted_status']['extended_tweet']['full_text']
            text = tweet['retweeted_status']['text']
            if 'extended_tweet' in tweet['retweeted_status']:
                text = tweet['retweeted_status']['extended_tweet']['full_text']

        if lang != 'en':  # only getting English-lang tweets (can possibly include transliterations)
            return True

        # make separate files for two locations by the day. Only store timestamp & text
        # only include tweets from US and Nepal
        if tweet['place'] != None:
            place_country_code = tweet['place']['country_code'] # every geotagged tweet has this
            if reply != None and place_country_code == 'US': # don't store replies from the US
                return True
            if place_country_code == 'US': # get only 1 out of 50 US tweets received
                self.us_count += 1
                if self.us_count % 50 != 0:
                    return True
            if place_country_code == 'NP' and followers_count > 100: # store the user's id
                with open('nepaliUsers.txt', 'a') as f:
                    f.write(user_id_str)
                    f.write('\n')

            if place_country_code in ['US', 'NP']:
                fh = open('tweets_%s_%s.csv' % (place_country_code, time.strftime('%Y-%m-%d')), 'a')
                writer = csv.writer(fh, delimiter=',', quotechar='"')
                writer.writerow([created_at, text])
                fh.close()
                return True

        # if there is mention of matcher in profile location, we take that tweet into the Nepal file
        if user_location != None and re.search(matcher, user_location):
            fh = open('tweets_%s_%s.csv' % ('NP', time.strftime('%Y-%m-%d')), 'a')
            writer = csv.writer(fh, delimiter=',', quotechar='"')
            writer.writerow([created_at, text])
            fh.close()
            if followers_count > 100: # store user id
                with open('nepaliUsers.txt', 'a') as f:
                    f.write(user_id_str)
                    f.write('\n')
            return True
        # if there is mention of matcher in profile bio, we take that tweet into the Nepal file
        if user_description != None and re.search(matcher, user_description):
            fh = open('tweets_%s_%s.csv' % ('NP', time.strftime('%Y-%m-%d')), 'a')
            writer = csv.writer(fh, delimiter=',', quotechar='"')
            writer.writerow([created_at, text])
            fh.close()
            if followers_count > 100: # store user id
                with open('nepaliUsers.txt', 'a') as f:
                    f.write(user_id_str)
                    f.write('\n')
            return True

        return True # ensures stream keeps on

    def on_error(self, status_code):
        if status_code == 420:
            print('Got error 420!')
            return False # disconnect the stream in this case


def main():
    auth = tweepy.OAuthHandler(keys.C_KEY, keys.C_SEC)
    auth.set_access_token(keys.AT, keys.AT_SEC)

    api = tweepy.API(auth, wait_on_rate_limit=True) # handles rate limiting

    myStreamListener = MyStreamListener(0)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # location in the order southwest and northeast, longitude and latitude
    myLocations = [-126.306381, 25.430873, -66.540756, 49.344809,   # Contiguous US
                    79.978834, 26.363573, 88.263044, 30.572903]     # Nepal

    myStream.filter(track=nepalTracker.words, locations=myLocations) # they don't filter each other


if __name__ == '__main__':
    main()