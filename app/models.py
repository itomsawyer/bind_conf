# coding: utf-8
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy


from app import db, login_manager

class DnsForwardIpnet(db.Model):
    __tablename__ = 'dns_forward_ipnet'

    id = db.Column(db.Integer, primary_key=True)
    ipnet = db.Column(db.String(45))
    disabled = db.Column(db.Integer)
    grp_id = db.Column(db.ForeignKey(u'dns_forward_ipnet_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)

    grp = db.relationship(u'DnsForwardIpnetGrp')


class DnsForwardIpnetGrp(db.Model):
    __tablename__ = 'dns_forward_ipnet_grp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45))
    prio = db.Column(db.Integer, nullable=False, server_default=db.text("'10'"))
    disabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    def __repr__(self):
        return self.name


class DnsForwardZone(db.Model):
    __tablename__ = 'dns_forward_zone'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True)
    typ = db.Column(db.String(45), nullable=False, server_default=db.text("'only'"))
    grp_id = db.Column(db.ForeignKey(u'dns_forward_zone_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    grp = db.relationship(u'DnsForwardZoneGrp')


class DnsForwardZoneGrp(db.Model):
    __tablename__ = 'dns_forward_zone_grp'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    #typ = db.Column(db.String(16), nullable=False, server_default=db.text("'only'"))
    disabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    def __repr__(self):
        return self.name

class DnsForwarder(db.Model):
    __tablename__ = 'dns_forwarders'

    id = db.Column(db.Integer, primary_key=True)
    zone_grp_id = db.Column(db.ForeignKey(u'dns_forward_zone_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ipnet_grp_id = db.Column(db.ForeignKey(u'dns_forward_ipnet_grp.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False, index=True)
    ldns_id = db.Column(db.ForeignKey(u'ldns.id'), nullable=False,  index=True)
    disabled = db.Column(db.Integer, nullable=False, server_default=db.text("'0'"))

    zone_grp = db.relationship(u'DnsForwardZoneGrp')
    ipnet_grp = db.relationship(u'DnsForwardIpnetGrp')
    ldns = db.relationship(u'Ldns')

    def __init__(self, ldns=None):
        self.ldns = ldns


    def __str__(self) :
        return self.ldns.name + " " +  self.ldns.addr



class Ldns(db.Model):
    __tablename__ = 'ldns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(127), nullable=False, unique=True)
    addr = db.Column(db.String(40), nullable=False)
    typ = db.Column(db.String(32), nullable=False, server_default=db.text("'A'"))
    enable = db.Column(db.Integer, nullable=False, server_default=db.text("'1'"))
    unavailable = db.Column(db.SmallInteger, nullable=False, server_default=db.text("'0'"))
    checkdm = db.Column(db.String(255))


    def __str__(self):
        return self.addr

    def __repr__(self):
        return 'Ldns(%s)' % repr(self.addr)


