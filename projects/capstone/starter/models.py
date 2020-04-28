import os
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

#database_filename = "database.db"
#project_dir = os.path.dirname(os.path.abspath(__file__))
#database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = "postgresql://postgres:muf72finS!$!@localhost:5432/capstone"

db = SQLAlchemy()

def setup_db(app):
  app.config["SQLALCHEMY_DATABASE_URI"] = database_path
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
  db.app = app
  db.init_app(app)

class Customer(db.Model):
  __tablename__ = 'customer'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  address = Column(String(120), nullable=False)
  city = Column(String(25), nullable=False)
  state = Column(String(2), nullable=False)
  zipCode = Column(String(5), nullable=False)
  active = Column(Boolean, nullable=False)

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

class Employee(db.Model):
  __tablename__ = 'employee'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  address = Column(String(120), nullable=False)
  city = Column(String(25), nullable=False)
  state = Column(String(2), nullable=False)
  zipCode = Column(String(5), nullable=False)
  position = Column(String(25), nullable=False)
  active = Column(Boolean, nullable=False)

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

class Order(db.Model):
  __tablename__ = 'order'
  id = Column(Integer, primary_key=True)
  customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
  employee_id = Column(Integer, ForeignKey('employee.id'), nullable=False)

  customer = relationship("Customer")#Why is this necessary???
  employee = relationship("Employee")

  def __init__(self, customer_id, employee_id):
    self.customer_id = customer_id
    self.employee_id = employee_id

  def format(self):
    return {
      'id': self.id,
      'customer_id': self.customer_id,
      'employee_id': self.employee_id}

class Item(db.Model):
  __tablename__ = 'item'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  cost = Column(Float, nullable=False)
  description = Column(String(255), nullable=False)

  def __init__(self, name, cost, description):
    self.name = name
    self.cost = cost
    self.description = description

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'cost': self.cost,
      'description': self.description}

class OrderItem(db.Model):
  __tablename__ = 'orderItem'
  id = Column(Integer, primary_key=True)
  quantity = Column(Integer, nullable=False)
  item_id = Column(Integer, ForeignKey('item.id'), nullable=False)
  order_id = Column(Integer, ForeignKey('order.id'), nullable=False)

  item = relationship("Item")#why???
  order = relationship("Order")

  def __init__(self, quantity):
    self.quantity = quantity

  def format(self):
    return {
      'id': self.id,
      'quantity': self.quantity}