from Functions import reddit_api
import logging
import os


# setting up logger, paste this at beginning on each file
logging.basicConfig(encoding='utf-8')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')
# file output settings
file_handler = logging.FileHandler('log.log',encoding='utf-8')
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

# gets current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
temp_storage = os.path.join(current_directory, 'temp_clip_storage')
output_storage = os.path.join(current_directory, 'output_storage')


if __name__ == "__main__":
    reddit_api.check_login()
    ##prompt chatgpt for fun facts
    ##create voice file
    ##clip duration from the 1h parkour vod
    ##add subtitles
    ## success!