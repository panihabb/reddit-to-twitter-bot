import os
import urllib.request
from twitter import tweet_content, twitter_api_v1, twitter_api_v2
from reddit import get_submission, get_submission_gallery_filenames, get_submission_filename, get_submission_chunked, get_submission_media_category, reddit_api

TWEET_MAX_LENGTH = 280
CURRENT_DIR = os.getcwd()
IMAGES_PATH = os.path.join(CURRENT_DIR, "images")
DICT_HASHTAGS = {
  "anime": "#anime #manga",
  "anime_irl": "#anime #manga",
  "animegifs": "#anime #manga",
  "animememes": "#Memes #anime #manga",
  "attackontitan": "#SNK #ShingekiNoKyojin #AoT #AttackOnTitan",
  "Berserk": "#Berserk",
  "bleach": "#BLEACH",
  "BlueLock": "#bluelock",
  "BokuNoHeroAcademia": "#BokuNoHeroAcademia #MyHeroAcadamia #mha",
  "BokuNoMetaAcademia": "#Memes #BokuNoHeroAcademia #MyHeroAcadamia #mha",
  "Boruto": "#BorutoNarutonextgenerations #BORUTO #NARUTO #NarutoShippuden",
  "ChainsawMan": "#chainsawman",
  "dankruto": "#Memes #NARUTO #NarutoShippuden",
  "dbz": "#DBZ #DragonBall #DragonBallZ #DragonBallGT #DragonBallSuper",
  "deathnote": "#DeathNote",
  "Dragonballsuper": "#DBZ #DragonBall #DragonBallZ #DragonBallGT #DragonBallSuper",
  "DrStone": "#DrSTONE",
  "fairytail": "#FairyTail",
  "FullmetalAlchemist": "#fma #FullmetalAlchemist #fmab #FullmetalAlchemistBrotherhood",
  "GoldenKamuy": "#goldenkamuy",
  "Grapplerbaki": "#baki",
  "hajimenoippo": "#hajimenoippo",
  "HunterXHunter": "#hxh #HunterXHunter",
  "JuJutsuKaisen": "#JJK #JujutsuKaisen",
  "KimetsuNoYaiba": "#DemonSlayer #kimetsunoyaiba",
  "Kingdom": "#Kingdom",
  "MemePiece": "#Memes #ONEPIECE",
  "Naruto": "#NARUTO #NarutoShippuden",
  "Ningen": "#Memes #DBZ #DragonBall #DragonBallZ #DragonBallGT #DragonBallSuper",
  "OnePiece": "#ONEPIECE",
  "OnePunchMan": "#OnePunchMan",
  "Re_Zero": "#rezero",
  "ShingekiNoKyojin": "#SNK #ShingekiNoKyojin #AoT #AttackOnTitan",
  "ShitPostCrusaders": "#Memes #JJBA #JOJOsBizzareAdventure #stardustcrusaders #goldenwind #StoneOcean",
  "sololeveling": "#sololeveling",
  "StardustCrusaders": "#JJBA #JOJOsBizzareAdventure #stardustcrusaders #goldenwind #StoneOcean",
  "TokyoRevengers": "#TokyoRevengers",
  "VinlandSaga": "#VinlandSaga #VINLAND_SAGA",
  "yugioh": "#yugioh",
  "YuYuHakusho": "#YuYuHakusho",
}

def download_content(urls, file_path_list):
    for url, file_path in zip(urls, file_path_list):
        urllib.request.urlretrieve(url, file_path)

def delete_all_files():
    for filename in os.listdir(IMAGES_PATH):
        if filename == "placeholder.txt":
            continue
        f = os.path.join(IMAGES_PATH, filename)
        os.remove(f)

def create_title(submission):
    subreddit_name = str(submission.subreddit)
    hashtag = DICT_HASHTAGS.get(subreddit_name, "#anime #manga")
    credits = "📸: " + submission.shortlink
    end_message = f"{hashtag}\n\n{credits}"

    total_length = len(submission.title + " " + end_message)
    if total_length <= TWEET_MAX_LENGTH:
        res = submission.title + " " + end_message
    else:
        diff = total_length - TWEET_MAX_LENGTH
        res = submission.title[: len(submission.title) - 3 - diff] + "... " + end_message

    return res

if __name__ == "__main__":
    success = False
    iteration = 0
    reddit_instance = reddit_api()
    twitter_instance_v1 = twitter_api_v1()
    twitter_instance_v2 = twitter_api_v2()
    while not success and iteration < 3:
        iteration += 1
        try:
            submission = get_submission(reddit_instance)
            file_path_list = []
            urls = []

            if "/gallery/" in submission.url:
                gallery = get_submission_gallery_filenames(submission)
                filenames, urls = gallery
                file_path_list = [os.path.join(IMAGES_PATH, filename) for filename in filenames]
            elif "v.redd.it" in submission.url:
                urls = [
                    "https://sd.redditsave.com/download.php?permalink=https://reddit.com/"
                    + submission.permalink
                    + "&video_url="
                    + submission.media["reddit_video"]["fallback_url"]
                    + "&audio_url=false"
                ]
                file_path_list = [os.path.join(IMAGES_PATH, get_submission_filename(submission))]
            else:
                urls = [submission.url]
                file_path_list = [os.path.join(IMAGES_PATH, get_submission_filename(submission))]

            download_content(urls, file_path_list)
            tweet_content(
                twitter_instance_v1,
                twitter_instance_v2,
                create_title(submission),
                file_path_list,
                get_submission_chunked(submission),
                get_submission_media_category(submission),
            )
            delete_all_files()
            submission.save()
            success = True
        except Exception as e:
            print(str(e))
            delete_all_files()
            submission.save()