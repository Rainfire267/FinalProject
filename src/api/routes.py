"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Owner, Buddy
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


api = Blueprint('api', __name__)

# @api.route('/token', methods=['POST'])
# def handle_token():
#    return jsonify(response_body), 200

@api.route('/register', methods=['POST'])
def register():
    password = request.json.get('password', None)
    email = request.json.get('email', None)
    name = request.json.get('name', None)
    user_role = request.json.get('rol', None)
    ## tipo de usuario
    last_name = request.json.get('last_name', None)
    
    if password is None:
        return 'You need to specify the password', 400
    if email is None:
        return 'You need to specify the email', 400
    if name is None:
        return 'You need to specify the name', 400
    if last_name is None:
        return 'You need to specify the last_name', 400
    if user_role is None:
        return 'You need to specify the user_rol', 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({"msg" : "User already exist"})
    else: 
        new_user = User(email=email, password=password, name=name, last_name=last_name, user_role=user_role, is_active=True)
        db.session.add(new_user)
        db.session.commit()
        if user_role == 'owner':
            new_owner = Owner(user_id=new_user.id)    
            db.session.add(new_owner)
            db.session.commit()
        else:
            new_buddy = Buddy(user_id=new_user.id)    
            db.session.add(new_buddy)
            db.session.commit()
        
        return jsonify({"msg" : "User added successfully!"}), 200

@api.route('/login', methods=['POST'])
def signin():
    password = request.json.get('password', None)
    email = request.json.get('email', None)

    if password is None:
        return 'You need to specify the password', 400
    if email is None:
        return 'You need to specify the email', 400

    user = User.query.filter_by(email=email).one_or_none()
    
    if not user or not user.check_password(password):
        # user not found on the db o password error
        return jsonify({"msg": "Invalidate email or password"})
    else:
        # create a new token with user_id
        access_token = create_access_token(identity=user, expires_delta=timedelta(hours=80))
        return jsonify({"token" : access_token, "user_id" : user.id}), 200
