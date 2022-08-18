bind = "0.0.0.0:80"
workers = 2
worker_class = 'gevent'
worker_connections = 2000
backlog = 2048
pidfile = "gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/error.log"
timeout = 600
capture_output = True
access_log_format = '%(t)s %(u)s %(h)s %(r)s %(s)s %(T)s %(B)s %(f)s %(a)s'