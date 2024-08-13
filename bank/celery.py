import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bank.settings')
app = Celery("bank")
app.config_from_object("django.conf:settings", namespace="CELERY")
# app.conf.task_routes = {'newapp.tasks.task1': {'queue': 'queue1'}, 'newapp.tasks.task2': {'queue': 'queue2'}}
app.autodiscover_tasks()










@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')