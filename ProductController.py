from odoo_clase import *


class Products(OdooConnection):

    def __init__(self, *args):
        super().__init__()

    def getEspecificProduct(self, idProducto):
        products = self.models.execute_kw(self.db, self.uid, self.password,
                                          'product.template', 'search_read',
                                          [
                                              [
                                                  ['id', '=', int(idProducto)]
                                              ]
                                          ], {
                                              'fields': []
                                          })

        return products

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

    def updateProduct(self, idProduct, name, listPrice):
        product = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'write',
                                         [[int(idProduct)], {
                                             'name': str(name),
                                             "price": str(listPrice)
                                         }])
        print(product)

    def deleteProduct(self, idProducto):
        delete = self.models.execute_kw(self.db, self.uid, self.password, 'product.template', 'unlink',
                                        [[int(idProducto)]])
        print(delete)
