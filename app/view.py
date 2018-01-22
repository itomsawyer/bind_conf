# -*- coding:utf-8 -*-
import os
import StringIO

from flask_admin.contrib import sqla
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField, QuerySelectField
from flask_admin.form.fields import Select2TagsField
from flask_admin.form import Select2Widget
from wtforms.validators import DataRequired,NumberRange

from . import models
from flask import url_for, redirect, render_template, request, abort
from flask_admin import BaseView, expose
from flask_security import current_user

from .validator import *

from app import db

import threading
lock = threading.Lock()

def is_accessible(roles_accepted=None, user=None):
    user = user or get_current_user()
    # uncomment if "admin" has access to everything
    # if user.has_role('admin'):
    #     return True
    if roles_accepted:
        accessible = any(
            [user.has_role(role) for role in roles_accepted]
        )
        return accessible

    return True

class Roled(object):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        roles_accepted = getattr(self, 'roles_accepted', None)
        return is_accessible(roles_accepted=roles_accepted, user=current_user)

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))

class ActionView(Roled, BaseView):
    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        super(ActionView, self).__init__(*args, **kwargs)

class PermView(Roled, sqla.ModelView):
    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        super(PermView, self).__init__(*args, **kwargs)

class BindConfForwarders():
    ldns = []
    policy = ""

    def __init__(self, policy, ldns=[]):
        self.policy = policy
        self.ldns = ldns

    def SetPolicy(self, policy):
        self.policy=policy

    def AddLdns(self, ldns):
        if not ldns in self.ldns:
            self.ldns.append(ldns)

class BindConfView():
    def __init__(self, name, prio=0):
        self.ipnets = []
        self.name = name
        self.prio = prio
        self.zones = {}

    def SetName(self, name):
        self.name = name

    def SetPrio(self, prio):
        self.prio = prio

    def AddIpnet(self, ipnet):
        if not ipnet in self.ipnets:
            self.ipnets.append(ipnet)

    def AddForwarder(self, zone, fwd, fwd_policy):
        if not zone in self.zones:
            self.zones[zone] = BindConfForwarders(policy=fwd_policy)

        self.zones[zone].AddLdns(fwd)

class BindConf():
    def __init__(self):
        self.conf = {}

    def AddView(self, name, prio):
        if not name in self.conf:
            self.conf[name] = BindConfView(name=name,prio=prio)

    def AddIpnet(self, name, ipnet):
        if name in self.conf:
            self.conf[name].AddIpnet(ipnet)

    def AddForwarder(self, name, zone, fwd, fwd_policy):
        if name in self.conf:
            self.conf[name].AddForwarder(zone, fwd, fwd_policy)

class SubmitView(ActionView):
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
            views = models.DnsForwardIpnets.query.order_by('prio').all();
            dfs = models.DnsForwarders.query.all()

            bc = BindConf()
            for v in views:
                bc.AddView(v.name,v.prio)
                bc.AddIpnet(v.name,v.ipnet)
            for fw in dfs:
                bc.AddForwarder(fw.view_name, fw.dm_zone, fw.ldns_addr, fw.fwd_policy)


            s = StringIO.StringIO()

            sorted_conf = sorted(bc.conf.items(), key=lambda x: x[1].prio)
            for item in sorted_conf:
                view = item[1]

                s.write("view \"%s\" {\n" % view.name)
                s.write("\tmatch-clients {\n")
                for ipnet in view.ipnets:
                    s.write("\t\t%s;\n" % ipnet)
                s.write("\t};\n")


                for zone in view.zones:
                    fwders = view.zones[zone]

                    s.write("\n")
                    s.write("\tzone \"%s\" IN {\n" % zone)
                    s.write("\t\ttype forward;\n")
                    s.write("\t\tforward %s;\n" % fwders.policy)
                    s.write("\t\tforwarders {\n")
                    for addr in fwders.ldns:
                        s.write("\t\t\t%s;\n" % addr)
                    s.write("\t\t};\n")
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

