"""flask app 初始化"""
import logging
from flask import Flask
from flask_compress import Compress


from app.flask_restx_api import flask_restx_api

logger = logging.getLogger(__name__)


def bind_app_hook(app: Flask):
    """绑定请求前后钩子"""

    @app.after_request
    def cors_after_request(resp):  # pylint: disable=unused-variable
        resp.headers.set('Access-Control-Allow-Origin', '*')
        resp.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        resp.headers.set('Access-Control-Allow-Headers',
                         'Response-Language, Content-Type, Cache-Control, Authorization, X-Requested-With')
        return resp

    @app.teardown_request
    def flask_teardown(exception):  # pylint: disable=unused-variable
        del exception

    @app.after_request
    def after_request(response):  # pylint: disable=unused-variable
        return response


def create_app():
    """创建 flask app"""
    app = Flask(__name__)
    Compress(app)
    flask_restx_api.init_app(app)
    app._logger = logging.getLogger(__name__)  # pylint: disable=protected-access
    # app.config['RESTFUL_JSON'] = {'cls': PltJSONEncoder}
    # app.json_encoder = PltJSONEncoder

    # 绑定全局异常处理器、请求前后钩子、默认终端等
    bind_app_hook(app)

    # 注册路由表
    blueprints = ()
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    app.url_map.strict_slashes = False
    return app
