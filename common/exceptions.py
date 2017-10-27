# -*- coding: utf-8 -*-
from __future__ import unicode_literals

OK = 200


class MyBaseException(Exception):
    """ Common base class for all non-exit exceptions. """
    code = 400


class CheckException(MyBaseException):
    """ Segment字段校验错误 """
    code = 401


class ConvertException(MyBaseException):
    """ Segment中converter中设置的类型转换错误 """
    code = 401

    def __init__(self, input, converter):
        super(ConvertException, self).__init__()
        self.message = '转换错误，输入：%s，转换器：%s' % (input, converter)


class FieldNotSupport(MyBaseException):
    """ Segment字段不支持 """
    code = 401


class IpFormatInvalid(MyBaseException):
    """ ip格式错误或无效 """
    code = 401


class ConstraintFailure(MyBaseException):
    """ 约束性错误
    唯一性验证等
    """
    code = 401


class PermissionDenied(MyBaseException):
    code = 400


# 校验错误集合
# CheckErrorCollection = (
#     CheckException, ConvertException, FieldNotSupport, IpFormatInvalid, ConstraintFailure
# )


class ImplementedError(MyBaseException):
    """ 方法或功能尚未实现 """
    code = 404


class ImportFileException(MyBaseException):
    """ 导入文件错误 """
    code = 400


class ExportFileException(MyBaseException):
    """ 导出文件错误 """
    code = 400


class ESNotInitException(MyBaseException):
    """ ES尚未初始化 """
    code = 400


class ESConfigException(MyBaseException):
    """ ES配置失败 """
    code = 405


class ClassOtherError(MyBaseException):
    """ view层class类中抛出的提示错误"""
    code = 404


class CsrfCheckError(MyBaseException):
    """csrf 验证失败"""
    code = 403
    message = '操作失败,请刷新页面后重新尝试！'


class LoginFailure(MyBaseException):
    """ 尚未登陆或登陆失败 """
    code = 302
    message = '未登陆或登陆超时！'


class CommunicationException(MyBaseException):
    """与外系统通信错误"""
    code = 400


class InsertConflictException(MyBaseException):
    """ 插入数据冲突错误 """
    code = 400


class CommonMessageException(MyBaseException):
    """ 通用抛出异常信息 """
    code = 400


class ArgumentError(MyBaseException):
    """ 参数错误 """
    code = 400


class UnknownError(MyBaseException):
    """ 未知错误 """
    code = 400


class InternalError(MyBaseException):
    """ 内部错误 """
    code = 500



