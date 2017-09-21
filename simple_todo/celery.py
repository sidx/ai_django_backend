from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_todo.settings')

app = Celery("ai_todolist")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
redis_url = os.environ.get('REDIS_URL', None)
app.config_from_object({
    "accept_content": ['json', 'pickle'],
    "task_serializer": 'pickle',
    "timezone": 'UTC',
    "task_default_queue": 'general',
    "task_always_eager": False,
    "task_ignore_result": True,

    "worker_send_task_events": True,

    "broker_url": redis_url,
    "result_backend": redis_url,
})

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
