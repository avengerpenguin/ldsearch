from flask import Flask, request, render_template
import os
from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Rete.Util import generateTokenSet
from FuXi.Horn.HornRules import HornFromN3
from rdflib import Graph, Namespace
import requests
from celery import Celery


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL = 'amqp://guest@' + os.getenv('RABBIT_HOST', 'localhost')+':5672//',
    CELERY_RESULT_BACKEND = 'amqp://guest@' + os.getenv('RABBIT_HOST', 'localhost')+':5672//'
)
celery = make_celery(app)
http = requests.Session()


@app.route('/', methods=['POST'])
def index():
    request_body = request.get_data().decode('utf-8')
    graph = Graph()
    graph.parse(data=request_body, format='json-ld')

    infer.delay(graph)

    return 'Accepted!', 202


@celery.task()
def infer(graph):
    rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
    rules = HornFromN3(os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'rules.n3'))

    closure_delta = Graph()
    network.inferredFacts = closure_delta
    for rule in rules:
        network.buildNetworkFromClause(rule)

    network.feedFactsToAdd(generateTokenSet(graph))

    new_graph = graph + closure_delta

    # Send to ingest
    http.post('http://localhost:5200/', new_graph.serialize(format='json-ld'))


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))
