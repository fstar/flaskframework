"""应用启动入口"""
import logging
import os
import numpy
import click
import inject
from celery import Celery

from sk_backend_common.log_handlers import init_logger
from sk_dicom_interface.dicom_helper import patch_generate_uid
from sk_gunicorn import run_http_server

from app import flask_app
from app.dependencies import Config
from app.tasks.message_listener import MessageListener
# from migrations.init_mongo import init_mongo_config

logger = logging.getLogger(__name__)
# numpy版本大于等于1.17.1引入的一个 feature, 将大于4M的内存，全部放入 hugepage 中，并默认开启
# 会导致内存访问及其缓慢乃至超时的问题。
# 在 numpy>=1.19.0 中加入了 _set_madvise_hugepage 可以关闭该特性
# 新版numpy支持使用环境变量 export NUMPY_MADVISE_HUGEPAGE=0
numpy.core.multiarray._set_madvise_hugepage(False)  # pylint: disable=W0212

# 针对 pydicom 的 generate_uid 函数, 利用 monkey patch 的方式进行改造
patch_generate_uid()
config: Config = inject.instance(Config)


@click.group()
def cli():
    """click group"""
    os.makedirs('logs', exist_ok=True)
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'server.ini'))
    logger.info('Init app...')


@cli.command()
def print_config():
    """打印配置"""
    click.echo('Config:')
    click.echo(config)


@cli.command()
def run_init_data():
    """服务初始化步骤"""
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'server.ini'))
    logger.info('run_init_data....')
    # init_mongo_config()


@cli.command()
def run_api_server():
    """启动 api 服务"""
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'server.ini'))
    # 恢复
    logger.info('Run api server...')
    run_http_server(flask_app, {'bind': '0.0.0.0:5004'})


@cli.command()
def run_alg_consumer():
    """监听 alg 消息队列"""
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'alg_listener.ini'))
    MessageListener.run_alg_listener()


@cli.command()
def run_do_postprocess_consumer():
    """监听 平台分发任务 消息队列"""
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'do_postprocess.ini'))
    MessageListener.run_platform_listener()


@cli.command()
def run_scheduler():
    """轮询任务超时"""
    init_logger(os.path.join(os.path.dirname(__file__), 'configs', 'scheduler.ini'))
    celery_app = inject.instance(Celery)
    celery_app.start(argv=[
        'celery', 'worker', '-l', 'INFO', '-c', '1', '-Q', f'{config.workflow.value.lower()}-beat-queue', '--beat'
    ])


celeryapp = inject.instance(Celery)

if __name__ == '__main__':
    cli()
