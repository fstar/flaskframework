"""配置项"""
import logging
import os
from dataclasses import dataclass, field
from typing import Dict
import yaml
try:
    # use faster C loader if available
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader  # type: ignore[misc]
import inject

import app

logger = logging.getLogger(__name__)


def number_of_workers():
    return 5


@dataclass
class Config:
    """默认配置"""
    # 项目目录
    project_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 是否开启 swagger
    enable_swagger: bool = False
    # title
    title: str = ''
    # description
    description: str = ''
    # 版本
    version: str = ''

    # db url
    db_uri: str = ''

    # gunicorn配置
    gunicorn_config: Dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.gunicorn_config:
            self.gunicorn_config = {
                'bind': '0.0.0.0:5004',
                'workers': number_of_workers(),
                'threads': 2,
            }


def bind_config(binder):
    """bind config"""
    config_filename = os.getenv('CONFIG')
    if not config_filename:
        config_filename = os.path.join(os.path.dirname(os.path.dirname(app.__file__)), 'configs', 'config.yml')
        logger.info(f'CONFIG env is not set, try {config_filename}')
    with open(config_filename, encoding='utf-8') as fin:
        data = yaml.load(fin, Loader)
        config = Config(**data) if data is not None else Config()

    with open(os.path.join(Config.project_path, 'VERSION'), encoding='utf-8') as version_file:
        setattr(config, 'NAME', version_file.readline().strip('\n'))
        setattr(config, 'VERSION', version_file.readline().strip('\n'))

    config_filename = os.getenv('VERSIONS', '')
    setattr(config, 'versions', config_filename)
    binder.bind(Config, config)


def bind(binder):
    """bind instance"""
    binder.install(bind_config)


inject.configure(bind, bind_in_runtime=False)
