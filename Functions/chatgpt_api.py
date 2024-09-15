from openai import OpenAI
import logging

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

def get_ai_response(post_title, prompt, post='post'):
    client = OpenAI(
        api_key = '' # your openAI api key
        )
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                'role':'user',
                'content':prompt
                }
            ],
            model='gpt-3.5-turbo'
        )
        response = chat_completion.choices[0].message.content
        logger.info(f'Response received from openAi: {response}')
    except Exception as e:
        logger.info('Error getting a response from openAI:' + e)
    return response