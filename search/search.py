import os
from flask import Flask, request, render_template
from flask_stache import render_view, render_template
from laconia import ThingFactory
from elasticsearch import Elasticsearch
from rdflib import Graph
import json


app = Flask(__name__)
app.import_name = '.'
es = Elasticsearch()


@app.route('/')
def index():
    return render_template('home')


@app.route('/search')
def search():
    query = request.args.get('q') or '*'
    response = es.search(index='bbc', q=query)

    hits = []
    for hit in response['hits']['hits']:
        g = Graph()
        g.parse(data=json.dumps(hit['_source']['jsonld']), format='json-ld')
        g.bind('og', 'http://ogp.me/ns#')
        g.bind('schema', 'http://schema.org/')

        thing = ThingFactory(g)(hit['_id'])

        hits.append(thing)

    results = {
        'total': response['hits']['total'],
        'hits': hits
    }

    return render_template('results', results=results)


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
