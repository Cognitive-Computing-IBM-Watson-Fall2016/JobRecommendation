import os
import json

tid = 'KingJames'
tweet_filename = './static/user/' + tid + '.json'
if not os.path.isfile(tweet_filename):
    print 'not exist'
else:
    print 'exist'

input_file = open(tweet_filename).read()
profile = json.loads(input_file)
print profile