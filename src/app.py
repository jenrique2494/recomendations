from flask import Flask
import pandas as pd
import numpy as np
from flask import jsonify
from recomendacion import recomendations
from flask import jsonify
from flask import request
#base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/laravel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
ma=Marshmallow(app)

class Banks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70),unique=True)
    description = db.Column(db.String(100))

    def __init__(self,name,description):
        self.name = name
        self.description = description




class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name','description')

task_schema= TaskSchema()
tasks_schema= TaskSchema(many=True)

@app.route('/products')
def getProducts():
    return 'datos'

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    datos=recomendations(product_name)
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

if __name__=='__main__':
    app.run(debug=True,port=4000)