from flask import Flask, request, render_template
import os
from rdflib import Graph, Namespace
import requests
from enrichers import programmes_rdf

app = Flask(__name__)


enrichers = [programmes_rdf]


@app.route('/', methods=['POST'])
def index():
    request_body = request.get_data().decode('utf-8')
    graph = Graph()
    graph.parse(data=request_body, format='json-ld')

    for enricher in enrichers:
        enricher.enrich(graph)

    # Send to infer
    requests.post('http://localhost:5100/', graph.serialize(format='json-ld'))

    return 'Accepted!', 202


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
