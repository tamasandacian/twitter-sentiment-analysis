import pandas as pd
import numpy as np
import fastText
import time
import datetime, pytz
import csv
import sys

from elasticsearch import Elasticsearch
 
MODEL_FILE = './model_sentiment.bin'
su_model = fastText.load_model(MODEL_FILE)
es = Elasticsearch()

class Analyzer():
    """
    Class to predict tweet's sentiment and index to Elasticsearch.
    """
    def getTweets(self, input_file_tweets):

       with open(input_file_tweets, 'rU') as file:
           # replace of newline '\n' character with empty string in the csv file
           filtered = (line.replace('\n', '') for line in file)
           # reading of data line by line and index to elasticsearch
           for row in csv.reader(filtered):
                 try:
                      if (len(row) > 1):
                         date = row[0]
                         id_str = row[1]
                         screen_name = row[2]
                         user_profile_image_url = row[3]
                         user_location = row[4]
                         text = row[5]
                         source_url = row[6]
                         favorite_count = row[7]
                         retweet_count = row[8]
                         hashtags = row[9]

                         sentiment, probability = self.predict(text)
                         created_at = self.date_to_datetime(date)
                        
                         # index tweet data and sentiment information to elasticsearch
                         es.index(index="twitter_sentiment_analysis",
                                 doc_type="test-type",
                                 body={
                                'author': screen_name,
                                'created_at': created_at,
                                'id_str': id_str,
                                'tweet_text': text,
                                'source_url': source_url,
                                'user_location': user_location,
                                'user_profile_image_url' : user_profile_image_url,
                                'favorite_count': favorite_count,
                                'retweet_count': retweet_count,
                                'sentiment': sentiment,
                                'probability': probability,
                                'hashtag': hashtags
                                })

                      else:
                         continue
                
                 except Exception as e:
                     print(e)
                     break
           return True

    def predict(self, tweet_text):
        """
        Method to predict sentiment analysis using Supervised Learning method.
        """
        prediction, percent = su_model.predict(tweet_text)
        fasttext_label = prediction[0]
        sentiment = fasttext_label[-1]
        probability = percent[0]
        return sentiment, probability 

    def date_to_datetime(self, date):
        """
        Method to convert string date to datetime object.
        """
        datetime_obj = datetime.datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
        return datetime_obj
        

if __name__ == '__main__':
    print("***************** START INDEXING DATA TO ELASTICSEARCH FROM CSV *********************")
    input_file_tweets = './csv_dumps/tweets.csv'
    
    analyzer = Analyzer()
    analyzer.getTweets(input_file_tweets)
    print("************ FINISHED INDEXING DATA TO ELASTICSEARCH! ***********")
