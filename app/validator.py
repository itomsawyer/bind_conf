# -*- coding:utf-8 -*-

from wtforms.validators import ValidationError
from netaddr import IPNetwork, IPAddress

def my_strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value

def netaddr_validator(form, data):
    try:
        IPNetwork(data.value)
    except e:
        raise ValidationError(u'地址段格式不合法 示例192.168.1.0/24')

    return True

class NetAddr(object):
    def __init__(self, message=u'地址段格式不合法 示例192.168.1.0/24'):
        self.message = message

    def __call__(self, form, field):
        try:
            IPNetwork(field.data)
        except e:
            raise ValidationError(self.message)


class IPAddr(object):
    def __init__(self, message=u'IP地址格式不合法 示例192.168.1.1'):
        self.message = message

    def __call__(self, form, field):
        try:
            IPAddress(field.data)
        except e:
            raise ValidationError(self.message)

