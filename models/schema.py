import datetime
from db import db
from flask_login import UserMixin
from sqlalchemy import ForeignKey


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    town_city = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(10), nullable=True)
    invoice = db.relationship('Invoice',cascade="all,delete",backref="customer")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price =  db.Column(db.Integer, nullable=False)
    iteam = db.relationship('Iteam',cascade="all,delete",backref="product")

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('customer.id'))
    invoice_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    iteam = db.relationship('Iteam',cascade="all,delete",backref="invoice")

class Iteam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoiceid = db.Column(db.Integer, ForeignKey('invoice.id'))
    productid = db.Column(db.Integer, ForeignKey('product.id'))
    quantity = db.Column(db.Integer)