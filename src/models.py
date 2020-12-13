from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema, fields
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy.fields import Nested
from app import db, ma 

class Banks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70),unique=True)
    description = db.Column(db.Text)

    def __init__(self,name,description):
        self.name = name
        self.description = description

product_image = db.Table('product_image',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('images.id'), primary_key=True)
)
factory_product = db.Table('factory_product',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('factory_id', db.Integer, db.ForeignKey('factories.id'), primary_key=True)
)
mark_product = db.Table('mark_product',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('mark_id', db.Integer, db.ForeignKey('marks.id'), primary_key=True)
)
subcategory_product = db.Table('subcategory_product',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('subcategory_id', db.Integer, db.ForeignKey('subcategories.id'), primary_key=True)
)

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'
    serialize_only = ('id', 'name', 'description', 'images')
   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)
    description = db.Column(db.Text)
    images = relationship("Image", secondary=product_image)
    factories = relationship("Factory", secondary=factory_product)
    marks = relationship("Mark", secondary=mark_product)
    subcategories = relationship("Subcategory", secondary=subcategory_product)

    def __init__(self,id,name,description):
        self.id = id
        self.name = name
        self.description = description

class Image(db.Model, SerializerMixin):
    __tablename__ = 'images'
    serialize_only = ('id', 'src')

    id = db.Column(db.Integer, primary_key=True)
    src = db.Column(db.Text)

    def __init__(self,src):
        self.src = src
class Factory(db.Model, SerializerMixin):
    __tablename__ = 'factories'
    serialize_only = ('id', 'name')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)

    def __init__(self,name):
        self.name = name

class Mark(db.Model, SerializerMixin):
    __tablename__ = 'marks'
    serialize_only = ('id', 'name')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)

    def __init__(self,name):
        self.name = name

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'
    serialize_only = ('id', 'name')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)

    def __init__(self,name):
        self.name = name

class Subcategory(db.Model, SerializerMixin):
    __tablename__ = 'subcategories'
    serialize_only = ('id', 'name')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250),unique=True)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'))
    category = relationship("Category")

    def __init__(self,name,category_id,category):
        self.name = name
        self.category_id = category_id
        self.category = category


class ImageSchema(ma.SQLAlchemySchema):
    class Meta:
        model =Image
    src = ma.auto_field()

images_schema= ImageSchema()
images_schema= ImageSchema(many=True)

class FactorySchema(ma.SQLAlchemySchema):
    class Meta:
        model =Factory
    name = ma.auto_field()

factories_schema= FactorySchema()
factories_schema= FactorySchema(many=True)

class MarkSchema(ma.SQLAlchemySchema):
    class Meta:
        model =Factory
    name = ma.auto_field()

marks_schema= MarkSchema()
marks_schema= MarkSchema(many=True)

class CategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model =Category
    name = ma.auto_field()

categories_schema= CategorySchema()
categories_schema= CategorySchema(many=True)

class SubcategorySchema(ma.SQLAlchemySchema):
    class Meta:
        model =Subcategory
    name = ma.auto_field()
    category_id = ma.auto_field()
    category = Nested(CategorySchema)

subcategories_schema= SubcategorySchema()
subcategories_schema= SubcategorySchema(many=True)



class ProductSchema(ma.SQLAlchemySchema):
    class Meta:
        model =Product
    id = ma.auto_field()
    name = ma.auto_field()
    description = ma.auto_field(dump_only=False)
    images = Nested(ImageSchema,many=True)
    factories = Nested(FactorySchema,many=True)
    marks = Nested(MarkSchema,many=True)
    subcategories = Nested(SubcategorySchema,many=True)



products_schema= ProductSchema()
products_schema= ProductSchema(many=True)
