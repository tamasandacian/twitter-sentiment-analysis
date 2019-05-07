from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credentials
import json
import csv
import sys
import time

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_user_timeline_tweets(self, num_tweets):
        tweet_list = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweet_list.append(tweet)
        return tweet_list

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():
    """
    Class to access Twitter API using  twitter user credentials.
    """
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
        auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_secret)
        return auth

##### TWITTER STREAMER #####
class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, fetched_retweets_filename, hashtag_list):
        """
        This method handles Twitter authentication and the connection to Twitter Streaming API
        """
        listener = TwitterListener(fetched_tweets_filename, fetched_retweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        while True:
            try:
                stream = Stream(auth, listener)
                stream.filter(track=hashtag_list, languages = ['en'])
            except:
                continue


class TwitterListener(StreamListener):
    """
    This is a basic listener class that just prints received tweets to stdout
    """

    def __init__(self, fetched_tweets_filename, fetched_retweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.fetched_retweets_filename = fetched_retweets_filename

    def on_data(self, data):
        
        try:
            data = json.loads(data)
            
            #Get tweet json attributes
            created_at = data['created_at']
            id_str = data['id_str']
            text = data['text']

            source = data['source']
            favorite_count = data["favorite_count"]
            retweet_count = data["retweet_count"]
            
            #Get tweet user json attributes
            name = data['user']['name']
            screen_name = data['user']['screen_name']
            user_location = data['user']['location']
            user_profile_image_url = data['user']["profile_image_url"]
            
            #Get retweet json attributes
            #retweeted_status_id_str = data['retweeted_status']['id_str']
            #retweeted_status_quote_count = data['retweeted_status']['quote_count']
            #retweeted_status_reply_count = data['retweeted_status']['reply_count']
            #retweeted_status_retweet_count = data['retweeted_status']['retweet_count']
            #retweeted_status_favorite_count = data['retweeted_status']['favorite_count']

            # If location is not provided then we store empty string in place
            if (user_location == None):
                user_location = ""
            
            # If name is not provided then we store empty string in place
            if (name == None):
                name = ""

            # Store tweet hashtags
            hashtags = []
            for hashtag in data['entities']['hashtags']:
                hashtags.append(hashtag['text'])
          
            # Check if the given tweet contains extended_tweet field
            # If exist then we append the extended tweet to csv file.
            if hasattr(data, 'extended_tweet'):
                extended_tweet = data['extended_tweet']['full_text']
                with open(self.fetched_tweets_filename, 'a', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([created_at, id_str, screen_name, user_profile_image_url, 
                                     user_location, extended_tweet, source, favorite_count, 
                                     retweet_count, hashtags])
            else:
                 # Check if the given tweet does not start with 'RT' at the beggining of the tweet
                 # If it doesn't then append data to tweets.csv file 
                 if not data['text'].startswith('RT'):
                    with open(self.fetched_tweets_filename, 'a', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([created_at, id_str, screen_name, user_profile_image_url, 
                                        user_location, text, source, favorite_count, retweet_count, hashtags])
                 
                 # If tweet text starts at the beginning with 'RT' then append to retweets.csv file
                 elif data['text'].startswith('RT'):
                    with open(self.fetched_retweets_filename, 'a', encoding='utf-8') as rf:
                        writer = csv.writer(rf)
                        writer.writerow([id_str, text])
            
            return True
        except BaseException as e:
            sys.stderr.write("text: " + text + "\n")
            sys.stderr.write("id_str: " + str(id_str) + "\n")
            sys.stderr.write("created_at: " + str(created_at) + "\n")
            sys.stderr.write("user_location: " + str(user_location) + "\n")
            sys.stderr.write("screen_name: " + screen_name + "\n")
            sys.stderr.write("source: " + source + "\n")
            sys.stderr.write("user_profile_image_url: " + user_profile_image_url + "\n")
            sys.stderr.write("favorite_count: " + str(favorite_count) + "\n")
            sys.stderr.write("retweet_count: " + str(retweet_count) + "\n")
            sys.stderr.write("Error on_data: {}\n".format(e))
        
            sys.exit()
            time.sleep(5)
        return True

    def on_error(self, status):
        """
        Method to return False in case rate limit occurs.
        """
        if status == 420:
            sys.stderr.write("Rate limit exceeded\n")
            return False
        else:
            sys.stderr.write("Error {}\n".format(status))
            return True
        

if __name__ == "__main__":

    # Crawling of tweets and retweets on specified hashtag keywords
    hashtag_list = ['Oneplus', 'Google Pixel', 'Galaxy Note', 'Huawei', 'Iphone', 'LG', 'Motorola']
    fetched_tweets_filename = './csv_dumps/tweets.csv'
    fetched_retweets_filename = './csv_dumps/retweets.csv'
    
    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename,fetched_retweets_filename, hashtag_list)

