elasticsearch: elasticsearch --config=/usr/local/opt/elasticsearch/config/elasticsearch.yml
shapely: shapely/target/universal/stage/bin/shapely -Dhttp.port=$PORT
ingest: venv/bin/python3 ingest/ingest.py
notify_celery: cd notify && ../venv/bin/celery -A notify.celery worker
notify_www: venv/bin/python3 notify/notify.py
search: venv/bin/python3 search/search.py
