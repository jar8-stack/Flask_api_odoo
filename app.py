import csv
import json

from flask import Flask, request, jsonify, render_template, url_for, redirect
from redis import Redis
from ProductController import *
import codecs
from flask import Flask, request

import smtplib, ssl

app = Flask(__name__)
redis = Redis(host='redis', port=6379)


@app.route('/')
def hello():
    return render_template('login.html')


@app.route('/recuperarPassword')
def recuperarView():
    return render_template('recuperarPassword.html')


@app.route('/recuperarPasswordController', methods=['POST', 'GET'])
def recuperarController():
    if request.method == 'POST':
        email = request.form['email']



        return render_template('login.html')


@app.route('/viewEpecificProduct', methods=['POST'])
def viewEspecificProduct():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:

            idProducto = request.form['idProductViz']
            a = Products()

            producto = a.getEspecificProduct(idProducto)


            return render_template('especificProduct.html', len=len(producto), Products=producto)



@app.route('/logOut', methods=['POST', 'GET'])
def logOut():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        json_object["usuarios"]["isLogged"] = False
        a_file = open("db/users.json", "w")
        json.dump(json_object, a_file)
        return render_template('login.html')

    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)
    a_file.close()


@app.route('/listaProductos', methods=['POST', 'GET'])
def productList():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if str(json_object["usuarios"]["correo"]) == email and str(json_object["usuarios"]["password"]) == password:
            json_object["usuarios"]["isLogged"] = True

            a_file = open("db/users.json", "w")
            json.dump(json_object, a_file)
            a = Products()
            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

        else:
            return render_template('login.html')

        a_file.close()

    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)


@app.route('/addProducts', methods=['POST', 'GET'])
def addProducts():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            nombreProducto = request.form['name']
            defaultCode = request.form['defaultCode']
            precio = request.form['precio']
            idCompany = request.form['idCompany']

            a = Products()
            a.createCsvProducts(nombreProducto, defaultCode, precio, idCompany)

            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()
            return render_template('addProducts.html', len=len(arrayProducts), Products=arrayProducts)

    a_file.close()


@app.route('/Dproducts')
def Dproducts():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if not json_object["usuarios"]["isLogged"]:
        return render_template('login.html')
    else:
        return render_template('deleteProducts.html')
    a_file.close()


@app.route('/deleteProducts', methods=['POST', 'GET'])
def deleteProducts():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            idProducto = request.form['idProducts']

            a = Products()
            a.deleteProduct(idProducto)

            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)
    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()
            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    a_file.close()


# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/CSVproducts')
def CSVproducts():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if not json_object["usuarios"]["isLogged"]:
        return render_template('login.html')
    else:
        return render_template('createCsvProducts.html')
    a_file.close()


# Get the uploaded files
@app.route("/CSVproductsAdded", methods=['POST', 'GET'])
def uploadFiles():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    data = []
    if request.method == "POST":
        a_file = open("db/users.json", "r")
        json_object = json.load(a_file)
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
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
    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()
            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    a_file.close()


@app.route("/UpdateProducts", methods=['POST', 'GET'])
def updateView():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            idProducto = request.form['idProduct']
            nombreProducto = request.form['nameProduct']
            precioProducto = request.form['priceProduct']
            company = request.form['companyProduct']

            dictDatos = {'id': idProducto, 'nombre': nombreProducto, 'precio': precioProducto, 'company': company}

            return render_template('updateProducts.html', datosProducto=dictDatos)
    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()
            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    a_file.close()


@app.route('/UpdateProductFinal', methods=['POST', 'GET'])
def updateFinal():
    a_file = open("db/users.json", "r")
    json_object = json.load(a_file)
    if request.method == 'POST':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            idProducto = request.form['idProduct']
            nombreProducto = request.form['nameProduct']
            precioProducto = request.form['priceProduct']
            company = request.form['companyProduct']

            a = Products()

            a.updateProduct(idProducto, nombreProducto, precioProducto)

            arrayProducts = a.getProducts()

            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    if request.method == 'GET':
        if not json_object["usuarios"]["isLogged"]:
            return render_template('login.html')
        else:
            a = Products()
            arrayProducts = a.getProducts()
            return render_template('listado_productos.html', len=len(arrayProducts), Products=arrayProducts)

    a_file.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
