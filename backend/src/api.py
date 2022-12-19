import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.get('/drinks')
def get_drinks():
    get = Drink.query.all()
    short = [drink.short()for drink in get]
    return jsonify({
        "success": True,
        "drinks": short

    })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.get("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_detail(jwt):
    get = Drink.query.all()
    long =[drink.long()for drink in get]
    return jsonify({
        "success":True,
        "drinks": long
    })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.post("/drinks")
@requires_auth('post:drinks')
def post_drinks(jwt):
    body = request.get_json()
    ntitle = body.get("title")
    nrecipe = body.get("recipe")

    rjson = json.dumps(nrecipe)
    add = Drink(title = ntitle, recipe = rjson)
    add.insert()
    return jsonify({
        "success":True,
        "drinks": [add.long()]

    })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.patch("/drinks/<id>")
@requires_auth('patch:drinks')
def patch_drink(jwt,id):
    body = request.get_json()
    ntitle = body.get("title")
    nrecipe = body.get("recipe")

    rjson = json.dumps(nrecipe)
    check_drink = Drink.query.filter_by(id=id).first()
    check_drink.title=ntitle
    check_drink.recipe=rjson
    check_drink.update()

    return jsonify({
        "success":True,
        "drinks":[check_drink.long()]

    })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.delete("/drinks/<id>")
@requires_auth("delete:drinks")
def delete_drink(jwt,id):
    dele = Drink.query.filter_by(id=id).first()
    dele.delete()
    return jsonify({
        "success": True, 
        "delete": id

    })


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def Auth_Error(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized error"
    }), 401

