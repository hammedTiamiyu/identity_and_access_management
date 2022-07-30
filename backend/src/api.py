import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS
import sys
import json

from .database.models import  setup_db, Drink

from .auth.auth import AuthError, get_token_auth_header, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

# db_drop_and_create_all()

# ROUTES

@app.route('/drinks')
# def headers():
#     jwt = get_token_auth_header()
#     print(jwt)
#     return "not implemented"

@requires_auth('get:drinks')
def get_drinks(token):
    try:
        
        drinks = Drink.query.all()
        formated_drinks = [drink.short() for drink in drinks]
        return jsonify({
            "success": True, 
            "drinks": formated_drinks
            }),200
    except:
        print(sys.exc_info())
        abort(403)


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(token):
    try:   
        if token:
            drinks = Drink.query.all()
            if drinks is None:
                abort(404)

            formated_drinks = [drink.long() for drink in drinks]
            return jsonify({
                "success": True, 
                "drinks": formated_drinks,
                "total": len (drinks)
                }),200
        else:
            abort()   
    except:
        print(sys.exc_info())
        abort(403)

 
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_new_drink(token):
    try:
        if token:
            body = request.get_json()
            title = body.get('title', None)           
            recipe = body.get('recipe', None)
            print(title, recipe)
            drink = Drink(title=title,recipe=json.dumps(recipe))
            drink.insert()           
            return jsonify ({
                "success": True, 
                "drinks": drink.short()
                }),200
        else:
            abort()
    except:
        print(sys.exc_info())
        abort(403)
      

@app.route("/drinks/<id>", methods=["PATCH"])
@requires_auth('patch:drinks')
def update_a_drink_details(token,id):
    try:
        if token:
            print(id)
            title = request.get_json().get("title")
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            
            if title is None:
                abort(422)
            drink.title = title
            drink.update()
            return jsonify ({
                "success": True, 
                "drinks": [drink.long() ]
                }),200
        else:
            abort()
    except:
        print(sys.exc_info())
        abort(400)


@app.route("/drinks/<id>", methods=["DELETE"])
@requires_auth('delete:drinks')
def delete_a_drink(token, id):
    try:
        if token:
            print(id)
            drink = Drink.query.get(id)
            drink.delete()
            if drink is None:
                abort(404)
            return jsonify({
                "success": True,
                "delete": id
            }),200
        else :
            abort()
    except:
        print(sys.exc_info())
        abort(422)


@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )

@app.errorhandler(422)
def unprocessable(error):
    return(
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422,
    )

@app.errorhandler(400)
def bad_request(error):
    return(
        jsonify({"success": False, "error": 400, "message": "bad request"}),
        400,
    )

@app.errorhandler(500)
def bad_request(error):
    return(
        jsonify({"success": False, "error": 500, "message": "internal server error"}),
        500,
    )


@app.errorhandler(AuthError)
def auth_error(error):
    return(
        jsonify({"success": False, "error":403, "message": "Permission not found."}),
        403,
    )