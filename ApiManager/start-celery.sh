export REDIS_ADDR=127.0.0.1

celery -A HttpRunnerManager worker -l info -B -f /path/to/log