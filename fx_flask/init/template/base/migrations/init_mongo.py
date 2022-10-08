"""初始化 mongo"""
import logging
import inject
import pymongo
from pymongo import uri_parser

from app.dependencies import Config

logger = logging.getLogger(__name__)
config: Config = inject.instance(Config)


def create_mongo_db():
    """初始化mongo 创建子产品数据库"""
    if not hasattr(config, 'mongo_uri', None) or not config.mongo_uri:
        return

    mongo_url = config.mongo_uri
    res = uri_parser.parse_uri(mongo_url)

    db_name = res['database']
    username = res['username']
    password = res['password']

    url = mongo_url.split(f'/{db_name}')[0]
    mongo_client = pymongo.MongoClient(url)
    database = mongo_client[db_name]

    user_name_set = {x['user'] for x in database.command('usersInfo')['users']}
    if username in user_name_set:
        logger.info(f'User-[{username}] already exist in database[{db_name}]')
    else:
        logger.info(f'Create user-[{username}] for the database[{db_name}]')
        logger.info(database.command('createUser', username, pwd=password, roles=['readWrite']))


def init_mongodb():
    """TODO 这里加入初始化 mongo 的操作, 比如创建索引"""
    logger.info('初始化 mongo')


def init_mongo_config():
    """初始化 mongo"""
    create_mongo_db()
    init_mongodb()
