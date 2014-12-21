#!/usr/bin/env python

from flask import Flask, request, render_template
import hyperspace


app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():

    uris = [line
            for line in request.get_data().decode('utf-8').splitlines()
            if not line.startswith('#')]

    for uri in uris:
        g = Graph()
        requests.get(uri)

    return 'Accepted!\n', 202, {'Content-Type': 'text/plain'}



if __name__ == '__main__':
    app.run(debug=True)
