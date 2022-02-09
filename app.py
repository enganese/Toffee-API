from flask import Flask, jsonify, json, request, abort
from uuid import uuid4
from sqlalchemy.orm import Session, session
import models as m
import os
import requests


BOT_TOKEN = "5117773200:AAFAmx590zp7oebV0FonobzItJ1tWLsh7l8"

app = Flask(__name__)

authorizations = ['12367890-12123423r23rijsvnsfodvndsfjbmdgbknsrgjbimrmowtbmw44389tigmewrkfpqewf', "ulan290106"]
session = Session(m.engine)


def send_message(text):
    try:
        method = "sendMessage"
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
        data = {"chat_id": 421770530, "text": text}
        resp = requests.post(url, data=data)
        print("reso.status", resp.status, "resp.json()", resp.json())
        return True
    except:
        return False
    
    
@app.errorhandler(404)
def resource_not_found(e):
    if request.headers.get('Authorization') == None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403
    return jsonify(status=404, message="Requested URL doesn't exist", data=None), 404


@app.errorhandler(405)
def server_side_error(e):
    if request.headers.get('Authorization') == None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403
    if not request.headers.get('Authorization') in authorizations:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403
    return jsonify(status=405, message="Unallowed/wrong request method!", data=None), 405


@app.errorhandler(500)
def server_side_error(e):
    if request.headers.get('Authorization') == None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403
    if not request.headers.get('Authorization') in authorizations:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403
    return jsonify(status=500, message="Something went wrong on server's side", data=None), 500


@app.route('/api/beta/receive', methods=['POST'])
def send_msg_via_bot():
    access = request.headers.get('Authorization')
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403

    if access in authorizations:
        message = request.values.to_dict().get("message")
        print("message:", message)
        send_message(text=message)
        response = jsonify(status=200, data=None), 200
        return response
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods', methods=['GET'])
def get_foods():
    access = request.headers.get('Authorization')
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!", data=None), 403

    if access in authorizations:
        foods = session.query(m.Food).all()
        all_foods = []
        for food in foods:
            all_foods.append({"id": food.id, "title": food.title, "description": food.description, "image": food.image, "price": food.price})
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
        print("request.values.to_dict()", request.values.to_dict())
        if request.get_json() == None or request.get_json() is None:
            new_food = m.Food(title=request.values.to_dict().get("title"), description=request.values.to_dict().get("description"), image=request.values.to_dict().get("image"), price=request.values.to_dict().get("price"))
            session.add(new_food)
            session.commit()
            response = {"id": new_food.id, "title": request.values.to_dict().get("title"), "description": request.values.to_dict().get("description"), "image": request.values.to_dict().get("image"), "price": request.values.to_dict().get("price")}
            return jsonify(status=201, data=response), 201
        else:
            new_food = m.Food(title=request.get_json().get("title", "Без названия"), description=request.get_json().get("description", ""), image=request.get_json().get("image", 0), price=request.get_json().get("price", 0))
            session.add(new_food)
            session.commit()
            response = {"id": new_food.id, "title": request.get_json().get("title", "Без названия"), "description": request.get_json().get("description", ""), "image": request.get_json().get("image", 0), "price": request.get_json().get("price", 0)}
            return jsonify(status=201, data=response), 201
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
        food = session.query(m.Food).filter(m.Food.id == food_id).first()
        if not food:
            return jsonify(status=404, message="no such food_id", data=None), 404
        return jsonify(status=200, data={"id": food.id, "title": food.title, "description": food.description, "image": food.image, "price": food.price}), 200
    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['PUT', "POST"])
def update_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
        print("request.get_json()", request.get_json())
        if request.get_json() == None or request.get_json() is None:
            food = session.query(m.Food).filter(m.Food.id == food_id).first()
            if not food:
                return jsonify(status=404, message="no such food_id", data=None), 404
            food.title = request.values.to_dict().get('title', food.title)
            food.description = request.values.to_dict().get('description', food.description)
            food.image = request.values.to_dict().get('image', food.image)
            food.price = request.values.to_dict().get('price', food.price)
            session.add(food)
            session.commit()
            food_again = session.query(m.Food).filter(m.Food.id == food_id).first()
            return jsonify(status=200, data={"id": food_again.id, "title": food_again.title, "description": food_again.description, "image": food_again.image, "price": food_again.price}), 200
        else:
            food = session.query(m.Food).filter(m.Food.id == food_id).first()
            if not food:
                return jsonify(status=404, message="no such food_id", data=None), 404
            food.title = request.get_json().get('title', food.title)
            food.description = request.get_json().get('description', food.description)
            food.image = request.get_json().get('image', food.image)
            food.price = request.get_json().get('price', food.price)
            session.add(food)
            session.commit()
            food_again = session.query(m.Food).filter(m.Food.id == food_id).first()
            return jsonify(status=200, data={"id": food_again.id, "title": food_again.title, "description": food_again.description, "image": food_again.image, "price": food_again.price}), 200

    else:
        return jsonify(status=403, message="Wrong authorization key!", data=None), 403


@app.route('/api/beta/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    access = request.headers.get("Authorization")
    if access == None or access is None:
        return jsonify(status=403, message="Unauthorized request!"), 403
    if access in authorizations:
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
