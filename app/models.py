# coding: utf-8
from flask_login import UserMixin
from flask_security import UserMixin, RoleMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, login_manager

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email


#t_dns_forward_ipnet_view = db.Table(
#    'dns_forward_ipnet_view', db.metadata,
#    db.Column('name', db.String(45)),
#    db.Column('prio', db.Integer, server_default=db.FetchedValue()),
#    db.Column('ipnet', db.String(45))
#)

class DnsForwarders(db.Model):
    __tablename__ = 'dns_forwarders_view'

    view_name = db.Column('view_name', db.String(45),primary_key=True)
    view_prio = db.Column('view_prio', db.Integer, server_default=db.FetchedValue(),primary_key=True)
    dm_zone = db.Column('dm_zone',   db.String(255),primary_key=True)
    fwd_policy = db.Column('fwd_policy',db.String(45), server_default=db.FetchedValue())
    ldns_name = db.Column('ldns_name', db.String(45),primary_key=True)
    ldns_addr = db.Column('ldns_addr', db.String(45),primary_key=True)

class DnsForwardIpnets(db.Model):
    __tablename__  = 'dns_forward_ipnet_view'
    name = db.Column('name', db.String(45),primary_key=True)
    prio = db.Column('prio', db.Integer, server_default=db.FetchedValue())
    ipnet = db.Column('ipnet', db.String(45),primary_key=True)

#t_dns_forwarders_view = db.Table(
#    'dns_forwarders_view', db.metadata,
#    db.Column('view_name', db.String(45)),
#    db.Column('view_prio', db.Integer, server_default=db.FetchedValue()),
#    db.Column('dm_zone',   db.String(255)),
#    db.Column('fwd_policy',db.String(45), server_default=db.FetchedValue()),
#    db.Column('ldns_name', db.String(45)),
#    db.Column('ldns_addr', db.String(45))
#)

#import enum
#class Disabled(enum.Enum):
#    enabled = 0
#    disabled = 1


class DnsForwardIpnet(db.Model):
    __tablename__ = 'dns_forward_ipnet'

    id = db.Column(db.Integer, primary_key=True)
    ipnet = db.Column(db.String(45), nullable=False, unique=True)
    disabled = db.Column(db.Integer, nullable=False)
    #disabled = db.Column(db.Enum(Disabled), nullable=False)
    grp_id = db.Column(db.ForeignKey(u'dns_forward_ipnet_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    grp = db.relationship(u'DnsForwardIpnetGrp', primaryjoin='DnsForwardIpnet.grp_id == DnsForwardIpnetGrp.id', backref=u'dns_forward_ipnets')

    def __repr__(self):
        return self.ipnet


class DnsForwardIpnetGrp(db.Model):
    __tablename__ = 'dns_forward_ipnet_grp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    prio = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    def __repr__(self):
        return self.name


class DnsForwardZone(db.Model):
    __tablename__ = 'dns_forward_zone'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    typ = db.Column(db.String(45), nullable=False, server_default=db.FetchedValue())
    grp_id = db.Column(db.ForeignKey(u'dns_forward_zone_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    grp = db.relationship(u'DnsForwardZoneGrp', primaryjoin='DnsForwardZone.grp_id == DnsForwardZoneGrp.id', backref=u'dns_forward_zones')

    def __repr__(self):
        return self.name

class DnsForwardZoneGrp(db.Model):
    __tablename__ = 'dns_forward_zone_grp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    def __repr__(self):
        return self.name

class DnsForwarder(db.Model):
    __tablename__ = 'dns_forwarders'

    id = db.Column(db.Integer, primary_key=True)
    zone_grp_id = db.Column(db.ForeignKey(u'dns_forward_zone_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ipnet_grp_id = db.Column(db.ForeignKey(u'dns_forward_ipnet_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ldns_id = db.Column(db.ForeignKey(u'ldns.id'), nullable=False,  index=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    zone_grp = db.relationship(u'DnsForwardZoneGrp')
    ipnet_grp = db.relationship(u'DnsForwardIpnetGrp')
    ldns = db.relationship(u'Ldns')

    #def __init__(self, ldns=None):
    #    self.ldns = ldns

    #def __str__(self) :
    #    return self.ldns.name + " " +  self.ldns.addr



class Ldns(db.Model):
    __tablename__ = 'ldns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    addr = db.Column(db.String(45), nullable=False, unique=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


    def __repr__(self):
        return self.name + "-" + self.addr


