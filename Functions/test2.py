import json

with open('funny_subreddits.txt', "r") as my_file:
    data = my_file.read()
    subreddit_list = data.replace('\n', ' ').split(" ")

with open('../Json_files/subreddit_lists.json', 'r') as f:
    data = json.load(f)

data['funny subreddits'] = subreddit_list

with open('../Json_files/subreddit_lists.json', 'w') as f:
    json.dump(data, f)