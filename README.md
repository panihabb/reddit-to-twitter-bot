# reddit-to-twitter-bot

This project is a Python bot that combines the functionality of retrieving images from the Reddit multireddit [topanime](https://www.reddit.com/user/top_anime_13/m/topanime/) created by the user [top_anime_13](https://www.reddit.com/user/top_anime_13) and posting them on a Twitter account. Additionally, it includes a script for managing your Twitter account by deleting tweets based on specific criteria.

## Key Features

- Automated retrieval of images from Reddit.
- Automatic posting to a Twitter account.
- Tweet management based on the number of favorites (likes) and age.

These key features highlight the core functionality of the project, enabling users to effortlessly retrieve content from Reddit and seamlessly publish it on Twitter. Additionally, the project offers flexible tweet management options to ensure that your Twitter account stays up-to-date with your preferences.

## Image Management

The project includes an `images` directory where images downloaded from Reddit are temporarily stored before being posted on Twitter. This directory serves as a temporary cache for media files. After a submission is successfully posted on Twitter, the associated image files are automatically removed from this directory to free up disk space.

This image management system ensures that only relevant and recently posted content is stored locally, preventing unnecessary clutter and conserving storage resources.

Please note that it is essential to maintain adequate disk space to accommodate the images downloaded from Reddit before they are posted on Twitter.

## Project Structure

### 1. `reddit.py`

This module contains functions for interacting with the Reddit API using the `praw` library. It includes the following functions:

- `check_size(url, max_bytes)`: Checks if the content size of a URL is below a specified threshold.
- `reddit_api()`: Sets up the Reddit API connection using information from `config.env`.
- `get_submission(reddit_instance)`: Retrieves a Reddit submission from the "topanime" multireddit based on specified criteria.
- `get_submission_gallery_filenames(submission)`: Retrieves filenames and URLs of images in a gallery submission.
- `get_submission_filename(submission)`: Generates a filename for a Reddit submission based on its URL.
- `get_submission_media_category(submission)`: Determines the media category of a submission (image, GIF, or video).
- `get_submission_chunked(submission)`: Checks if a submission requires chunked media upload.

### 2. `twitter.py`

This module interacts with the Twitter API using the `tweepy` library. It includes the following functions:

- `twitter_api_v1()`: Sets up the Twitter API connection using OAuth 1.0 User Handler with credentials from `config.env`.
- `twitter_api_v2()`: Sets up the Twitter API connection using OAuth 2.0 with credentials from `config.env`.
- `tweet_content(twitter_instance_v1, twitter_instance_v2, message, file_path_list, chunked, media_category)`: Posts content to Twitter, including text, media files, and media category.

### 3. `main.py`

The main script that orchestrates the entire process of fetching Reddit submissions, downloading media files, and posting to Twitter. It also defines hashtags for various subreddits and handles content length restrictions.

### 4. `delete_tweets.py`

This script is used to delete tweets from a Twitter account based on specific criteria. It connects to the Twitter API using the provided API keys and access tokens from `config.env`. The script includes the following functionality:

- `wipe(account_name, favorite_threshold, days)`: Deletes tweets that have fewer favorites (likes) than a specified threshold and are older than a certain number of days.

   - `account_name`: The Twitter username of the account from which tweets will be deleted.
   - `favorite_threshold`: The minimum number of favorites a tweet must have to be retained (tweets with fewer favorites will be deleted).
   - `days`: The number of days after which tweets will be considered for deletion.

This script helps you manage your Twitter account by removing less popular or older tweets. Please note that it may not work with the free version of the Twitter API, as there are limitations on the number of requests and actions you can perform.

## Installation

1. Clone this GitHub repository to your local machine:

   ```bash
   git clone https://github.com/panihabb/reddit-to-twitter-bot.git
   ```

2. Make sure you have Python 3.x installed on your machine.

3. Install the required dependencies by running the following command in the project directory:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure the Twitter and Reddit API keys and credentials in the `config.env` file with your own information.

## Usage

1. Run the `main.py` file to launch the application:
   
   ```bash
   python main.py
   ```

2. The application will retrieve a submission from Reddit, download its content, and publish it on Twitter.

3. You can customize various parameters in the `main.py` and `delete_tweets.py` files to tailor the application to your needs.

## Contributing

Contributions are welcome! If you would like to improve this project, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. Please see the `LICENSE` file for more information.