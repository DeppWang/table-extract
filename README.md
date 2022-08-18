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

安装 `Comments`:

```
$ pip install -e .
```

## 运行


```
$ export FLASK_APP=comments
$ flask init-db
$ flask run
```

## 测试

=======
## Hard Point
1. 镜像
2. Gunicorn 稳定性
3. 图片截取
4. 图片解析
5. 指定横向



```
docker build -t table-extract .
docker run -dit -p 80:80 --name=table-extract table-extract /bin/bash 
cd workspace/table-extract
docker cp . c0fd936bf027:/home/table-extract
gunicorn -c gunicorn_conf.py tableetl:app --preload
git clone ssh://git@10.60.128.2:7999/elab-2/table-extract.git
docker exec -it c0fd936bf027 /bin/bash
```



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
$ flask run -h 0.0.0.0 -p 80
```

- https://flask.palletsprojects.com/en/2.0.x/server/#development-server

### 保持后台运行

```
gunicorn -w 2 -b 0.0.0.0:80 tableetl:app -- daemon
```

- https://iximiuz.com/en/posts/flask-gevent-tutorial/
- https://lionhead8.medium.com/run-python-flask-server-application-in-background-643692634fd3
- https://medium.com/coding-memo/backend-run-flask-in-background-with-gunicorn-3f1f4cffca8d

### Session



## 测试

安装 `tableetl`:

```
$ pip install -e .
```

执行测试
