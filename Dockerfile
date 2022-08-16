FROM rappdw/docker-java-python:openjdk1.8.0_171-python3.6.6

RUN pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip3 install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /home/table-extract

COPY . .

RUN pip install -r requirements.txt

CMD gunicorn -c gunicorn_conf.py run:app --preload