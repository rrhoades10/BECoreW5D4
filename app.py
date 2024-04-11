from flask import Flask, jsonify, request
# Flask - everything we need for running flask
# jsonify - transform python objects to be displayed the browser or postman
# request - HTTP requset handling
from flask_sqlalchemy import SQLAlchemy
# SQLAlchemy is the Object Relational Mapper - any functionality for converting python classes to SQL tables
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# DeclarativeBase - provides base model functionality to create SQL tables from Python Classes
# All classes that become tables will inherit this class
# Mapped - provides a column for our table while declaring the python type and an attribute for the class
# python types are converted to SQL types like varchar, int, etc..
# mapped_column - set our column and allow us to set any constraints for that column
from flask_marshmallow import Marshmallow
# Marshmallow - serializes and deserializes JSON objects so we can interact with them as python dictionaries
from marshmallow import fields
# fields allows us to create a data shape or type for incoming data to adhere to
from typing import List
# give us a type of empty list that we can use as placeholder for a collection of relationships
# creating a one to many relationship, where One customer would have a collection or List of Orders
import datetime 
# give us access to the date type from datetime module



app = Flask(__name__)
#                                                                user  password      host       db name
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:Buttmuffin3!@localhost/e_commerce_db2"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

# creating our classes that will become tables in sql
# Models

class Customer(Base):
    __tablename__ = "Customers" #what the name of the table will be in sql
    customer_id: Mapped[int] = mapped_column(primary_key=True)
    #                                     alotting 255 characters for this specific string
    name: Mapped[str] = mapped_column(db.String(255), nullable = False)
    email: Mapped[str] = mapped_column(db.String(320))
    phone: Mapped[str] = mapped_column(db.String(15))
    # Creating a One-to-one relationship with the CustomerAccount
    # One day I will show up as a foreign key in the CustomerAccount Table
    customer_account: Mapped["CustomerAccount"] = db.relationship(back_populates="customer")
    # One-to-Many: Customer to Order
    # one day I will show up as a foreign key in the orders table
    orders: Mapped[List["Order"]] = db.relationship(back_populates="customer")

class CustomerAccount(Base):
    __tablename__ = "Customer_Accounts"
    account_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable = False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.customer_id'))
    # One-to-one:
    customer: Mapped["Customer"] = db.relationship(back_populates="customer_account")

# association (join) table for managing many-to-many relationships
order_product= db.Table(
    "Order_Product",
    Base.metadata, #also the same as DeclarativeBase
    db.Column("order_id", db.ForeignKey("Orders.order_id"), primary_key=True),
    db.Column("product_id", db.ForeignKey("Products.product_id"), primary_key=True)
)

class Order(Base):
    __tablename__ = "Orders"
    order_id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.customer_id'))
    # Many-to-One:
    # to establish a bidirectional relationshop in one-to-many relationshops, where the reverse side is many to one 
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    # many-to-many: Products and Orders
    products: Mapped[List["Product"]] = db.relationship(secondary=order_product)

class Product(Base):
    __tablename__ = "Products"
    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)

# Initialize the database and create tables
with app.app_context():
    # db.drop_all()
    db.create_all()

# Define Customer Schema
# Define the schema for a single customer(with optional 'id')
class CustomerSchema(ma.Schema):
    customer_id = fields.Integer(required=False)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("customer_id", "name", "email", "phone")

# Schema for many customers with a required id
class CustomersSchema(ma.Schema):
    customer_id = fields.Integer(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("customer_id", "name", "email", "phone")

# instantiate our CustomerSchemas
# GET, POST, PUT, DELETE
# Retrieve, Create, Update, Delete
customer_schema = CustomerSchema() # Create, Update, Get One
customers_schema = CustomerSchema(many=True) # Get all
# No schema for delete because theres not transfer of data through an HTTP request

# Product Schema
class ProductSchema(ma.Schema):
    product_id = fields.Integer(required=False)
    name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ("product_id", "name", "price")

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)








    


    


   

@app.route("/")
def home():
    return "REEEEEEEEEEEEEEEEEEEEE"



if __name__ == "__main__":
    app.run(debug=True)