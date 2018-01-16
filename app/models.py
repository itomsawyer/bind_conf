# coding: utf-8
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, login_manager

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

    def __str__(self):
        return self.name + "-" + self.addr

    def __repr__(self):
        return self.name + "-" + self.addr


