import tweepy
import os
from dotenv import load_dotenv

load_dotenv('config.env')

# Clés Twitter
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

def twitter_api_v1():
    auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def twitter_api_v2():
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_SECRET
    )
    return client

def tweet_content(twitter_instance_v1, twitter_instance_v2, message, file_path_list, chunked, media_category):
    media_ids = []
    for file_path in file_path_list:
        temp = twitter_instance_v1.media_upload(filename=file_path, chunked=chunked, media_category=media_category)
        media_ids.append(temp.media_id)

    twitter_instance_v2.create_tweet(text=message, media_ids=media_ids)