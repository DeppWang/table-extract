FROM python:3.8

RUN pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple
    
RUN pip install --default-timeout=100 Flask requests gunicorn tabula-py

COPY tableetl /tableetl

CMD gunicorn -w 2 -b 0.0.0.0:80 --preload tableetl:app -- daemon