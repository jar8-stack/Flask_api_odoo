from odoo_clase import *


class Products(OdooConnection):

    def __init__(self, *args):
        super().__init__()


    def getProducts(self):
        products = self.models.execute_kw(self.db, self.uid, self.password,
                                          'product.template', 'search_read',
                                          [
                                              [
                                                  ['company_id', '=', 1]
                                              ]
                                          ], {
                                              'fields': []
                                          })

        return products


    def createCsvProducts(self, name, defaultCode, listPrice, companyId):
        id = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'create',
                                    [
                                        {
                                            'name': name,
                                            'default_code': defaultCode,
                                            'list_price': listPrice,
                                            'company_id': int(companyId)
                                        }
                                    ])
        print(id)


    def createProducts(self):
        id = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'create',
                                    [
                                        {
                                            'name': "celular api",
                                            'default_code': "123456",
                                            'list_price': "9999",
                                            'company_id': 1
                                        }
                                    ])
        print(id)


    def updateProduct(self):
        product = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'write', [[2], {
            'name': "Clase-Jueves Update",
            "price": "4567"
        }])
        print(product)


    def deleteProduct(self, idProducto):
        delete = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'unlink', [[int(idProducto)]])
        print(delete)