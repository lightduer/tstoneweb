# -*- coding: utf-8 -*-
import wtforms


class Segment(object):
    __slots__ = ('method', 'type', 'default', 'validators', 'converter', 'nullable')

    def __init__(self, method=None, seg_type=None, default=None, nullable=None, validator=None, converter=None):

        """
        define for query field
        :param method:
        :param seg_type:
        :param default:
            默认值
        :param nullable:
            允许字段为空，不进行validators的校验
            like nullable = ['GET', 'POST']，说明在get和post时，允许为空，其余方式不允许为空
        :param validator:
        :param converter:
        """

        validator = validator or []
        method = method or ['GET']
        converter = converter or []
        self.type = seg_type or wtforms.StringField
        if self.type is wtforms.IntegerField:
            default = default or 0
        self.default = default
        # like nullable = ['GET', 'POST']，说明在get和post时，允许为空，其余方式不允许
        self.nullable = nullable or []  # 允许字段为空，不进行validators的校验
        self.method = method if isinstance(method, list) else [method, ]
        self.converter = converter if isinstance(converter, list) else [converter, ]
        self.validators = validator if isinstance(validator, list) else [validator, ]
