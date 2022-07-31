FROM python:3.8

RUN pip install Flask requests gunicorn

COPY tableetl /tableetl

CMD gunicorn --workers $WORKERS \
  --threads $THREADS \
  --bind 0.0.0.0:$PORT_APP \
  tableetl:app