#!/usr/bin/env python
import os
from flask import Flask, request, render_template
import requests
from celery import Celery
from rdflib import Graph, URIRef, Literal, RDF


http = requests.Session()


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


@app.route('/', methods=['POST'])
def index():
    uris = [line.strip() # trim any whitespace
            for line in request.get_data().decode('utf-8').splitlines()
            if not line.startswith('#')]

    for uri in uris:
        send_content.delay(uri)

    return 'Accepted!\n', 202, {'Content-Type': 'text/plain'}


@celery.task(name='notify.send_content')
def send_content(uri):
    g = Graph()
    g.add((URIRef(uri), RDF.type, URIRef('http://www.bbc.co.uk/search/schema/ContentItem')))
    g.parse(uri)

    # Send to enrich
    http.post('http://localhost:5000/', g.serialize(format='json-ld'))

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', 5000)), host='0.0.0.0')

