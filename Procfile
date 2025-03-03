<!-- web: gunicorn -w 4 -b 0.0.0.0:$PORT app:app -->


web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8080
