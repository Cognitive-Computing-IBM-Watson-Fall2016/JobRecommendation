#!/usr/bin/env python2.7

import os
import click
import flask
from flask import Flask, request, render_template, g, redirect, Response, json 
import json

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
min_words = 100
tweet_filename = 'tweet.json'
titles = ['big5-openness', 'big5-conscientiousness', 'big5-extraversion', 'big5-agreeableness', 'big5-neuroticism', \
        'need-challenge', 'need-closeness', 'need-curiosity', 'need-excitement', 'need-harmony', 'need-ideal', \
        'need-liberty', 'need-love', 'need-practicality', 'need-self-expression', 'need-stability', 'need-structure',\
        'value-conservation', 'value-openness_to_change', 'value-hedonism', 'value-self_enhancement', 'value-self_transcendence'
        ]


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
        temp['markers'] = [arr[i]*100]
        results.append(temp)
    return json.dumps(results)


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

    return flask.render_template("personality.html")


@app.route("/get_data")
def get_data():
    data = toJson(parse_tweet())
    return data


@app.route('/companies')
def companies():
    return flask.render_template('companies.html')


@app.route("/get_companies")
def get_companies():
    input_file = open('companies.json').read()  # YOU NEED TO REPLACE THIS
    data = json.dumps(json.loads(input_file))
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
