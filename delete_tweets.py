# -*- coding: utf-8 -*-

""" Deletes all tweets below a certain retweet threshold.
"""

import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv('config.env')

# Constants
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')
TWITTER_USER_NAME = os.getenv('TWITTER_USER_NAME')

# Connect To Your Twitter Account via Twitter API
auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)

api = tweepy.API(auth,
                 wait_on_rate_limit=True,
                 retry_count=3,
                 retry_delay=5,
                 retry_errors=set([401, 404, 500, 503]))

# For the account name
def wipe(account_name=TWITTER_USER_NAME, favorite_threshold=100, days=62):
    # Get the current datetime
    current_date = datetime.utcnow().date()
    
    # For each tweet
    for status in tweepy.Cursor(api.user_timeline, screen_name='@'+account_name).items():
        # Get the tweet id
        status_id = status._json['id']

        print(datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"), 'Examining', status_id)

        # Get the number of favorites
        status_favorites = status._json['favorite_count']

        # Get the datetime of the tweet
        status_date = datetime.strptime(status._json['created_at'], '%a %b %d %H:%M:%S +0000 %Y').date()
        
        # If the difference between the current datetime and the tweet's
        # is more than a day threshold
        if (current_date - status_date).days >= days:
            # If the number of favorites is lower than the favorite threshold
            if status_favorites < favorite_threshold:
                # Delete the tweet
                api.destroy_status(status_id)
                print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Deleting', status_id)

# Run main function
if __name__ == '__main__':
    wipe(account_name=TWITTER_USER_NAME, favorite_threshold=2, days=1)