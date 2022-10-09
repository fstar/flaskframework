"""应用启动入口"""
import logging
from logging.config import fileConfig
import os
import numpy
import click
import inject

from app import flask_app, StandaloneApplication
from app.dependencies import Config

logger = logging.getLogger(__name__)
# numpy版本大于等于1.17.1引入的一个 feature, 将大于4M的内存，全部放入 hugepage 中，并默认开启
# 会导致内存访问及其缓慢乃至超时的问题。
# 在 numpy>=1.19.0 中加入了 _set_madvise_hugepage 可以关闭该特性
# 新版numpy支持使用环境变量 export NUMPY_MADVISE_HUGEPAGE=0
numpy.core.multiarray._set_madvise_hugepage(False)  # pylint: disable=W0212

config: Config = inject.instance(Config)


def init_logger(log_config_file=None):
    """配置 logger """
    if log_config_file:
        fileConfig(log_config_file, disable_existing_loggers=False)
    else:
        logging_config = (os.getenv('LOG_CONFIG_PATH') or os.path.join(os.path.dirname(__file__), 'log.ini'))
        fileConfig(logging_config, disable_existing_loggers=False)


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
    StandaloneApplication(flask_app, config.gunicorn_config).run()


if __name__ == '__main__':
    cli()
