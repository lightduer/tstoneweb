# -*- coding: utf-8 -*-
import abc
import copy

import functools
import wtforms
from flask import request
from flask.views import MethodViewType
from flask_restful import Resource
from werkzeug.datastructures import ImmutableMultiDict
from common.exceptions import CheckException


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


def _get_req_args():
    """ 获取请求
    """
    if request.get_json(silent=True):
        req_args = ImmutableMultiDict(getattr(request, 'json', None))
    elif request.method in ['GET']:
        req_args = request.args
    else:
        req_args = request.form
    return req_args


def _wrapper_rest_method(func):
    @functools.wraps(func)
    def _wrapper(self, *args, **kwargs):
        func_kwargs = {}
        req_args = _get_req_args()
        args_count = func.im_func.func_code.co_argcount  # func parameters count
        args_names = func.im_func.func_code.co_varnames  # func parameters name tuple
        # just new test
        form, new_req_args = self._make_form(req_args, request.files)
        if not form.validate():
            raise CheckException(form.errors)
        field_value = self._set_field_value(form.data)
        if field_value:
            kwargs.update(field_value)
        for i in xrange(1, args_count):  # according to python stack, the first parameters are defined by func
            field = args_names[i]
            func_kwargs.setdefault(field, kwargs.get(field, None))
        try:
            ret_val = func(self, **func_kwargs)
        except Exception as e:
            raise
        return ret_val
    return _wrapper


class DynamicObjectMeta(type):
    def __new__(cls, name, base, attrs):
        t = super(DynamicObjectMeta, cls).__new__(cls, name, base, attrs)
        # if the 'cls' is the subclass of DynamicObject
        if Resource in base:
            return t
        is_subclass = False
        for b in base:
            if issubclass(b, MyResource) and b is not MyResource:
                fields = getattr(b, '__fields', [])
                for field in fields:
                    seg = getattr(b, field, None)
                    if isinstance(seg, Segment):
                        attrs.setdefault(field, seg)
                is_subclass = True
        if MyResource in base or is_subclass:
            fields = []
            # add Segment to __fields
            for key, val in attrs.iteritems():
                if not key.startswith('__') and isinstance(val, Segment):
                    fields.append(key)
            setattr(t, '__fields', fields)
            # if not hasattr(t, '__hidden_support__'):
            #     setattr(t, '__uuid__', '{0}.{1}'.format(t.__module__, name))
            if not is_subclass:
                setattr(t, '__funcs', [])
                cls.decorate_real_method(t, 'get', _wrapper_rest_method)
                cls.decorate_real_method(t, 'post', _wrapper_rest_method)
                cls.decorate_real_method(t, 'put', _wrapper_rest_method)
                cls.decorate_real_method(t, 'delete', _wrapper_rest_method)
        return t

    @staticmethod
    def decorate_real_method(real_type, method_name, decorate_method):
        origin_func = getattr(real_type, method_name, None)
        funcs = getattr(real_type, '__funcs', [])
        if origin_func:
            funcs.append(method_name)
            setattr(real_type, '__funcs', funcs)
        # this function get all hidden method call, don't wrapper it !
        if hasattr(real_type, '__hidden_support__'):
            return
        if hasattr(real_type, method_name):
            setattr(real_type, method_name, decorate_method(origin_func))


class DynamicMeta(abc.ABCMeta, DynamicObjectMeta, MethodViewType):
    pass


class MyResource(Resource):
    """dynamic create object during the flask is already running
       which can define class by user if you like
    """
    __metaclass__ = DynamicMeta

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
                    pass
            setattr(self, field, val)
            form_data[field] = val

        if convert_errors:
            raise Exception('\n'.join(convert_errors))
        return form_data

    @staticmethod
    def error_router(original_handler, e):
        return original_handler(e)

