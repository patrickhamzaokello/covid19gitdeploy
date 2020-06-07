import tweepy
import datetime
from textblob import TextBlob
from my_app.twittermodule.tweet_store import TweetStore

import json

consumer_key = '9Cxv5dofHohbaVIVURcZMGBMu'
consumer_secret = 'NaKLbd48avhwO9hDx9i9ADQRMp7ujGnBiTYZSMeGV7utpbHOe8'
access_token = '1425384708-DCb0eNrysG8WC7aHQ1phX7LvGHdr9PWudmmcqug'
access_token_secret = 'ZXqvNhtE5nGipCPDMrp33DDVaq2ZOZITAuTeFYzE3ncsa'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
store = TweetStore()

class StreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if ('RT @' not in status.text):
            blob = TextBlob(status.text)
            sent = blob.sentiment
            polarity = sent.polarity
            subjectivity = sent.subjectivity

            tweet_item = {
                'id_str': status.id_str,
                'text': status.text,
                'polarity': polarity,
                'subjectivity': subjectivity,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                'received_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            store.push(tweet_item)
            print("Pushed to redis:", tweet_item)

    def on_error(self, status_code):
        if status_code == 420:
            return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=["@newvisionwire", "@UVRIug", "@MinofHealthUG", "#StaySafeUg", "@ntvuganda", "@JaneRuth_Aceng","@KagutaMuseveni"])
