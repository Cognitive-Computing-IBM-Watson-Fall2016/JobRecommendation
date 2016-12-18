#!/usr/bin/env python2.7

import os
import click
import flask
from flask import Flask, request, render_template, g, redirect, Response, json 
import json
import numpy as np

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
min_words = 100
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

@app.before_request
def before_request():
    try:
        print "connection got!"
    except:
        print "uh oh, problem connecting to database"
        import traceback; traceback.print_exc()


@app.teardown_request
def teardown_request(exception):
    """
    close everything and reclaim resource
    """
    try:
        print 'the session closed'
    except Exception as e:
        pass

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/bullet')
def bullet():
    X = parse_tweet()
    return flask.render_template('bullet.html')

@app.route('/companies')
def companies():
    return flask.render_template('companies.html')

@app.route('/personality')
def personality():
    id = request.args.get('tid')
    print id
    return flask.render_template("diagram.html", mux=3, muy=3)

@app.route('/profile',methods=['POST'])
def profile():
    m=[]
    context = dict(data1=m, data2='movies')
    return render_template("result.html",**context)   


@app.route("/get_data")
def get_data():
    input_file = open('bullet.json').read()
    data = json.dumps(json.loads(input_file))
    return data

@app.route("/get_companies")
def get_companies():
    input_file = open('companies.json').read()
    data = json.dumps(json.loads(input_file))
    return data

@app.route("/data")
@app.route("/data/<int:ndata>")
def data(ndata=100):
    """
    On request, this returns a list of ``ndata`` randomly made data points.

    :param ndata: (optional)
        The number of data points to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10. ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
        "color": c[i]}
        for i in range(ndata)])

@app.route("/gdata")
@app.route("/gdata/<float:mux>/<float:muy>")
def gdata(ndata=100,mux=.5,muy=0.5):
    """
    On request, this returns a list of ``ndata`` randomly made data points.
    about the mean mux,muy

    :param ndata: (optional)
        The number of data points to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """

    x = np.random.normal(mux,.5,ndata)
    y = np.random.normal(muy,.5,ndata)
    A = 10. ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
        "color": c[i]}
        for i in range(ndata)])


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
