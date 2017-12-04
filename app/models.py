from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class DnsForwarder(db.Model):
    __tablename__ = 'dns_forwarder'

    id = db.Column(db.BigInteger, primary_key=True)
    dm = db.Column(db.String(255), nullable=False)
    dns = db.Column(db.String(255), nullable=False)
    typ = db.Column(db.String(16), nullable=False, server_default=db.text("'only'"))


    def __str__(self):
        return self.dm + " " + self.dns


class Ldns(db.Model):
    __tablename__ = 'ldns'

    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    addr = db.Column(db.String(255), nullable=False)

    def __str__(self):
        return self.addr


