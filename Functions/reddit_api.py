import json
import os
import praw
from redvid import Downloader
import logging
from random import randint
from Functions import pushover

# setting up logger, paste this at beginning on each file
logging.basicConfig(encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
# file output settings
file_handler = logging.FileHandler('../log.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # level for file output in this file
file_handler.setFormatter(formatter)
# console output settings
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.DEBUG)  # level for console output in this file
# adding console and file outputs to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)  # remove this to remove console output for this file
# checking that logger works
logger.debug('Imported')



username = '' # your reddit username
client_id = '' # your reddit client id
client_secret = '' # your reddit client secret
password = '' # your reddit password

replied_to = [] # list of comment ids that have been replied to

#creates reddit instance for given user
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    username=username,
    password=password,
    user_agent=''
)


# checks if the api is connected to the selected user
def check_login():
    try:
        logger.info(f' API connected to user: {reddit.user.me()}')
    except:
        logger.exception('Reddit Authentication Failed:')
        pushover.send_notification(f'Failed to auth into reddit')





# downloads video from post ID, using Redvid
def download_video(post_id, file_name, target_directory):
    submission = reddit.submission(post_id)
    logger.debug(f' Attempting to download video from post: {submission.title} ')
    try:
        if submission.is_video:
            video = Downloader(max_q=True, path=target_directory, filename=file_name)
            video.url = submission.url
            video.download()
            logger.debug(f' Video from post "{submission.title}" saved to {target_directory}')
            return True
        else:
            logger.error(' post does not contain video')
            return False
    except Exception as e:
        logger.error(f'Failed to download video {e}')
        return False


# should select videos totalling x duration randomly from the hot posts of the given subreddits
current_directory = os.path.dirname(os.path.abspath(__file__))
temp_storage = os.path.join(current_directory, '../temp_clip_storage')
output_storage = os.path.join(current_directory, '../output_storage')


def download_reddit_videos( subreddit_list, target_directory = temp_storage, total_duration=600, max_vod_lenght = 15 ):
    # takes the list of target subreddits from the json
    current_dir = os.path.dirname(__file__)
    subreddit_list_path = os.path.join(current_dir, '../json_files/subreddit_lists.json')
    with open(subreddit_list_path, "r") as my_file:
        data = json.load(my_file)
        subreddit_list = data[subreddit_list]
    logger.debug(f'subreddit list created: {subreddit_list}')
    current_duration = 0
    post_id_dict = {}
    for subreddit in subreddit_list:
        logger.debug(f' checking posts of {subreddit} for suitable videos')
        subreddit = reddit.subreddit(subreddit)
        for submission in subreddit.top("day", limit=100):
            if submission.is_video and submission.media["reddit_video"]["duration"] <= max_vod_lenght and not submission.over_18:
                post_id_dict[submission.id]=submission.media["reddit_video"]["duration"]
                logger.debug(f'post "{submission.title}" in "{submission.subreddit.display_name}" added to list of '
                             f'suitable videos',)
    total_download_lenght = 0
    id_list = list(post_id_dict.keys())
    videos_downloaded = 0
    logger.info(f'list of post IDs: {id_list}')
    logger.info('starting to download videos from reddit')
    while total_download_lenght <= total_duration:
        videos_downloaded += 1
        random_post_id = id_list[randint(0, (len(id_list)-1))]
        origin_subreddit = reddit.submission(id=random_post_id)
        subreddit_name = origin_subreddit.subreddit.display_name
        downloaded = download_video(random_post_id, f'{subreddit_name}_video{videos_downloaded}', target_directory)
        if downloaded:
            total_download_lenght += post_id_dict[random_post_id]
        id_list.remove(random_post_id)
        if len(id_list) == 0:
            logging.info(f'no more clips available to download before reaching desired clip lenght')
            break
    logger.info(f'successfully downloaded {videos_downloaded} videos from reddit for a total of {total_download_lenght}s of content.')
    pushover.send_notification(f'successfully downloaded {videos_downloaded} videos from reddit for a total of {total_download_lenght}s of content.')