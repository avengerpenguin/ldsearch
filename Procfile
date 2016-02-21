enrich:        cd enrich && venv/bin/python3 -u enrich.py
infer:         infer/venv/bin/python3 -u infer/infer.py
ingest:        ingest/venv/bin/python3 -u ingest/ingest.py
notify_celery: cd notify && venv/bin/celery -A notify.celery worker -n notify.$PORT
notify:        notify/venv/bin/python3 -u notify/notify.py
search:        cd search && venv/bin/python3 -u search.py
enrich_celery: cd enrich && venv/bin/celery -A  enrich.celery worker -n enrich.$PORT
infer_celery:  cd infer && venv/bin/celery -A infer.celery  worker -n infer.$PORT
