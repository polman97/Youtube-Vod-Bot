import http.client, urllib
import logging

#"token": "ah9aqxojr8zqmfnz8nstha59j96y2y",
#"user": "uvxh3gdpukmhx8bew6m1zstvte339d",

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

def send_notification(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                     "token": "ah9aqxojr8zqmfnz8nstha59j96y2y",
                     "user": "uvxh3gdpukmhx8bew6m1zstvte339d",
                     "message": message,
                 }), {"Content-type": "application/x-www-form-urlencoded"})
    logger.info(f'Push notification sent: {message}')
    conn.getresponse()

