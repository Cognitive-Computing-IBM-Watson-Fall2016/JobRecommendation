import json

def json_export(data):
    jsonFile = open("person_tweet_1.json", "w")
    jsonFile.write(json.dumps(data, indent=4, separators=(',', ': ')))
    jsonFile.close()

if __name__ == "__main__":
    min_words = 100
    filename = 'tweet.json'
    input_file = open(filename).read()
    profile = json.loads(input_file)
    X = []
    y = []
    need = []
    value = []
    person = []
    for facet in profile['tree']['children']:
        if facet['id'] == 'personality':
            for item in facet['children'][0]['children']:
                person.append(item['percentage'])
        if facet['id'] == 'needs':
            for item in facet['children'][0]['children']:
                need.append(item['percentage'])
        if facet['id'] == 'values':
            for item in facet['children'][0]['children']:
                value.append(item['percentage'])
    X = need + person + value
    id = profile['id'].encode('utf8')
    dict = {id : X}
    json_export(dict)
