import os
from flask import Flask, request, jsonify, abort, redirect, render_template, session, url_for, make_response
from sqlalchemy import exc
from flask_cors import CORS
from models import setup_db, Customer, Employee#, Order, Item, OrderItem, db_drop_and_create_all
from flask_sqlalchemy import SQLAlchemy
import json
from auth import AuthError, requires_auth
import http.client

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #CORS headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/')
    def login():
        return redirect('https://dev-jie5-13n.auth0.com/authorize?audience=https://udacity-flower-shop.herokuapp.com&response_type=token&client_id=qdF7zuk9fTZrHHlSR2jZR4nfZbn9Zm2U&redirect_uri=https://udacity-flower-shop.herokuapp.com/login-results')

    @app.route('/login-results', methods=['GET', 'POST'])
    def login_results(jwt):
        return jsonify({
            'message': 'You are logged in.  Use the token in the address bar to hit various endpoints in Postman.'
        })

    #Customer operations
    
    @app.route('/customers', methods=['GET'])
    @requires_auth("view:customers")
    def get_customer_list(jwt):
        customer_list = Customer.query.all()
        if not customer_list:
            abort(404)
        returnList = []
        for customer in customer_list:
            record = customer.format()
            returnList.append(record)
        return jsonify({
            'customerList': returnList
        })

    @app.route('/customers/<customer_id>', methods=['GET'])
    @requires_auth("view:customer")
    def get_customer(jwt, customer_id):
        customer = Customer.query.filter_by(id=customer_id).first()
        if not customer:
            abort(404)
        return jsonify({
            'customer': customer.format()
        })
    
    @app.route('/customers', methods=['POST'])
    @requires_auth("add:customer")
    def create_customer(jwt):
        customerData = request.get_json()
        if customerData == None:
            abort(404)
        myName = customerData.get('name')
        myAddress = customerData.get('address')
        myCity = customerData.get('city')
        myState = customerData.get('state')
        myZip = customerData.get('zipCode')

        if  myName and myAddress and myCity and myState and myZip:
            newCustomer = Customer(name=myName, address=myAddress, city=myCity, state=myState, zipCode=myZip, active=True)
            newCustomer.insert()
            return jsonify({
                'customerName': myName,
                'message': 'was added successfully'
            })
        return jsonify({
            'message': 'Please fill out all required fields and resubmit'
        }), 422
    
    @app.route('/customers/<customer_id>', methods=['PATCH'])
    @requires_auth("patch:customer")
    def update_customer(jwt, customer_id):
        customerUpdates = request.get_json()
        if not customerUpdates:
            return jsonify({
                'message': 'No updated information included in your request.  Changes canceled.'
            })

        customer = Customer.query.filter_by(id=customer_id).first()
        if not customer:
            abort(401)

        try:
            customer.name = customerUpdates.get('name') if customerUpdates.get('name') != '' else customer.name
            customer.address = customerUpdates.get('address') if customerUpdates.get('address') != '' else customer.address
            customer.city = customerUpdates.get('city') if customerUpdates.get('city') != '' else customer.city
            customer.state = customerUpdates.get('state') if customerUpdates.get('state') != '' else customer.state
            customer.zipCode = customerUpdates.get('zipCode') if customerUpdates.get('zipCode') != '' else customer.zipCode
            customer.active = customerUpdates.get('active') if customerUpdates.get('active') != True or customerUpdates.get('active') != False else customer.active
            customer.update()
        except:
            return jsonify({
                'message': 'All fields must be included in original request.  Please try again.'
            })
        return jsonify({
            'message': 'Customer has been updated'
        })
    
    @app.route('/customers/<customer_id>', methods=['DELETE'])
    @requires_auth("delete:customer")
    def delete_customer(jwt, customer_id):
        customer = Customer.query.filter_by(id=customer_id).first()
        if not customer:
            abort(401)
        customer.delete()
        return jsonify({
            'message': 'Customer has been deleted'
        })
    
    # Employee operations

    @app.route('/employees', methods=['GET'])
    @requires_auth("view:employees")
    def get_employee_list(jwt):
        employee_list = Employee.query.all()
        if not employee_list:
            return jsonify({
                'message': 'No employees in database'
            }, 404)
        returnList = []
        for employee in employee_list:
            record = employee.format()
            returnList.append(record)
        return jsonify({
            'employeeList': returnList
        })

    @app.route('/employees', methods=['POST'])
    @requires_auth("add:employee")
    def create_employee(jwt):
        employeeData = request.get_json()
        if employeeData == None:
            return jsonify({
                'message': 'Missing or invalid employee information'
            }, 404)
        
        myName = employeeData.get('name')
        myAddress = employeeData.get('address')
        myCity = employeeData.get('city')
        myState = employeeData.get('state')
        myZip = employeeData.get('zipCode')
        myPosition = employeeData.get('position')

        if  myName and myAddress and myCity and myState and myZip and myPosition:
            newEmployee = Employee(name=myName, address=myAddress, city=myCity, state=myState, zipCode=myZip, position=myPosition, active=True)
            newEmployee.insert()
            return jsonify({
                'employeeName': myName,
                'message': 'was added successfully'
            })
        return jsonify({
                'message': 'Please fill out all required fields and resubmit'
            }), 422

    @app.route('/employees/<employee_id>', methods=['PATCH'])
    @requires_auth("patch:employee")
    def update_employee(jwt, employee_id):
        employeeUpdates = request.get_json()
        if not employeeUpdates:
            return jsonify({
                'message': 'No updated information included in your request.  Changes canceled.'
            })

        employee = Employee.query.filter_by(id=employee_id).first()
        if not employee:
            return jsonify({
                'message': 'No employee found'
            }, 404)

        try:
            employee.name = employeeUpdates.get('name') if employeeUpdates.get('name') != '' else employee.name
            employee.address = employeeUpdates.get('address') if employeeUpdates.get('address') != '' else employee.address
            employee.city = employeeUpdates.get('city') if employeeUpdates.get('city') != '' else employee.city
            employee.state = employeeUpdates.get('state') if employeeUpdates.get('state') != '' else employee.state
            employee.zipCode = employeeUpdates.get('zipCode') if employeeUpdates.get('zipCode') != '' else employee.zipCode
            employee.position = employeeUpdates.get('position') if employeeUpdates.get('position') != '' else employee.position
            employee.active = employeeUpdates.get('active') if employeeUpdates.get('active') != True or employeeUpdates.get('active') != False else employee.active
            employee.update()
        except:
            return jsonify({
                'message': 'All fields must be included in original request.  Please try again.'
            })
        return jsonify({
            'message': 'Employee has been updated'
        })

    @app.route('/employees/<employee_id>', methods=['DELETE'])
    @requires_auth("delete:employee")
    def delete_employee(jwt, employee_id):
        employee = Employee.query.filter_by(id=employee_id).first()
        if not employee:
            return jsonify({
                'message': 'No employee found'
            })
        employee.delete()
        return jsonify({
            'message': 'Employee has been deleted'
        })
    
    #Order operations

    # @app.route('/orders/<order_id>', methods=['GET'])
    # @requires_auth("view:order")
    # def get_order(jwt, order_id):
    #     order = Order.query.filter_by(id=order_id).first()
    #     if not order:
    #         return jsonify({
    #             'message': 'No order found'
    #         }, 404)

    #     return jsonify({
    #         'order': order.format()
    #     })

    # @app.route('/addToOrder/<order_id>', methods=['POST'])
    # @requires_auth("add:order")
    # def add_to_order(jwt):
    #     orderItem = request.get_json()
    #     if orderItem == None:
    #         return jsonify({
    #             'message': 'Missing or invalid item information'
    #         }, 404)
        
    #     myQuantity = orderItem.get('quantity')
    #     myItemId = orderItem.get('item_id')
    #     myOrderId = orderItem.get('order_id')

    #     if myQuantity and myItemId and myOrderId:
    #         newOrderItem = OrderItem(quantity=myQuantity, item.id=myItemId, order_id=myOrderId)
    #         newOrderItem.insert()
    #         return jsonify({
    #             'message': 'Item was added successfully'
    #         })
    #     return jsonify({
    #             'message': 'Please fill out all required fields and resubmit'
    #         }), 422

    # @app.route('/orders/<order_id>', methods=['DELETE'])
    # @requires_auth("delete:order")
    # def delete_order(jwt, order_id):
    #     order = Order.query.filter_by(id=order_id).first()
    #     if not order:
    #         return jsonify({
    #             'message': 'No order found'
    #         })
    #     order.delete()
    #     return jsonify({
    #         'message': 'Order has been deleted'
    #     })
    
    #Error handlers

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 401

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code
    

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)