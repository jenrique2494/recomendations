from flask import Flask
import pandas as pd
import numpy as np
from flask import jsonify
from recomendacion import recomendations
from buscador_principal import buscador_principal
from filtraje import filtraje
from flask import jsonify
from flask import request
#base de datos
'''from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema, fields
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_serializer import SerializerMixin
from marshmallow_sqlalchemy.fields import Nested
from sqlalchemy import and_, or_

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/laravel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
engine = create_engine('mysql+pymysql://root@localhost/laravel', echo = True)
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

db=SQLAlchemy(app)
ma=Marshmallow(app)


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


'''class ProductImage(db.Model,SerializerMixin):
    __tablename__ = 'product_image'
    serialize_only = ('id', 'product_id', 'image_id', 'products', 'images')
    serialize_rules = ('-images.products.images','-products.images.products',)

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))

    product = relationship(Product, backref=backref("product_image", cascade="all, delete-orphan"))
    image = relationship(Image, backref=backref("product_image", cascade="all, delete-orphan"))

    def __init__(self,src,products,images):
        self.products = products
        self.images = images
'''
class SmartNested(Nested):
    def serialize(self, attr, obj, accessor=None):
        if attr not in obj.__dict__:
            return {"id": int(getattr(obj, attr + "_id"))}
        return super(SmartNested, self).serialize(attr, obj, accessor)
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','description')

task_schema= TaskSchema()
tasks_schema= TaskSchema(many=True)

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

'''

@app.route('/products')
def getProducts():
    return 'datos'

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    datos=buscador_principal(product_name)
    datos_recomendacion=json.dumps(datos)
    return datos_recomendacion

@app.route('/products',methods=['POST'])
def postProducts():
    all_products=Banks.query.all()
    lista_productos= tasks_schema.dump(all_products)
    producto_buscar={
        "name":request.json['name'],
        "description":request.json['description'],
    }
    lista_productos_json=json.dumps(lista_productos)

    datos=recomendations(producto_buscar,lista_productos_json)
    datos_recomendacion=json.dumps(datos)
    return datos_recomendacion
#buscador_python
@app.route('/search/products',methods=['POST'])
def postSearchProducts():
    #listas de filtros
    lista_marca_json=request.json['marks']
    lista_subcategoria_json=request.json['subcategories']
    lista_factories_json=request.json['factories']
    lista_categories_json=request.json['categories']

    filter_group = filtraje(lista_marca_json,lista_subcategoria_json,lista_factories_json,lista_categories_json,Mark,Subcategory,Factory,Category,Product)

    #filtraje por join
    all_products=session.query(Product)\
        .join(Subcategory, Product.subcategories) \
        .join(Mark, Product.marks) \
        .join(Factory, Product.factories) \
        .join(Category, Subcategory.category) \
        .filter(and_(*filter_group)
        )\
        .all()

    #return json.dumps(all_products)
    #array=[]
    #for x in all_products:
     #   for y in x.images:
      #      array.append(y)

    lista_productos= products_schema.dump(all_products)
    #return  json.dumps(lista_productos)
    
    producto_buscar={
        "name":request.json['name'],
    }
    lista_productos_json=json.dumps(lista_productos)

    datos=buscador_principal(producto_buscar,lista_productos_json)

    datos_buscador=json.dumps(datos)

    return datos_buscador

    the_rock_movies = session.query(Product) \
    .join(Image, Product.images) \
    .all()
    print('###########################################')
    for product in the_rock_movies:
        print(f'el producto es in {product.images}')
        for image in product.images:
             print(f'la imagen es in {image.src}')
        print('')
    lista_productos= products_schema.dump(the_rock_movies)
    return  json.dumps(lista_productos)
    
if __name__=='__main__':
    app.run(debug=True,port=5000)