import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


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


def dist_cal(user_vector):
    input_file = open('vectors.json').read()
    companies = json.loads(input_file)  # dict
    company_scores = []  # list of 2-tuples
    user_vector_arr = np.array(user_vector).reshape(1, -1)
    company_score = []
    for company_name, company_vectors in companies.items():
        company_vectors = np.array(company_vectors)
        similarities = cosine_similarity(company_vectors, user_vector_arr)
        company_score = 1 * similarities[0] + \
                        2 * similarities[1] + \
                        3 * similarities[2] + \
                        4 * similarities[3] + \
                        5 * similarities[4]
        company_scores.append((company_name, float(company_score)))
    company_scores.sort(key=lambda x: x[1])  # sort by score in descending order
    company_scores.reverse()
    print company_scores[0][0], company_scores[0][1]
    print company_scores[1][0], company_scores[1][1]
    print company_scores[2][0], company_scores[2][1]
    print company_scores[3][0], company_scores[3][1]

dist_cal(parse_tweet())