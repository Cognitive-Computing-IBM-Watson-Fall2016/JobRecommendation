
#!/usr/bin/env python2.7
import os
import click
import flask
from flask import Flask, request, render_template, g, redirect, Response, json 
import requests
import json
import twitter
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
min_words = 100
titles = ['big5-openness', 'big5-conscientiousness', 'big5-extraversion', 'big5-agreeableness', 'big5-neuroticism', \
        'need-challenge', 'need-closeness', 'need-curiosity', 'need-excitement', 'need-harmony', 'need-ideal', \
        'need-liberty', 'need-love', 'need-practicality', 'need-self-expression', 'need-stability', 'need-structure',\
        'value-conservation', 'value-openness_to_change', 'value-hedonism', 'value-self_enhancement', 'value-self_transcendence'
        ]
tweet_filename = ''
user_vector = []


def parse_tweet():
    global user_vector
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
    user_vector = need + person + value


def to_json_person():
    arr = user_vector
    results = []
    for i in range(0, 22):
        temp = {}
        temp['title'] = titles[i]
        temp['subtitle'] = str(arr[i]*100) + 'percentile (%)'
        temp['ranges'] = [100]
        temp['measures'] = [arr[i]*100]
        temp['markers'] = [arr[i]*100]
        results.append(temp)
    return json.dumps(results)


def to_json_company(tuples):
    results = []
    for i in range(0, min(5, len(tuples))):
        temp = {}
        temp['title'] = tuples[i][0]
        temp['subtitle'] = str(tuples[i][1])
        temp['ranges'] = [0, 15]
        temp['measures'] = [tuples[i][1]]
        temp['markers'] = [tuples[i][1]]
        results.append(temp)
    return json.dumps(results)


# --- Twitter Analysis --- start ----
def convert_status_to_pi_content_item(s):
    return {
        'userid': str(s.user.id),
        'id': str(s.id),
        'sourceid': 'python-twitter',
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
        'reply': (s.in_reply_to_status_id == None),
        'forward': False
    }


def twitter_analyzer(t_id):
    handle = t_id
    twitter_api = twitter.Api(consumer_key='DIHaMzuF37zYvCsIwGUee3QO6',
                              consumer_secret='oUotOFsH8kiz2Neh35bxH2lu5El94GLtOQIIllK8hjlmcpmvM6',
                              access_token_key='807677389878726657-x0IGggAGUrg1FJeblrUC8u56BpcaXXt',
                              access_token_secret='2NxlriEmgcpm5lSiLJsAbneWrlgXoZpyHYlwAF9hrbX9q',
                              debugHTTP=True)

    max_id = None
    statuses = []
    for x in range(0, 16):  # Pulls max number of tweets from an account
        if x == 0:
            statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                           count=200,
                                                           include_rts=False)
            status_count = len(statuses_portion)
            max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
        else:
            statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                           count=200,
                                                           max_id=max_id,
                                                           include_rts=False)
            status_count = len(statuses_portion)
            if status_count!=0 :
                max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
        for status in statuses_portion:
            statuses.append(status)

    pi_content_items_array = map(convert_status_to_pi_content_item, statuses)
    pi_content_items = {'contentItems': pi_content_items_array}

    r = requests.post('https://gateway.watsonplatform.net/personality-insights/api' + '/v2/profile',
                      auth=('c5032e9c-1eef-48a6-b237-93d8e6153d9e', 'hQLicY30CvOs'),
                      headers={
                          'content-type': 'application/json',
                          'accept': 'application/json'
                      },
                      data=json.dumps(pi_content_items)
                      )

    print("Profile Request sent. Status code: %d, content-type: %s" % (r.status_code, r.headers['content-type']))
    jsonFile = open(t_id + ".json", "w")
    jsonFile.write(json.dumps(json.loads(r.text), indent=4, separators=(',', ': ')))
    jsonFile.close()
# --- Twitter Analysis --- end ----


# --- Distance Calculation --- start ----
def dist_cal():
    global user_vector
    input_file = open('companies_vector.json').read()
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
    return company_scores
# --- Distance Calculation --- end ----

@app.before_request
def before_request():
    try:
        print "connection got!"
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()


@app.teardown_request
def teardown_request(exception):
    try:
        print 'the session closed'
    except Exception as e:
        pass


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/personality', methods=['POST'])
def personality():
    tid = request.form['tid']
    #twitter_analyzer(tid)
    global tweet_filename
    tid = 'KingJames'
    tweet_filename = tid + '.json'
    return flask.render_template("personality.html")


@app.route("/get_data")
def get_data():
    parse_tweet()
    data = to_json_person()
    return data


@app.route('/companies')
def companies():
    return flask.render_template('companies.html')


@app.route("/get_companies")
def get_companies():
    company_scores = dist_cal()
    data = to_json_company(company_scores)
    return data


if __name__ == "__main__":
    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=6998, type=int)
    def run(debug, threaded, host, port):
        print "running on %s:%d" % (host, port)
        app.run(host=host, port=port, debug=debug, threaded=threaded)
    run()
