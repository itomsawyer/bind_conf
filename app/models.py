# coding: utf-8
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy

from app import db, login_manager


#dns_forwarders_table = db.Table('dns_forwarders', db.Model.metadata,
#                           db.Column('ldns_id', db.Integer, db.ForeignKey('ldns.id')),
#                           db.Column('zone_id', db.Integer, db.ForeignKey('dns_forward_zone.id'))
#                           )

class DnsForwardZone(db.Model):
    __tablename__ = 'dns_forward_zone'

    id = db.Column(db.Integer, primary_key=True)
    dm = db.Column(db.String(255), unique=True)
    typ = db.Column(db.String(16), nullable=False, server_default=db.text("'only'"))

    ldnsList = association_proxy("dns_fwds","ldns")
    #ldns = db.relationship('Ldns', secondary=DnsForwarder)


class DnsForwarder(db.Model):
    __tablename__ = 'dns_forwarders'

    id = db.Column(db.Integer, primary_key=True)
    zone_id = db.Column(db.ForeignKey(u'dns_forward_zone.id', ondelete=u'CASCADE', onupdate=u'CASCADE'), index=True)
    ldns_id = db.Column(db.ForeignKey(u'ldns.id'), index=True)

    zone = db.relationship(DnsForwardZone, backref=db.backref("dns_fwds",cascade="all, delete-orphan"))
    ldns = db.relationship(u'Ldns')
    #ldns_addr = association_proxy("ldns","addr")

    def __init__(self, ldns=None):
        print ("init ldns", ldns)
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


    def __init__(self, ):
        print("init wtf", wtf)


    def __str__(self):
        return self.addr

    def __repr__(self):
        return 'Ldns(%s)' % repr(self.addr)


