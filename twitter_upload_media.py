import urllib.request
import tweepy
import credentials

def get_picture(url, full_path):
    urllib.request.urlretrieve(url, full_path)

def twitter_api():
    consumer_key = credentials.consumer_key
    consumer_secret = credentials.consumer_secret
    access_token = credentials.access_token
    access_token_secret = credentials.access_token_secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    
    return api
