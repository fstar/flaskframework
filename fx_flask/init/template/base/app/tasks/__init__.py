# -*- coding: utf-8 -*-
"""celery 初始化"""
import logging
from celery import Celery, platforms

from app.dependencies import Config

logger = logging.getLogger(__name__)


def init_celery(config: Config):
    celery_ = Celery(__name__, include=[
        'app.tasks.scheduler_task',
    ])
    # 定时任务
    beat_schedule = {
        # 'scheduler_task.check_case_job': {
        #     'task': 'app.tasks.scheduler_task.check_case_job',
        #     'args': (),
        #     'schedule': 5,
        #     'options': {
        #         'queue': f'{config.workflow.value.lower()}-beat-queue'
        #     }
        # }
    }
    logger.info(f'Scheduled tasks: {beat_schedule}')
    celery_.conf.update(
        CELERYBEAT_SCHEDULE=beat_schedule,
        CELERY_DEFAULT_EXCHANGE_TYPE='direct',
        BROKER_URL=config.celery_broker,
        CELERY_RESULT_BACKEND=config.celery_backend,
        # 任务的硬超时时间
        CELERYD_TASK_TIME_LIMIT=300,
        CELERY_ACKS_LATE=True,
        CELERY_TASK_RESULT_EXPIRES=600,
        CELERY_TASK_SERIALIZER='json',
        CELERY_ACCEPT_CONTENT=['json', 'pickle'],
        CELERY_RESULT_SERIALIZER='json',
        CELERY_TIMEZONE='Asia/Shanghai',
        CELERY_ENABLE_UTC=True,
        BROKER_CONNECTION_TIMEOUT=10,
        # 拦截根日志配置
        CELERYD_HIJACK_ROOT_LOGGER=False,
        CELERYD_LOG_FORMAT='[%(name)s]:%(asctime)s:%(filename)s:%(lineno)d %(levelname)s/%(processName)s %(message)s')

    platforms.C_FORCE_ROOT = True
    return celery_
