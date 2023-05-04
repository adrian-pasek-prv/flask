import requests
import os
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required, get_jwt
from blocklist import BLOCKLIST

from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema

# Import a task of sending an email message to user
from tasks import send_user_registration_email

blp = Blueprint('users', __name__, description='Operations on users')

@blp.route('/register')
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            # Check if either username or email already exists in the database
            or_(
                UserModel.username == user_data['username'],
                UserModel.email == user_data['email']
                )
        ).first():
            abort(409, message='A user with that username or email already exists.')
            
        user = UserModel(
            username = user_data['username'],
            email = user_data['email'],
            # scramble password into a hash which then
            # can be compared in another attempt to the same hashed password
            password = pbkdf2_sha256.hash(user_data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Attach a task to queue with email and username argument that will be passed down to
        # send_user_registration_email
        current_app.queue.enqueue(send_user_registration_email, user.email, user.username)
        
        return {"message": "User created successfully."}, 201
    
@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Check if user exists
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()
        
        # Check if you can match hashed version of provided password to hashed version stored in DB
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            # Access token will be used for critical endpoints, while
            # refresh token to not so important endpoints
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_token, 'refresh_token': refresh_token}
        
        abort(401, message='Invalid credentials.')

@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        # fresh=Flase is important because otherwise we will overwrite fresh token that is used for critical operations
        # that require user to reauthenticate
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}
        
@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        # After user logs out, add his current jti to blocklist
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Successfully logged out.'}
            

@jwt_required()           
@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
