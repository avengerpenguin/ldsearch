import os
from flask import Flask, request, render_template
from elasticsearch import Elasticsearch
from pyld import jsonld
import json
from rdflib import Graph, URIRef


app = Flask(__name__)
es = Elasticsearch()


@app.route('/', methods=['POST'])
def index():
    request_body = request.get_data().decode('utf-8')
    doc = json.loads(request_body)
    body = {'jsonld': jsonld.expand(doc)}

    g = Graph()
    g.parse(data=request_body, format='json-ld')

    for identifier in g.objects(subject=None, predicate=URIRef('http://purl.org/dc/terms/identifier')):
        es.index(index='bbc', body=body, doc_type='item', id=identifier)

    return 'Accepted!', 202


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
