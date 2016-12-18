import json

titles = ['big5-openness', 'big5-conscientiousness', 'big5-extraversion', 'big5-agreeableness', 'big5-neuroticism', \
          'need-challenge', 'need-closeness', 'need-curiosity', 'need-excitement', 'need-harmony', 'need-ideal', \
          'need-liberty', 'need-love', 'need-practicality', 'need-self-expression', 'need-stability', 'need-structure', \
          'value-conservation', 'value-openness_to_change', 'value-hedonism', 'value-self_enhancement',
          'value-self_transcendence'
          ]

tweet_filename = 'tweet.json'


def parse_tweet():
    input_file = open(tweet_filename).read()
    profile = json.loads(input_file)
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
    return X


def toJson(arr):
    results = []
    for i in range(0, 22):
        temp = {}
        temp['title'] = titles[i]
        temp['subtitle'] = 'percentile (%)'
        temp['ranges'] = [20, 40, 60, 80, 100]
        temp['measures'] = [30, 60]
        temp['markers'] = [arr[i]]
        results.append(temp)
    return json.dumps(results)

print parse_tweet()
print toJson(parse_tweet())