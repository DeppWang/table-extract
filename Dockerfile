FROM python:3.8

RUN pip install Flask requests gunicorn

COPY tableetl /tableetl

CMD gunicorn --workers 2 \
  --threads 10 \
  --bind 0.0.0.0:80 \
  tableetl:app