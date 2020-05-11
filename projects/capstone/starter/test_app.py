import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Customer, Employee#, Order, Item, OrderItem#, db, db_drop_and_create_all
from flask import Flask, request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from models import db
import datetime
import base64

class FlowerShopTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:muf72finS!$!@localhost:5432/capstone_test"
        setup_db(self.app)

        self.mgrtoken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UZEROVEU0TVRKQ05EWXpOMEUwTWpNNE0wRTJOalpFTmpVNU9EUTBRVVpGTkRFd01FRXdSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qaWU1LTEzbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNzE0ZmYxY2MxYWMwYzE0OThhYTNjIiwiYXVkIjoiaHR0cHM6Ly91ZGFjaXR5LWZsb3dlci1zaG9wLmhlcm9rdWFwcC5jb20iLCJpYXQiOjE1ODkxNzMxNzUsImV4cCI6MTU4OTI1OTU3NSwiYXpwIjoicWRGN3p1azlmVFpySEhsU1IyalpSNG5mWmJuOVptMlUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDpjdXN0b21lciIsImFkZDplbXBsb3llZSIsImFkZDpvcmRlciIsImRlbGV0ZTpjdXN0b21lciIsImRlbGV0ZTplbXBsb3llZSIsImRlbGV0ZTpvcmRlciIsInBhdGNoOmN1c3RvbWVyIiwicGF0Y2g6ZW1wbG95ZWUiLCJ2aWV3OmN1c3RvbWVyIiwidmlldzpjdXN0b21lcnMiLCJ2aWV3OmVtcGxveWVlcyIsInZpZXc6b3JkZXIiXX0.jjCMirsjFpaz7Hgxv0YDFnYSSpMO6woqdMVwy5eO5nu2gj_T1SqTg14oZwSQat7tDWjS_658gBDZa9LkW5Wajd-9y576odlLUONdvKbM8qsOVhW2NWj5UEZF3RMWZM-6uOXIBLp5DaUODbzprvrNMh1WNz2-sJrL687rI5J6sTAf5IMSdX_SAZgExMijpQH18Khoa7c96bice4iaArifyQyYoGRs5o3P3jGiHx3BjFvt99NAJ1qq-aqESh_DTCAEcyD9gy8Jh4JKwi1aSbjcyv99rM1XDbe1asZlLGmYkcPaKJg7JqtgQvSyVfsX08R57JLkCOn4btaDirb-63ycXA'
        self.emptoken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UZEROVEU0TVRKQ05EWXpOMEUwTWpNNE0wRTJOalpFTmpVNU9EUTBRVVpGTkRFd01FRXdSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qaWU1LTEzbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNzE1MjYxY2MxYWMwYzE0OThhYWE0IiwiYXVkIjoiaHR0cHM6Ly91ZGFjaXR5LWZsb3dlci1zaG9wLmhlcm9rdWFwcC5jb20iLCJpYXQiOjE1ODkxNzMyNjcsImV4cCI6MTU4OTI1OTY2NywiYXpwIjoicWRGN3p1azlmVFpySEhsU1IyalpSNG5mWmJuOVptMlUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDpjdXN0b21lciIsImFkZDpvcmRlciIsImRlbGV0ZTpvcmRlciIsInBhdGNoOmN1c3RvbWVyIiwidmlldzpjdXN0b21lciIsInZpZXc6b3JkZXIiXX0.eYOViO1HujkQKjjfE-HbDVvqTArrP9r57p44ExOYwyBNdzOktQ-QGsVdBSAZW8a3F_AyN221d6TLd6ZntmnLX-WKUuvBd9LxCTQdSuGaY1ub3wjoUS5Gj7zRgmDF4Y8yCCbMCUzEdhSDrReJNCW0dM-q_Ansh2rzXOwK4cuuT98WZNEUyagOGsii2YFzkLfbqpLZMw73fwr4sEWIKt4lMxj-XAETXSeEysedqhWY2xTjazl6fpHwTk_M3sBjCWeYpOA-ozu3ek_9q7fJhid9MIa1oekXJSHwrXPHci_ESVI4B4PPKLLL2xP6HkwfBJQeSJ-EgE3CMNs2-t3Nlm4Lhg'
        self.csttoken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UZEROVEU0TVRKQ05EWXpOMEUwTWpNNE0wRTJOalpFTmpVNU9EUTBRVVpGTkRFd01FRXdSQSJ9.eyJpc3MiOiJodHRwczovL2Rldi1qaWU1LTEzbi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViNzE1NTA1NGIxNGMwYzEyODlmZTM1IiwiYXVkIjoiaHR0cHM6Ly91ZGFjaXR5LWZsb3dlci1zaG9wLmhlcm9rdWFwcC5jb20iLCJpYXQiOjE1ODkxNzMzNDIsImV4cCI6MTU4OTI1OTc0MiwiYXpwIjoicWRGN3p1azlmVFpySEhsU1IyalpSNG5mWmJuOVptMlUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImFkZDpvcmRlciIsInZpZXc6b3JkZXIiXX0.nY0hYIjIrZ4Y2PDRlPYH0h6Wr8_Xcun4p-7kyAepA8Vt-PCHOjEvm832wuXQjFL3E9LxQYSXEqWXM_Jo9UM2HG8uLExLbDJeSAQYlJg3BAYgfi_ghGD4tBhCJcTSfzIZ8hzxj6pZRwvE7Ta4z19B05UJwm1MYKGk4XngMVoZTLoX57KFKygct3necTGygwJjdOEmCVCTDBTBQDMaTymlBs8BDQYXDv9IoSeQgat0OEbgebnkrZ0FjEIlmiwkW6mqGXX_m5tjYrEKh6aJIwXyRljE0_FaQyOpKKHZAkOfnzmRFYe59ecvGdpCYVGEuj2lUj7eNm42TTeJKigl8LNN5g'

        self.mgrheader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.mgrtoken}
        self.empheader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.emptoken}
        self.cstheader = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.csttoken}

        self.post_customer = {
            'name': 'Joe Schmo',
            'address': '123 Street',
            'city': 'your city',
            'state': 'BE',
            'zipCode': '23890',
            'active': True
        }

        self.post_employee = {
            'name': 'Joe Schmo',
            'address': '123 Street',
            'city': 'your city',
            'state': 'BE',
            'zipCode': '23890',
            'position': 'manager',
            'active': True
        }


        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    #Tests for success

    def test_create_customer(self):
        res = self.client().post('/customers', headers=self.mgrheader, json=self.post_customer)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'was added successfully')
        self.assertEqual(res.status_code, 200)

    def test_get_customer_list(self):
        res = self.client().get('/customers', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)
    
    def test_get_customer(self):
        res = self.client().get('/customers/5', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)
    
    def test_update_customer(self):
        res = self.client().patch('/customers/5', headers=self.mgrheader, json={'name': 'Test update name', 'address': 'new', 'city': 'new', 'state': 'VA', 'zipCode': '12345', 'active': 'true'})
        self.assertEqual(res.status_code, 200)
    
    def test_delete_customer(self):
        res = self.client().delete('/customers/7', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)
    
    def test_create_employee(self):
        res = self.client().post('/employees', headers=self.mgrheader, json=self.post_employee)
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'was added successfully')
        self.assertEqual(res.status_code, 200)

    def test_get_employee_list(self):
        res = self.client().get('/employees', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)
    
    def test_update_employee(self):
        res = self.client().patch('/employees/1', headers=self.mgrheader, json={'name': 'Test update name', 'address': 'new', 'city': 'new', 'state': 'VA', 'zipCode': '12345', 'position': 'cashier', 'active': 'true'})
        self.assertEqual(res.status_code, 200)
    
    def test_delete_employee(self):
        res = self.client().delete('/employees/2', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)
    

    #Failure testing

    def test_create_customer_fail(self):
        res = self.client().post('/customers', headers=self.mgrheader, json={'name': 'Only include name - but no other fields'})
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Please fill out all required fields and resubmit')

    def test_create_employee_fail(self):
        res = self.client().post('/employees', headers=self.mgrheader, json={'name': 'Only include name - but no other fields'})
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'Please fill out all required fields and resubmit')

    def test_get_customer_fail(self):
        res = self.client().get('/customers/100000', headers=self.mgrheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_update_customer_fail(self):
        res = self.client().patch('/customers/100000', headers=self.mgrheader, json=self.post_customer)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_delete_customer_fail(self):
        res = self.client().delete('/customers/100000', headers=self.mgrheader)
        self.assertEqual(res.status_code, 401)
    
    def test_create_employee_fail(self):
        res = self.client().post('/employees', headers=self.mgrheader, json={'name': 'Just the name'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)

    def test_update_employee_fail(self):
        res = self.client().patch('/employees/1000000', headers=self.mgrheader, json={'name': 'Test update name', 'address': 'new', 'city': 'new', 'state': 'VA', 'zipCode': '12345', 'position': 'cashier', 'active': 'true'})
        self.assertEqual(res.status_code, 200)
    
    def test_delete_employee_fail(self):
        res = self.client().delete('/employees/100000', headers=self.mgrheader)
        self.assertEqual(res.status_code, 200)

    #RBAC testing

    def test_create_customer_rbac_missing_header(self):
        res = self.client().post('/customers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
    
    def test_create_customer_rbac_no_permissions(self):
        res = self.client().post('/customers', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    def test_get_customer_list_missing_header(self):
        res = self.client().get('/customers')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_customer_list_no_permissions(self):
        res = self.client().get('/customers', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_customer_missing_header(self):
        res = self.client().patch('/customers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_customer_no_permissions(self):
        res = self.client().patch('/customers/1', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_customer_missing_header(self):
        res = self.client().delete('/customers/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_customer_no_permissions(self):
        res = self.client().delete('/customers/1', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
    
    def test_create_employee_missing_header(self):
        res = self.client().post('/employees/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_create_employee_no_permissions(self):
        res = self.client().post('/employees/1', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_employee_list_missing_header(self):
        res = self.client().get('/employees')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_get_employee_list_no_permissions(self):
        res = self.client().get('/employees', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_update_employee_missing_header(self):
        res = self.client().patch('/employees/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_update_employee_no_permissions(self):
        res = self.client().patch('/employees/1', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_delete_employee_missing_header(self):
        res = self.client().delete('/employees/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_delete_employee_no_permissions(self):
        res = self.client().delete('/employees/1', headers=self.cstheader)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()