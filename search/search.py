import os
from flask import Flask, request, render_template
from flask_stache import render_view, render_template
from laconia import ThingFactory
from elasticsearch import Elasticsearch
from rdflib import Graph
from rdflib.tools.rdf2dot import rdf2dot
import json
from io import StringIO, BytesIO
from pydot import graph_from_dot_data


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
        g.bind('og2', 'http://opengraphprotocol.org/schema/')
        g.bind('po', 'http://purl.org/ontology/po/')
        g.bind('dcterms', 'http://purl.org/dc/terms/')

        thing = ThingFactory(g)(hit['_id'])

        hits.append(thing)

    results = {
        'total': response['hits']['total'],
        'hits': hits
    }

    return render_template('results', results=results)

@app.route('/graph')
def graph():
    out = StringIO()
    uri = request.args.get('uri')

    g = Graph()
    g.parse(data=json.dumps(es.get(index='bbc', doc_type='item', id=uri)['_source']['jsonld']), format='json-ld')

    rdf2dot(g, out)

    dot_graph = graph_from_dot_data(out.getvalue())

    return dot_graph.create(format='png'), 200, {'Content-Type': 'image/png'}




if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)), host='0.0.0.0')
