elasticsearch: elasticsearch --config=/usr/local/opt/elasticsearch/config/elasticsearch.yml
infer:         venv/bin/python3 infer/infer.py
ingest:        venv/bin/python3 ingest/ingest.py
notify_celery: cd notify && ../venv/bin/celery -A notify.celery worker
notify_www:    venv/bin/python3 notify/notify.py
search:        cd search && ../venv/bin/python3 search.py
