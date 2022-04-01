import csv

from flask import Flask, request, jsonify, render_template, url_for, redirect
from redis import Redis
from ProductController import *
import codecs

import os
from os.path import join, dirname, realpath

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def hello():
    a = Products()
    arrayProducts = a.getProducts()

    return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)


@app.route('/products')
def products():
    return render_template('addProducts.html')


@app.route('/addProducts', methods=['POST'])
def addProducts():
    if request.method == 'POST':
        nombreProducto = request.form['name']
        defaultCode = request.form['defaultCode']
        precio = request.form['precio']
        idCompany = request.form['idCompany']

        a = Products()
        a.createCsvProducts(nombreProducto, defaultCode, precio, idCompany)

        arrayProducts = a.getProducts()

        return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)


@app.route('/Dproducts')
def Dproducts():
    return render_template('deleteProducts.html')


@app.route('/deleteProducts', methods=['POST'])
def deleteProducts():
    if request.method == 'POST':
        idProducto = request.form['idProducts']

        a = Products()
        a.deleteProduct(idProducto)

        arrayProducts = a.getProducts()

        return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)


# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/CSVproducts')
def CSVproducts():
    return render_template('createCsvProducts.html')


# Get the uploaded files
@app.route("/CSVproductsAdded", methods=['POST'])
def uploadFiles():
    data = []
    if request.method == "POST":
        flask_file = request.files['fileupload']  # This line uses the same variable and worked fine
        if not flask_file:
            return 'Upload a CSV file'

        stream = codecs.iterdecode(flask_file.stream, 'utf-8')
        for row in csv.reader(stream, dialect=csv.excel):
            if row:
                data.append(row)

        data.pop(0)

        a = Products()
        for row in data:
            a.createCsvProducts(row[0], row[1], row[2], row[3])

    return "Succes"


@app.route("/UpdateProducts", methods=['POST'])
def updateView():
    if request.method == 'POST':
        idProducto = request.form['idProduct']
        nombreProducto = request.form['nameProduct']
        precioProducto = request.form['priceProduct']
        company = request.form['companyProduct']

        dictDatos= {'id':idProducto, 'nombre':nombreProducto, 'precio':precioProducto, 'company':company}

        return render_template('updateProducts.html', datosProducto=dictDatos)


@app.route('/UpdateProductFinal', methods=['POST'])
def updateFinal():
    if request.method == 'POST':
        idProducto = request.form['idProduct']
        nombreProducto = request.form['nameProduct']
        precioProducto = request.form['priceProduct']
        company = request.form['companyProduct']

        a = Products()
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
