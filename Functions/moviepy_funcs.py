from moviepy.editor import VideoFileClip, CompositeVideoClip, ColorClip
import os
import logging
import shutil
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


def create_16_9_compilation(temp_directory, output_directory, video_name):
    folder_path = temp_directory
    video_clips = []
    logger.info(f'combining all mp4s in {temp_directory}')
    current_duration = 0
    video_created = False
    try:
        for file_name in os.listdir(folder_path):  # checks all filenames in given directory
            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.mp4'): # checks if file ends with .mp4
                logger.debug(f' adding {file_name} to compilation')
                vod = VideoFileClip(file_path)  # turns mp4 into moviepy clip
                if vod.size[1] >= vod.size[0] and vod.size[0] < 1080:
                    logger.info(f'rezising clip height from {vod.size[0]} to 1080')
                    vod = vod.resize(height=1080)
                if vod.size[0] >= vod.size[1] and vod.size[0]/vod.size[1] < 1920/1080:
                    vod = vod.resize(height=1080)
                elif vod.size[0] >= vod.size[1] and vod.size[0]/vod.size[1] > 1920/1080:
                    vod = vod.resize(width= 1920)
                vod = vod.set_position('center')  # positions the clip in the center
                vod = vod.set_start(current_duration)  # sets start time  at current vod duration
                video_clips.append(vod)
                current_duration += vod.duration
        background_color = (0, 0, 0)  # we make a black background for all clips
        duration = current_duration
        background_clip = ColorClip(size=(1920, 1080), color=background_color, duration=duration)
        composite_clip = CompositeVideoClip([background_clip] + video_clips)
        composite_clip.write_videofile(f'{video_name}.mp4', codec='libx264', fps=24)
        logger.info('Compilation video created')
        pushover.send_notification('Daily Compilation Created')
        video_created = True
    except Exception as e:
        logger.error(f'Failed to create daily compilation: {e}')
        pushover.send_notification(f'Failed to create daily compilation.')
    current_directory = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_directory, video_name)
    logger.debug(f'attempting to move "{video_name}"')
    try:
        shutil.copy2(path, output_directory)  # moves the file to the shorts folder
        logger.debug(' clip moved successfully')
    except Exception as e:
        logger.error(f' Error moving clip: {e}')
    return video_created

def filter_shorts(directory, target_directory):
    folder_path = directory
    video_clips = []
    logger.info(f'creating shorts from {directory}')
    current_duration = 0
    shorts = []

    for file_name in os.listdir(folder_path):  # checks all filenames in given directory
        file_path = os.path.join(folder_path, file_name) # puts all mp4s into the list
        if file_name.endswith('.mp4'):  # checks if file ends with .mp4
            vod = VideoFileClip(file_path)  # turns mp4 into moviepy clip
            if vod.size[0] < vod.size[1]:
                if vod.size[1] < 1020:  # checks if its short format, resizes to 1080 height
                    logger.debug(f'adding "{file_name}" to list of shorts to be moved')
                    vod = vod.resize(height=1020)
                    shorts.append(file_path)
            vod.close()
    for path in shorts:
        logger.debug(f'attempting to move {path}')
        try:
            shutil.copy2(path, target_directory)  # moves the file to the shorts folder
            logger.debug(' clip moved successfully')
        except Exception as e:
            logger.error(f' Error moving clip: {e}' )



