from flask import Flask, request, jsonify, render_template, url_for, redirect
from redis import Redis
from ProductController import *
import pandas as pd



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


def parseCSV(filePath):
    a = Products()
    # CVS Column Names
    col_names = ['name', 'default_code', 'list_price', 'company_id']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None)
    # Loop through the Rows
    for i, row in csvData.iterrows():
        a.createCsvProducts(row['name', row['default_code'], row['list_price'], row['company_id']])


# Get the uploaded files
@app.route("/CSVproductsAdded", methods=['POST'])
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
          # save the file

      parseCSV(redirect(url_for('index')))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
