from flask import Flask, request, render_template
import os
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Rete.Util import generateTokenSet
from FuXi.Horn.HornRules import HornFromN3
from rdflib import Graph, Namespace
import requests


app = Flask(__name__)


rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
rules = HornFromN3(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'rules.n3'))


@app.route('/', methods=['POST'])
def index():
    request_body = request.get_data().decode('utf-8')
    graph = Graph()
    graph.parse(data=request_body, format='json-ld')

    closure_delta = Graph()
    network.inferredFacts = closure_delta
    for rule in rules:
        network.buildNetworkFromClause(rule)

    network.feedFactsToAdd(generateTokenSet(graph))
    closure_delta.bind('schema', Namespace('http://schema.org/'))

    new_graph = graph + closure_delta

    # Send to ingest
    requests.post('http://localhost:5100/', new_graph.serialize(format='json-ld'))

    return 'Accepted!', 202


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
