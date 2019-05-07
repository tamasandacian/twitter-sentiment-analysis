# Create FastText model using from raw train data

import fastText

TRAIN_FILE = './datasets/raw_data/tweets.train'
su_model = fastText.train_supervised(input=TRAIN_FILE, wordNgrams=3)
su_model.save_model('model_sentiment.bin')