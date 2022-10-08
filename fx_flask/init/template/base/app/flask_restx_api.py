"""初始化 flask_restx Api 对象"""
import logging
import inject
from json import dumps

from flask_restx import Api
from flask_restx.api import HTTPStatus
from flask import make_response, current_app

from app.dependencies import Config
from app.exceptions import ClientErr, ExceptionErr, PlatformErr

logger = logging.getLogger(__name__)


def bind_app_hook(restx_api: Api):
    """绑定一些 hook"""

    def output_json(data, code, headers=None):
        """所有返回值统一格式"""

        if code == HTTPStatus.INTERNAL_SERVER_ERROR:
            # 异常返回值
            result = {'data': '', 'code': data['code'], 'message': data['message']}
        else:
            # 正常返回值
            result = {'data': data, 'code': 0, 'message': 'success'}
        dumped = dumps(result, cls=current_app.json_encoder)
        response = make_response(dumped, code)
        response.headers.extend(headers or {})
        return response

    def mask_error_handler(error):
        """生成异常处理的数据"""
        result = {
            'data': '',
            'code': error.code,
            'message': error.message,
        }
        return result, HTTPStatus.INTERNAL_SERVER_ERROR

    restx_api.representations['application/json'] = output_json
    restx_api.error_handlers.update({
        ClientErr: mask_error_handler,
        ExceptionErr: mask_error_handler,
        PlatformErr: mask_error_handler,
    })


def create_flask_restx_api():
    """初始化 flask_restx_app"""
    config = inject.instance(Config)
    if not config.enable_swagger:
        return Api(title=config.title, version=config.version, description=config.description, doc='')
    authorizations = {'apikey': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
    restx_api = Api(
        title=config.title,  # 标题
        version=config.version,  # 版本号
        description=config.description,  # 描述
        doc='/doc',  # swagger UI路由
        security='apikey',  # 使用何种鉴权模式
        authorizations=authorizations)  # 鉴权模式的参数设置
    bind_app_hook(restx_api)
    return restx_api


flask_restx_api = create_flask_restx_api()
