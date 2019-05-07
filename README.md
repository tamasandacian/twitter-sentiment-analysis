# Twitter Sentiment Analysis using FastText, Elasticsearch, Kibana

This project contains all the code necessary to reproduce Twitter sentiment prediction using FastText library. 

In this project we employ an open source twitter dataset collection containing 1.6 mil tweets (see https://www.kaggle.com/kazanova/sentiment140). This dataset is used for creating a binary classfication model using FastText. 

The output given model predicts newly incoming tweets and index tweet's data with the sentiment score to Elasticsearch for data visualization using Kibana builtin dashboard.

Required libraries:
```
1. install python 3
2. sudo pip3 install tweepy
3. sudo apt-get install python3-numpy
4. sudo apt-get install python3-pandas
5. sudo apt-get install python3-elasticsearch
```

Basic project installation steps:
```
In the root folder twitter-sentiment-analysis clone repositories:

1. FastText:
git clone https://github.com/facebookresearch/fastText.git 
cd fastText
python setup.py install

2. Docker-elk
git clone git@github.com:deviantony/docker-elk.git 
cd docker-elk
sudo docker-compose up

3. To index data to elasticsearch use command:
python3 indexer.py

To stream twitter data provide Twitter user credentials:
twitter_credentials.py

```
