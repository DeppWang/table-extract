## Hard Point
1. 镜像、Gunicorn 稳定性
2. 图片解析
3. 图片截取
4. 指定横向

## Docker 镜像

```
git clone ssh://git@10.60.128.2:7999/elab-2/table-extract.git
docker build -t table-extract .
docker run -dit -p 80:80 --name=table-extract table-extract /bin/bash 
docker exec -it table-extract /bin/bash
gunicorn -c gunicorn_conf.py tableetl:app --preload
docker cp . table-extract:/home/
```

## 表格提取、图片解析

### 表格提取

### 图片解析

```
tesseract 26-1_1.jpg 26-1_1 -l eng pdf
tesseract test.png test -l eng pdf
```

