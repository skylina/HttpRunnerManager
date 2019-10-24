# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.utils import timezone
#from django_celery_beat.models import PeriodicTask,PeriodicTasks
from datetime import timedelta
# set the default Django settings module for the 'celery' program.

# 设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HttpRunnerManager.settings')

app = Celery('HttpRunnerManager')
#  使用CELERY_ 作为前缀，在settings中写配置
# 'django.conf:settings'表示django,conf.settings也就是django项目的配置，celery会根据前面设置的环境变量自动查找并导入
# - namespace表示在settings.py中celery配置项的名字的统一前缀，这里是'CELERY_'，配置项的名字也需要大写
app.config_from_object('django.conf:settings',namespace='CELERY')
app.now = timezone.now

#PeriodicTask.objects.all().update(last_run_at=None)
#[PeriodicTasks.changed(task) for task in PeriodicTask.objects.all()]

# Load task modules from all registered Django app configs.
# 发现任务文件每个app下的task.py
app.autodiscover_tasks()

#platforms.C_FORCE_ROOT=True
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
@app.task(bind=True)
def debug_task(self):

    print('Request: {0!r}'.format(self.request))

app.conf.update(

    CELERYBEAT_SCHEDULE={

        'ApiManager': {

        'task': 'ApiManager.tasks.city_task',

        'schedule': timedelta(hours=1),

        'args': ''

         },

    }

)