class UserView(PermView):
    column_labels = dict(email=u'用户名', active=u"激活", roles=u"角色",password=u"密码")
    column_list = ('email','active','roles')
    column_searchable_list = ('email','active','roles.name')
    column_sortable_list = (('roles','roles.name'), 'email','active')
    form_excluded_columns = ['last_name', 'first_name','confirmed_at']

    form_args = {
        'active': {
            'validators': [DataRequired()]
        },
        'roles': {
            'validators': [DataRequired()]
        },
        'password': {
            'validators': [DataRequired()]
        },
        'email': {
            'validators': [DataRequired()],
            'filters': [my_strip_filter]
        }
    }


class DnsForwardZoneGrpView(PermView):
    column_labels = dict(name=u'域名组', disabled=u"状态", dns_forward_zones=u"域名")
    column_searchable_list = ('name','disabled')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

    form_args = {
        'disabled': {
            'validators': [DataRequired()]
        },
        'name': {
            'validators': [DataRequired()],
            'filters': [my_strip_filter]
        }
    }


class DnsForwardZoneView(PermView):
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

    form_args = {
        'typ': {
            'validators': [DataRequired()]
        },
        'grp': {
            'validators': [DataRequired()]
        },
        'disabled': {
            'validators': [DataRequired()]
        },
        'name': {
            'validators': [DataRequired()],
            'filters': [my_strip_filter]
        }
    }



class DnsForwardIpnetGrpView(PermView):
    column_labels = dict(name=u'源地址组', disabled=u"状态", prio=u"优先级",dns_forward_ipnets=u'源地址段')
    column_searchable_list = ('name','disabled','prio',models.DnsForwardIpnet.ipnet)
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

    form_args = {
        'active': {
            'validators': [DataRequired()]
        },
        'prio': {
            'validators': [DataRequired(),NumberRange(0,100,u'合法优先级取值0-100')]
        },
        'disabled': {
            'validators': [DataRequired()]
        },
        'name': {
            'validators': [DataRequired()],
            'filters': [my_strip_filter]
        }
    }


class DnsForwardIpnetView(PermView):
    column_labels = dict(grp=u'源地址组', disabled=u"状态",ipnet=u'源地址段')
    column_sortable_list = (('grp','grp.name'), 'ipnet','disabled')
    column_searchable_list = (models.DnsForwardIpnetGrp.name, 'disabled','ipnet')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

    form_args = {
        'grp': {
            'validators': [DataRequired()]
        },
        'disabled': {
            'validators': [DataRequired()]
        },
        'ipnet': {
            'validators': [DataRequired(),NetAddr()],
        }
    }


class DnsForwarderView(PermView):
    column_labels = dict(disabled=u"状态",ldns=u"DNS服务器",ipnet_grp=u"源地址组",zone_grp=u"域名组")
    column_sortable_list = (('zone_grp','zone_grp.name'), ('ipnet_grp','ipnet_grp.name'),('ldns','ldns.name'),('ldns','ldns.addr'),'disabled')
    column_searchable_list = (models.DnsForwardIpnetGrp.name,models.DnsForwardZoneGrp.name, models.Ldns.addr, 'disabled')
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }


    form_args = {
        'ldns': {
            'validators': [DataRequired()]
        },
        'ipnet_grp': {
            'validators': [DataRequired()]
        },
        'zone_grp': {
            'validators': [DataRequired()]
        },
        'disabled': {
            'validators': [DataRequired()]
        },
    }


class LdnsView(PermView):
    column_labels = dict(addr=u"地址",name=u"名称",disabled=u"状态",status=u"可用性")
    column_searchable_list = ('disabled','name','addr','status')
    form_excluded_columns = ['status']
    form_choices = {
            'disabled': [
               ('0',u'启用'),
               ('1',u'禁用'),
            ]
    }

    form_args = {
        'addr': {
            'validators': [DataRequired(),IPAddr()]
        },
        'name': {
            'validators': [DataRequired()],
            'filters':[my_strip_filter],
        },
        'disabled': {
            'validators': [DataRequired()]
        },
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
