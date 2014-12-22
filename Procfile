enrich:        cd enrich && ../venv/bin/python3 -u enrich.py
infer:         venv/bin/python3 -u infer/infer.py
ingest:        venv/bin/python3 -u ingest/ingest.py
notify_celery: cd notify && ../venv/bin/celery -A notify.celery worker -n notify.$PORT
notify:        venv/bin/python3 -u notify/notify.py
search:        cd search && ../venv/bin/python3 -u search.py
enrich_celery: venv/bin/celery -A enrich.enrich.celery worker -n enrich.$PORT
infer_celery:  venv/bin/celery -A infer.infer.celery  worker -n infer.$PORT
