"""自定义异常"""


class ClientErrStatusCode:
    """客户端异常 code"""
    base = 1000  # base
    params_err = 1001  # 参数错误


class ExceptionErrStatusCode:
    """内部异常 code"""
    base = 2000  # base
    value_err = 2001  # 值异常


class ThirdPartErrStatusCode:
    """请求第三方服务异常 code"""
    base = 3000  # base
    dump_image_err = 3001  # 调用 dump 异常
    alg_err = 3002  # 调用 alg 异常
    setting_err = 3003  # 调用 setting 异常


class ClientErr(Exception):
    """客户端调用错误"""

    def __init__(self, message='客户端调用错误', status_code=ClientErrStatusCode.base):
        self.message = message
        self.code = status_code
        super().__init__(message, status_code)


class ExceptionErr(Exception):
    """模块内部错误"""

    def __init__(self, message='模块内部错误', status_code=ExceptionErrStatusCode.base) -> None:
        self.message = message
        self.code = status_code
        super().__init__(message, status_code)


class PlatformErr(Exception):
    """请求第三方模块错误"""

    def __init__(self, message='请求第三方模块错误', status_code=ThirdPartErrStatusCode.base) -> None:
        self.message = message
        self.code = status_code
        super().__init__(message, status_code)
