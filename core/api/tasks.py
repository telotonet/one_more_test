from celery import shared_task
from time import sleep


@shared_task
def sleep_event():
    sleep(60)