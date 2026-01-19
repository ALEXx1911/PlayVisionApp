import multiprocessing

bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count() * 2 + 1

worker_class = "sync"

#Max time in seconds for a worker to respond before being killed and restarted
timeout = 60

keepalive = 5

loglevel = "info"

#Docker collects logs from stdout/stderr
accesslog = "-"

errorlog = "-"

# Restart workers after handling a certain number of requests to prevent memory leaks
max_requests = 1000
max_requests_jitter = 50

