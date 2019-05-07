# FastText model evaluation and prediction on raw test data

import fastText

VALID_FILE = './datasets/raw_data/tweets.valid'
FT_MODEL_FILE = './model_sentiment.bin'

su_model = fastText.load_model(FT_MODEL_FILE)
numOfTweets, precision, recall = su_model.test(VALID_FILE)
print("N\t" + str(numOfTweets))
print("P@{}\t{:.3f}".format(5, precision))
print("R@{}\t{:.3f}".format(5, recall))

sentence_positive1 = "Maybe I'm mad but I'm now the proud owner of a potentially #bendy #iphone6, it's so much bigger than #4s"
prediction, probability = su_model.predict(sentence_positive1)
print ('sentence: ' + sentence_positive1)
print('prediction: ' + str(prediction))
print('probability: ' + str(probability))

sentence_positive2 = "Looks like a great combination! :)"
prediction, probability = su_model.predict(sentence_positive2)
print ('sentence: ' + sentence_positive2)
print('prediction: ' + str(prediction))
print('probability: ' + str(probability))

sentence_negative1 = "I'm not sure I want it. It's too big to fit in my back pocket! lol #iphone6"
prediction, probability = su_model.predict(sentence_negative1)
print ('sentence: ' + sentence_negative1)
print('prediction: ' + str(prediction))
print('probability: ' + str(probability))

sentence_negative2 = "I'm really dissapointed with the #iphone6. It took them 2 years to change the screen & size. Let down"
prediction, probability = su_model.predict(sentence_negative2)
print ('sentence:' + sentence_negative2)
print('prediction:' + str(prediction))
print('probability:' + str(probability))
