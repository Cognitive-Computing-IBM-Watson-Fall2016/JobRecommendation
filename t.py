import json

user_file = open('person_tweet.json').read()
user_vector = json.loads(user_file)['807677389878726657']
print user_vector