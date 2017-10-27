# -*- coding: utf-8 -*-
import copy
import wtforms
from flask import request
from flask_restful import Resource
from werkzeug.datastructures import ImmutableMultiDict


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


class MyResource(Resource):
    """dynamic create object during the flask is already running
       which can define class by user if you like
    """
    # __metaclass__ = DynamicMeta

    decorators = []
    _form_class = {}

    def _make_form(self, req_args, req_files):
        """ make the form by query parameters"""
        fields = {}
        support_fields = getattr(self, '__fields')
        form_req_args = copy.copy(req_args.to_dict())
        form_req_files = copy.copy(req_files.to_dict())
        form_req_args.update(form_req_files)
        unsupport_fileds = [field for field in req_args if field not in support_fields]
        unsupport_fileds.append([field for field in req_files if field not in support_fields])
        for seg in req_args.keys():
            if seg in unsupport_fileds:
                continue
            segment = getattr(self, seg)
            assert isinstance(segment, Segment)
            validators = segment.validators
            if request.method in segment.nullable and not req_args.get(seg, None):
                validators = []
            fields[seg] = segment.type(seg, validators=validators)
        # add default value to support field if not support by request
        for seg in support_fields:
            if seg in fields:
                continue
            segment = getattr(self, seg)
            # check request method support
            if request.method not in segment.method:
                continue
            validators = segment.validators
            if request.method in segment.nullable and not req_args.get(seg, None):
                validators = []
            fields[seg] = segment.type(seg, validators=validators)
            if seg not in form_req_args:
                form_req_args.setdefault(seg, segment.default)

        name = getattr(self, "__obj_name__", repr(self.__class__.__name__))
        fields.keys().sort()
        name = str('Form' + name + str(fields.keys()))
        base = self.__class__.__base__
        form_class = base._form_class.get(name, None) or type(name, (wtforms.Form,), fields)
        base._form_class.setdefault(name, form_class)
        # return the instance of form_class
        return form_class(ImmutableMultiDict(form_req_args)), form_req_args

    def _set_field_value(self, form_data):
        convert_errors = []
        for field in getattr(self, '__fields'):
            seg = getattr(self, field)
            if request.method not in seg.method:
                setattr(self, field, None)
                continue
            val = form_data.get(field, seg.default)
            for conv in seg.converter:
                try:
                    val = conv(val)
                except Exception as e:
                    print e.message
            setattr(self, field, val)
            form_data[field] = val

        if convert_errors:
            raise Exception('\n'.join(convert_errors))
        return form_data
