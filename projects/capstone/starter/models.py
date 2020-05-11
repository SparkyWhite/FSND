import os
from sqlalchemy import Table, Column, String, Integer, Boolean, Float, ForeignKey, create_engine
#from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()

def setup_db(app):
  ENV = 'dev'

  if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:muf72finS!$!@localhost:5432/capstone'
  elif ENV == 'testing':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:muf72finS!$!@localhost:5432/capstone_test'
  else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rfvooomtbpmdwy:bfe213aa639a9e596dc1c5898da8c86c9cd003beeb8cb3c794e7b995487f2031@ec2-18-206-84-251.compute-1.amazonaws.com:5432/d5niid1ojj6cao'

  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.app = app
  db.init_app(app)

def db_drop_and_create_all():
  db.drop_all()
  db.create_all()

class Customer(db.Model):
  __tablename__ = 'customer'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(25), nullable=False)
  state = db.Column(db.String(2), nullable=False)
  zipCode = db.Column(db.String(5), nullable=False)
  active = db.Column(db.Boolean, nullable=False)

  def __init__(self, name, address, city, state, zipCode, active):
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.zipCode = zipCode
    self.active = active

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'address': self.address,
      'city': self.city,
      'state': self.state,
      'zipCode': self.zipCode,
      'active': self.active}
  
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

class Employee(db.Model):
  __tablename__ = 'employee'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(120), nullable=False)
  city = db.Column(db.String(25), nullable=False)
  state = db.Column(db.String(2), nullable=False)
  zipCode = db.Column(db.String(5), nullable=False)
  position = db.Column(db.String(25), nullable=False)
  active = db.Column(db.Boolean, nullable=False)

  def __init__(self, name, address, city, state, zipCode, position, active):
    self.name = name
    self.address = address
    self.city = city
    self.state = state
    self.zipCode = zipCode
    self.position = position
    self.active = active

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'address': self.address,
      'city': self.city,
      'state': self.state,
      'zipCode': self.zipCode,
      'position': self.position,
      'active': self.active}

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()

""" class Order(db.Model):
  __tablename__ = 'order'
  id = Column(Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
  employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)

  # customer = db.relationship("Customer")#Why is this necessary???
  # employee = db.relationship("Employee")

  def __init__(self, customer_id, employee_id):
    self.customer_id = customer_id
    self.employee_id = employee_id

  def format(self):
    return {
      'id': self.id,
      'customer_id': self.customer_id,
      'employee_id': self.employee_id}

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()
 
  def delete(self):
    db.session.delete(self)
    db.session.commit() """

# class Item(db.Model):
#   __tablename__ = 'item'
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(100), nullable=False)
#   cost = db.Column(db.Float, nullable=False)
#   description = db.Column(db.String(255), nullable=False)
#   children = db.relationship('OrderItem', backref='item', cascade='all, delete-orphan', lazy=True)

#   def __init__(self, name, cost, description):
#     self.name = name
#     self.cost = cost
#     self.description = description

#   def format(self):
#     return {
#       'id': self.id,
#       'name': self.name,
#       'cost': self.cost,
#       'description': self.description}

#   def insert(self):
#     db.session.add(self)
#     db.session.commit()
  
#   def update(self):
#     db.session.commit()
  
#   def delete(self):
#     db.session.delete(self)
#     db.session.commit()

# class OrderItem(db.Model):
#   __tablename__ = 'orderItem'
#   id = db.Column(db.Integer, primary_key=True)
#   quantity = db.Column(db.Integer, nullable=False)
#   #item_id = db.Column(db.Integer, ForeignKey('item.id'), nullable=False)
#   item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='cascade'), nullable=False)
#   order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=False)

#   # item = db.relationship("Item")
#   # order = db.relationship("Order")

#   def __init__(self, quantity):
#     self.quantity = quantity

#   def format(self):
#     return {
#       'id': self.id,
#       'quantity': self.quantity}

#   def insert(self):
#     db.session.add(self)
#     db.session.commit()
  
#   def update(self):
#     db.session.commit()
  
#   def delete(self):
#     db.session.delete(self)
#     db.session.commit()