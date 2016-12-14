import json

filename = 'Google.json'
input_file = open(filename).read()
reviews = json.loads(input_file)
cnt = 0
min_words = 50
for review in reviews:
    txt = ''
    if review['advice'] != None:
        txt += review['advice']
    if review['cons'] != None:
        txt += review['cons']
    if review['pros'] != None:
        txt += review['pros']
    if review['summary'] != None:
        txt += review['summary']
    if len(txt.split()) > min_words:
        cnt += 1
print cnt