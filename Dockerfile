FROM python:3.8

RUN pip install Flask requests gunicorn tabula-py

COPY tableetl /tableetl

CMD gunicorn -w 2 -b 0.0.0.0:80 --preload tableetl:app -- daemon