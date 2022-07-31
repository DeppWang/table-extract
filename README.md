## 安装

安装虚拟环境

```
python3 -m venv venv
. venv/bin/activate
```

安装依赖

```
pip install -r requirements.txt
```

## 运行

### 内置开发模式：


```
$ export FLASK_APP=tableetl
$ flask init-db
$ flask run
```

- https://flask.palletsprojects.com/en/2.0.x/server/#development-server

### 保持后台运行

```
gunicorn -w 2 -b 0.0.0.0:80 tableetl:app -- daemon
```

- https://iximiuz.com/en/posts/flask-gevent-tutorial/
- https://lionhead8.medium.com/run-python-flask-server-application-in-background-643692634fd3
- https://medium.com/coding-memo/backend-run-flask-in-background-with-gunicorn-3f1f4cffca8d

## 测试

安装 `tableetl`:

```
$ pip install -e .
```

执行测试

```
pytest
```

## 方案

[方案](方案.md)