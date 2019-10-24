import json
from django.shortcuts import render
from django.http import HttpResponse
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
import json
from django.utils import timezone
import  datetime


def create_task(name, task, task_args, crontab_time, desc):
    '''
    新增定时任务
    :param name: 定时任务名称
    :param task: 对应tasks里已有的task
    :param task_args: list 参数
    :param crontab_time: 时间配置
    :param desc: 定时任务描述
    :return: ok
    '''
    # task任务， created是否定时创建

    task, created = PeriodicTask.objects.create(name=name, task=task)
    '''
    crontab_time = {
        'month_of_year': 4,  # 月份
        'day_of_month': 10,  # 日期
        'hour': 22,  # 小时
        'minute': 5,  # 分钟
        "timezone":"Asia/Shanghai"
    }'''
    # 获取 crontab
    crontab = CrontabSchedule.objects.filter(**crontab_time).first()
    if crontab is None:
        # 如果没有就创建，有的话就继续复用之前的crontab
        crontab = CrontabSchedule.objects.create(**crontab_time)
    task.crontab = crontab  # 设置crontab
    task.enabled = True  # 开启task
    task.kwargs = json.dumps(task_args, ensure_ascii=False)  # 传入task参数
    #expiration = timezone.now() + datetime.timedelta(hours=1)
    #task.expires = expiration  # 设置任务过期时间为现在时间的一小时以后
    task.description = desc
    task.save()
    return 'ok'



def change_task_status(name, mode):
    '''
    任务状态切换：open or close
    :param name: 任务名称
    :param mode: 模式
    :return: ok or error
    '''
    try:
        task = PeriodicTask.objects.get(name=name)
        task.enabled = mode
        task.save()
        return 'ok'
    except PeriodicTask.DoesNotExist:
        return 'error'


def delete_task(name):
    '''
    根据任务名称删除任务
    :param name: task name
    :return: ok or error
    '''
    try:
        task = PeriodicTask.objects.get(name=name)
        task.enabled = False  # 设置关闭
        task.delete()
        return 'ok'
    except PeriodicTask.DoesNotExist:
        return 'error'
