# -*- coding:utf-8 -*-
import os
import string
import StringIO

from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form.fields import Select2TagsField
from flask_admin.form import Select2Widget
from wtforms.validators import DataRequired

from . import models
from flask_admin import BaseView, expose

import threading
lock = threading.Lock()

def my_strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value

class SubmitView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/submit.html', beforeSubmit=True)
    @expose('/apply')
    def submit_all(self):
        retcode = 0
        lock.acquire(True)

        path = "/tmp/iwgweb.conf"

        try:
            from flask import current_app
            if current_app.config["DNS_FORWARD_SUBMIT_PATH"] :
                path = current_app.config["DNS_FORWARD_SUBMIT_PATH"]
        except Exception, e:
            pass

        try:
            dfs = models.DnsForwardZone.query.all()
            s = StringIO.StringIO()
            for df in dfs:
                if len(df.ldnsList) > 0 :
                    s.write("zone \"%s\" IN {\n" % df.dm)
                    s.write("\ttype forward;\n")
                    s.write("\tforward %s;\n" % df.typ)
                    s.write("\tforwarders {\n")
                    for dns in df.ldnsList:
                        s.write("\t\t%s;\n" % dns.addr)
                    s.write("\t};\n")
                    s.write("};\n")

            with open(path, "w") as f:
                f.write(s.getvalue())
                f.close()

            retcode = os.system("rndc reload")
        except Exception,e:
            lock.release()
            return self.render('admin/submit.html', retcode=1, msg="%s" % e)

        lock.release()
        return self.render('admin/submit.html', retcode=retcode)

class DnsForwardZoneGrpView(sqla.ModelView):
    column_labels = dict(name=u'域名组', disabled=u"状态", dns_forward_zones=u"域名")
    column_searchable_list = ('name','disabled')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

class DnsForwardZoneView(sqla.ModelView):
    column_labels = dict(name=u'域名', typ=u'转发策略', grp=u'域名组', disabled=u"状态")
    column_searchable_list = ('name','typ','disabled',models.DnsForwardZoneGrp.name)
    column_sortable_list = (('grp','grp.name'), 'name','typ','disabled')
    form_choices = {
            'typ': [
               ('only', 'only'),
               ('first', 'first'),
            ],
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }


class DnsForwardIpnetGrpView(sqla.ModelView):
    column_labels = dict(name=u'源地址组', disabled=u"状态", prio=u"优先级",dns_forward_ipnets=u'源地址段')
    column_searchable_list = ('name','disabled','prio',models.DnsForwardIpnet.ipnet)
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }


class DnsForwardIpnetView(sqla.ModelView):
    column_labels = dict(grp=u'源地址组', disabled=u"状态",ipnet=u'源地址段')
    column_sortable_list = (('grp','grp.name'), 'ipnet','disabled')
    column_searchable_list = (models.DnsForwardIpnetGrp.name, 'disabled','ipnet')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

class DnsForwarderView(sqla.ModelView):
    column_labels = dict(disabled=u"状态",ldns=u"DNS服务器",ipnet_grp=u"源地址组",zone_grp=u"域名组")
    column_sortable_list = (('zone_grp','zone_grp.name'), ('ipnet_grp','ipnet_grp.name'),('ldns','ldns.addr'),'disabled')
    column_searchable_list = (models.DnsForwardIpnetGrp.name,models.DnsForwardZoneGrp.name, models.Ldns.addr, 'disabled')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

class LdnsView(sqla.ModelView):
    column_labels = dict(addr=u"地址",name=u"名称",disabled=u"状态",status=u"可用性")
    column_searchable_list = ('disabled','name','addr','status')
    form_excluded_columns = ['status']
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

#class DnsForwardZoneView(sqla.ModelView):
#    column_list = ('dm', 'ldnsList', 'typ')
#    column_searchable_list = ['dm','typ', 'ldnsList.addr']
#    #column_filters = ['dm','ldnsList.addr','typ']
#    column_labels = dict(dm=u'域名', typ=u'转发策略', ldnsList=u"DNS服务器",dns_fwds=u"DNS Forwarder")
#
#    #can_export = True
#
#    form_columns = ('dm', 'ldnsList')
#
#    #form_choices = {
#    #        'typ': [
#    #           ('only', 'only'),
#    #           ('first', 'first'),
#    #        ]
#    #}
#
#    form_args = {
#        'ldnsList': {
#            'validators': [DataRequired()]
#        },
#        'dm': {
#            'validators': [DataRequired()],
#            'filters': [my_strip_filter]
#        }
#    }
#
#
#    #form_ajax_refs = {
#    #    'ldns': {
#    #        'fields': (models.Ldns.addr)
#    #    }
#    #}
#
#    #def ldns_choices():
#    #    #return [ ldns.addr for ldns in models.Ldns.query.all() ]
#    #    return models.Ldns.query.all()
#
#
#    #form_extra_fields= dict(
#    #    #dns=QuerySelectMultipleField(
#    #    #dns=MyQuerySelectMultipleField(
#    #    #    label='DNS server',
#    #    #    query_factory=ldns_choices,
#    #    #    validators=[Required()],
#    #    #)
#
#    #    dns=Select2TagsField(label='DNS Server',validators=[Required()]),
#    #)
