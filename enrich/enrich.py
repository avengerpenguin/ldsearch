from flask import Flask, request, render_template
import os
from rdflib import Graph, Namespace
import requests
try:
    from enrichers import programmes_rdf, dbpedia_spotlight
except ImportError:
    from enrich.enrichers import programmes_rdf, dbpedia_spotlight
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
app.import_name = '.'
celery = make_celery(app)


enrichers = [programmes_rdf, dbpedia_spotlight]
http = requests.Session()


@app.route('/', methods=['POST'])
def index():
    request_body = request.get_data().decode('utf-8')
    graph = Graph()
    graph.parse(data=request_body, format='json-ld')

    enrich.delay(graph)

    return 'Accepted!', 202


@celery.task(name='enrich.enrich')
def enrich(graph):
    for enricher in enrichers:
        enricher.enrich(graph)

    # Send to infer
    http.post('http://localhost:5100/', graph.serialize(format='json-ld'))


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)))

