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


class DnsForwardZoneView(sqla.ModelView):
    column_list = ('dm', 'ldnsList', 'typ')
    column_searchable_list = ('dm','typ', 'ldnsList.addr')
    #column_filters = ['dm','ldnsList.addr','typ']
    column_labels = dict(dm=u'域名', typ=u'转发策略', ldnsList=u"DNS服务器",dns_fwds=u"DNS Forwarder")

    #can_export = True

    form_columns = ('dm', 'ldnsList')

    #form_choices = {
    #        'typ': [
    #           ('only', 'only'),
    #           ('first', 'first'),
    #        ]
    #}

    form_args = {
        'ldnsList': {
            'validators': [DataRequired()]
        },
        'dm': {
            'validators': [DataRequired()],
            'filters': [my_strip_filter]
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
