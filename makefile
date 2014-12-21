venv/bin/python:
	virtualenv -p python3 venv
	venv/bin/pip install flask celery elasticsearch PyLD requests rdflib rdflib-jsonld html5lib flask-stache laconia

venv/bin/honcho: venv/bin/python
	venv/bin/pip install honcho

r2r:
	cd r2r && mvn install

shapely/target/universal/stage/bin/shapely: r2r
	cd shapely && sbt compile stage

run: venv/bin/honcho venv/bin/python shapely/target/universal/stage/bin/shapely
	honcho start

.PHONY: run r2r notify
