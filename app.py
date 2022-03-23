import csv

from flask import Flask, request, jsonify, render_template, url_for, redirect
from redis import Redis
from ProductController import *




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
    if request.method == 'POST':
        # Create variable for uploaded file
        f = request.files['fileupload']

        # store the file contents as a string
        fstring = f.read()

        # create list of dictionaries keyed by header row
        csv_dicts = [{k: v for k, v in row.items()} for row in csv.DictReader(fstring.splitlines(), skipinitialspace=True)]



        # do something list of dictionaries
        a = Products()
        for i in csv_dicts:
            a.createCsvProducts(csv_dicts[i]['name'], csv_dicts[i]['default_code'], csv_dicts[i]['list_price'], csv_dicts[i]['company_id'])
    return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
