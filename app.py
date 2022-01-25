from flask import Flask, jsonify, json, request, abort
from uuid import uuid4
from sqlalchemy.orm import Session, session
import models as m


app = Flask(__name__)

authorizations = ['12367890-12123423r23rijsvnsfodvndsfjbmdgbknsrgjbimrmowtbmw44389tigmewrkfpqewf', "ulan290106"]


@app.errorhandler(404)
def resource_not_found(e):
    if request.headers.get('Authorization') == None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403
    return jsonify(status=404, message="Requested URL doesn't exist", data=None), 404


@app.errorhandler(500)
def server_side_error(e):
    if request.headers.get('Authorization') == None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403
    if not request.headers.get('Authorization') in authorizations:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403
    return jsonify(status=500, message="Something went wrong on server's side", data=None), 500


@app.route('/api/beta/foods', methods=['GET'])
def get_foods():
    access = request.headers.get('Authorization')
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403

    if access in authorizations:
        session = Session(m.engine)
        foods = session.query(m.Food).all()
        all_foods = []
        for food in foods:
            all_foods.append({"id": food.id, "title": food.title, "description": food.description, "amount": food.amount, "price": food.price})
        response = jsonify(status=200, data=all_foods), 200
        return response
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


# @app.route('/api/secret/api_tokens/get/<string:secret>', methods=['GET'])
# def get_api(secret):
#     try:
#         print(secret)
#         if secret == "ulanIsTheBestDeveloper":
#             uid = uuid4()
#             authorizations.append(f"{uid}")
#             response = jsonify(status=201, data={"api_token": f"{uid}", "message": "We're glad to see you using our service!"}), 201
#             return response
#         else:
#             return jsonify(status=403, message="Unauthorized request!", data=None), 403 
#     except Exception as e:
#         print(e)


@app.route('/api/beta/foods', methods=['POST'])
def add_food():
    access = request.headers.get('Authorization')
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403

    if access in authorizations:
        if request.json == None or request.json is None:
            session = Session(m.engine)
            new_food = m.Food(title=request.values.get("title"), description=request.values.get("description"), amount=request.values.get("amount"), price=request.values.get("price"))
            session.add(new_food)
            session.commit()
            response = {"title": request.values.get("title"), "description": request.values.get("description"), "amount": request.values.get("amount"), "price": request.values.get("price")}
            return jsonify(status=201, data=response), 201
        else:
            session = Session(m.engine)
            new_food = m.Food(title=request.json.get("title", "Без названия"), description=request.json.get("description", ""), amount=request.json.get("amount", 0), price=request.json.get("price", 0))
            session.add(new_food)
            session.commit()
            response = {"title": request.json.get("title", "Без названия"), "description": request.json.get("description", ""), "amount": request.json.get("amount", 0), "price": request.json.get("price", 0)}
            return jsonify(status=201, data=response), 201
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
        session = Session(m.engine)
        food = session.query(m.Food).filter(m.Food.id == food_id).first()
        if not food:
            return jsonify(status=404, message="no such food_id", data=None), 404
        return jsonify(status=200, data={"id": food.id, "title": food.title, "description": food.description, "amount": food.amount, "price": food.price}), 200
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
        session = Session(m.engine)
        food = session.query(m.Food).filter(m.Food.id == food_id).first()
        if not food:
            return jsonify(status=404, message="no such food_id", data=None), 404
        food.title = request.json.get('title', food.title)
        food.description = request.json.get('description', food.description)
        food.amount = request.json.get('amount', food.amount)
        food.price = request.json.get('price', food.price)
        session.add(food)
        session.commit()
        return jsonify(status=200, data={"id": food.id, "title": food.title, "description": food.description, "amount": food.amount, "price": food.price}), 200
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
        session = Session(m.engine)
        food = session.query(m.Food).filter(m.Food.id == food_id).first()
        if not food:
            return jsonify(status=404, message="no such food_id", data=None), 404
        try:
            session.delete(food)
            session.commit()
            return jsonify(status=200, data={"deleted": True})
        except Exception as e:
            return jsonify(status=500, data={"deleted": False})
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


# @app.route('/api/beta/users', methods=['POST'])
# def add_user():
#     try:
#         req = request.json
#         print('\n\n\n\n\n\n\n\nYoooooooooo', req)
#         un = req['username']
#         fn = req['first_name']
#         ln = req['last_name']
#         tp = req['type']
#         datas = {"username": un, "first_name": fn, "last_name": ln, "type": tp}
#         for key in datas.keys():
#             if datas[key] == None:
#                 return jsonify(error={"code": 403, "message": f"{datas[key]} is required data in request!"}), 403
#     except KeyError as e:
#         print(e)


if __name__ == '__main__':
    app.run(debug=True)
