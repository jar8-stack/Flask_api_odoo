import xmlrpc.client
import socket


class OdooConnection(object):
    url = None
    password = None
    user = None
    db = None
    uid = None
    models = None
    common = None

    def __init__(self, *args):
        self.url = "http://192.168.10.1:8069"
        self.password = "Serranosoto1"
        self.user = "saidserrano315@gmail.com"
        self.db = "sie_modelo"

        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))

        self.output = self.common.version()

        self.uid = self.common.authenticate(self.db, self.user, self.password, self.output)

        print(self.uid)