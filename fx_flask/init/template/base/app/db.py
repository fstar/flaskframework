# -*- coding: utf-8 -*-
import inject
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm import sessionmaker

from app.dependencies import Config

config: Config = inject.instance(Config)

# 创建对象的基类:
Base = declarative_base()
Base.metadata.bind = create_engine(config.db_uri)


class MainDBSession(scoped_session, Session):
    """mysql session"""
    pass


@inject.autoparams()
def init_main_db_session(app_config: Config):
    """初始化 mysql"""
    engine = create_engine(app_config.db_uri, isolation_level='REPEATABLE READ', pool_recycle=1800, pool_pre_ping=True)
    return scoped_session(sessionmaker(engine, autocommit=True))
