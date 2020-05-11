Udacity Flower Shop API

Motivation
    I wanted to create a project in a field I had previous experience in.  Originally, I wanted to add the ability to add orders and get their associated data as JSON
    objects, but due to work constraints, have run out of time.  I may come back and finish that functionality later.  For now, the API allows tracking customers and
    employees, and reporting information for both.

Notes
    Tokens for all users can be found at the top of test_app.py.
    Auth0 Domain Name: dev-jie5-13n.auth0.com
    JWT Signing Secret: mw7Q7eoRMDNFadXXFOoTZj6jT61w2Az77V4Gen8yo72aULMERHEHpsRAKjpXFDt4
    Auth0 Client ID: qdF7zuk9fTZrHHlSR2jZR4nfZbn9Zm2U

Testing

    To run tests:
    Set line 10 in models to "testing"
    py test_app.py

Deployment

    This app is deployed on Heroku https://udacity-flower-shop.herokuapp.com

Endpoints

    GET '/customers'
    GET '/customers/int:id'
    POST '/customers'
    PATCH '/customers/int:id'
    DELETE '/customers/int:id'
    GET '/employees'
    POST '/employees'
    PATCH '/employees/int:id'
    DELETE '/employees/int:id'

Following is the demonstration of each endpoint.

    GET '/customers'
        Get a list of all customers
        Returns a JSON object with all customers
        {
            "customerList": [
                {
                    "active": true,
                    "address": "123 Street",
                    "city": "your city",
                    "id": 2,
                    "name": "Joe Schmo",
                    "state": "BE",
                    "zipCode": "23890"
                }
            ]
        }

    GET '/customers/int:id'
        Get one customer object
        Returns a JSON object with one customer's information
        {
            "customer": {
                "active": true,
                "address": "123 Street",
                "city": "your city",
                "id": 2,
                "name": "Joe Schmo",
                "state": "BE",
                "zipCode": "23890"
            }
        }

    POST '/customers'
        Add a customer to the database
        Input data needed (JSON):
            {
                "name" : "First Employee",
                "address" : "Johnsons Fence",
                "city": "Some City",
                "state": "AL",
                "zipCode": "22887",
                "position": "cashier",
                "active": true
            }

        Returns JSON object
            {
                "employeeName": "First Employee",
                "message": "was added successfully"
            }

    PATCH '/customers/int:id'
        Update one customer's information
        Input data needed (JSON):
            {
                "name" : "customer name",
                "address" : "their address",
                "city": "and city",
                "state": "AL",
                "zipCode": "22887",
                "active": true
            }
        
        Returns JSON object
            {
                "message": "Customer has been updated"
            }

    DELETE '/customers/int:id'
        Delete one customer
        Returns JSON object
            {
                "message": "Customer has been deleted"
            }

    GET '/employees'
        Get a list of all employees
        Returns a JSON object
            {
                "employeeList": [
                    {
                        "active": true,
                        "address": "123 Street",
                        "city": "your city",
                        "id": 1,
                        "name": "Joe Schmo",
                        "position": "manager",
                        "state": "BE",
                        "zipCode": "23890"
                    }
                ]
            }

    POST '/employees'
        Add a new employee to the database
        Input data needed (JSON):
            {
                "name" : "employee name",
                "address" : "their address",
                "city": "and city",
                "state": "AL",
                "zipCode": "22887",
                "position": "cashier",
                "active": true
            }
        
        Returns JSON object
            {
                "message": "Employee has been updated"
            }

    PATCH '/employees/int:id'
        Update one employee's information
        Input data needed (JSON):
            {
                "name" : "employee name",
                "address" : "their address",
                "city": "and city",
                "state": "AL",
                "zipCode": "22887",
                "position": "cashier",
                "active": true
            }
        
        Returns JSON object
            {
                "message": "Employee has been updated"
            }

    DELETE '/employees/int:id'
        Delete one employee
        Returns JSON object
            {
                "message": "Employee has been deleted"
            }

Permissions
    This app has two users.  Each user has unique privileges.

        Manager
            Can perform all actions
            mgr@flower.com
            Password is 38flow##!

        Employee
            Can perform all get methods, but no others
            emp@flower.com
            Password is 38flow##@

        Customer
            cst@flower.com
            May develop later.  Password is 38flow##*