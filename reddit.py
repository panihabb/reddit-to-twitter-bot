import praw
import requests
import os
from dotenv import load_dotenv


MINIMUM_SCORE = 0
MAX_PHOTO_SIZE = 5242880
MAX_GIF_SIZE = 15728640
MAX_VIDEO_SIZE = 536870912

def check_size(url, max_bytes):
    response = requests.head(url)
    content_length = response.headers.get("Content-Length")
    return content_length and int(content_length) < max_bytes

def reddit_api():
    load_dotenv('config.env')

    reddit = praw.Reddit(
        client_id=os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT'),
        password=os.getenv('REDDIT_PASSWORD'),
        username=os.getenv('REDDIT_USERNAME')
    )
    
    return reddit

def get_submission(reddit_instance):
    found = False
    while not found:
        # The multireddit can be changed here
        subreddit = reddit_instance.multireddit('top_anime_13', 'topanime')
        for submission in subreddit.hot():
            if submission.score < MINIMUM_SCORE or submission.saved or submission.spoiler or submission.over_18:
                continue
            
            if 'v.redd.it' in submission.url:
                if check_size(submission.url, MAX_VIDEO_SIZE):
                    found = True
                    break
                else:
                    # video file size too big, save and skip
                    submission.save()
                    continue

            if submission.url.endswith('.gif'):
                if check_size(submission.url, MAX_GIF_SIZE):
                    found = True
                    break
                else:
                    # gif file size too big, save and skip
                    submission.save()
                    continue

            if submission.url.endswith(('.jpg', '.png', '.jpeg')):
                if check_size(submission.url, MAX_PHOTO_SIZE):
                    found = True
                    break
                else:
                    # image file size too big, save and skip
                    submission.save()
                    continue

            if "/gallery/" in submission.url:
                correct_gallery = False
                for item in sorted(submission.gallery_data['items'], key=lambda x: x['id']):
                    media_id = item['media_id']
                    meta = submission.media_metadata[media_id]
                    if meta['e'] == 'Image':
                        extension = meta['m'].split('/')
                        if len(extension) < 2:
                            continue
                        
                        source = meta['s']
                        if (extension[1] == "jpg" or extension[1] == "png" or extension[1] == "jpeg") and check_size(source['u'], MAX_PHOTO_SIZE):
                            correct_gallery = True
                            break
                
                if correct_gallery:
                    found = True
                    break
                else:
                    submission.save()
                    continue

    if found:
        return submission
    else:
        raise Exception("No submission found")

def get_submission_gallery_filenames(submission):
    filenames = []
    urls = []
    i = 1
    for item in sorted(submission.gallery_data['items'], key=lambda x: x['id']):
        media_id = item['media_id']
        meta = submission.media_metadata[media_id]
        if meta['e'] == 'Image':
            extension = meta['m'].split('/')
            if len(extension) < 2:
                continue

            source = meta['s']
            if (extension[1] == "jpg" or extension[1] == "png" or extension[1] == "jpeg") and check_size(source['u'], MAX_PHOTO_SIZE):
                urls.append(source['u'])
                filename = f"{submission.id}-{i}.{extension[1]}"
                filenames.append(filename)
                i += 1
            
            if i == 5:
                break
    
    return filenames, urls

def get_submission_filename(submission):
    if submission.url.endswith('.jpg'):
        filename = f"{submission.id}.jpg"
    elif submission.url.endswith('.jpeg'):
        filename = f"{submission.id}.jpeg"
    elif submission.url.endswith('.png'):
        filename = f"{submission.id}.png"
    elif submission.url.endswith('.gif'):
        filename = f"{submission.id}.gif"
    elif 'v.redd.it' in submission.url:
        filename = f"{submission.id}.mp4"

    return filename

def get_submission_media_category(submission):
    if "/gallery/" in submission.url or submission.url.endswith(('.jpg', '.png', '.jpeg')):
        media_category = "tweet_image"
    elif submission.url.endswith('.gif'):
        media_category = "tweet_gif"
    elif 'v.redd.it' in submission.url:
        media_category = "tweet_video"

    return media_category

def get_submission_chunked(submission):
    if "/gallery/" in submission.url or submission.url.endswith(('.jpg', '.png', '.jpeg')):
        chunked = False
    elif submission.url.endswith('.gif') or 'v.redd.it' in submission.url:
        chunked = True

    return chunked
