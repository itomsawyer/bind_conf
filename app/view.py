# -*- coding:utf-8 -*-
import os
import string

from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form.fields import Select2TagsField
from flask_admin.form import Select2Widget
from wtforms.validators import Required

from . import models
from flask_admin import BaseView, expose

import threading
lock = threading.Lock()

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
            path = current_app.config.DNS_FORWARD_SUBMIT_PATH
        except Exception, e:
            pass

        try:
            #dfs = DnsForwardZone.query.all()
            #with open(path, "w") as f:
            #    for df in dfs:
            #        dnsList = string.split(df.dns)
            #        f.write("zone \"%s\" IN {\n" % df.dm)
            #        f.write("type forward;\n")
            #        f.write("forward %s;\n" % df.typ)
            #        f.write("forwarders {\n")
            #        for dns in dnsList:
            #            f.write("%s;\n" % dns.strip())
            #        f.write("};\n")
            #        f.write("};\n")
            #    f.close()

            retcode = os.system("rndc reload")
        except Exception,e:
            return self.render('admin/submit.html', retcode=-1, msg="%s" % e)

        lock.release()

        return self.render('admin/submit.html', retcode=retcode)


class DnsForwardZoneView(sqla.ModelView):
    column_searchable_list = [models.DnsForwardZone.dm]
    column_filters =  column_searchable_list
    column_labels = dict(dm=u'域名', typ=u'转发策略', ldns=u"DNS服务器")

    can_export = True

    form_excluded_columns = ('typ')
    form_choices = {
            'typ': [
               ('only', 'only'),
               ('first', 'first'),
            ]
    }

    form_args = {
        'ldns': {
            'validators': [Required()]
        },
        'dm': {
            'validators': [Required()]
        }
    }

    #form_ajax_refs = {
    #    'ldns': {
    #        'fields': (models.Ldns.addr)
    #    }
    #}

    #def ldns_choices():
    #    #return [ ldns.addr for ldns in models.Ldns.query.all() ]
    #    return models.Ldns.query.all()


    #form_extra_fields= dict(
    #    #dns=QuerySelectMultipleField(
    #    #dns=MyQuerySelectMultipleField(
    #    #    label='DNS server',
    #    #    query_factory=ldns_choices,
    #    #    validators=[Required()],
    #    #)

    #    dns=Select2TagsField(label='DNS Server',validators=[Required()]),
    #)
