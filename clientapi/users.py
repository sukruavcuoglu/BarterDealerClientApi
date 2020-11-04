"""
This is the people module and supports all the REST actions for the
people data
"""

import datetime

import jwt
from flask import make_response, abort, request
from werkzeug.security import generate_password_hash

from clientapi.models.users import User, UserSchema
from application import db


def login(user):
    email = user.get("email")
    password = user.get("password")

    # check whether user exists in the database and whether
    # the password entered matches the password in the database
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        # log user in
        data = read_one(user_id=user.user_id)
        auth_token = encode_auth_token(user_id=user.user_id)
        data["auth_token"] = auth_token.decode()

        return data

    # when login details are incorrect
    else:
        abort(404, 'Invalid email or password.')


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of Users

    :return:        json string of list of people
    """

    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''

    if auth_token:
        resp = decode_auth_token(auth_token)
        if isinstance(resp, str):
            # Create the list of people from our data
            users = User.query.order_by(User.username).all()

            # Serialize the data for the response
            user_schema = UserSchema(many=True)
            data = user_schema.dump(users)
            return data
        else:
            abort(401, "Please provide a valid token")
    else:
        abort(401, "Please provide a valid token")


def read_one(user_id):
    """
    This function responds to a request for /api/users/{user_id}
    with one matching user from Users

    :param user_id:   Id of user to find
    :return:            user matching id
    """
    # TODO: check auth token, null kontrolleri

    # Build the initial query
    user = (
        User.query.filter(User.user_id == user_id)
            .one_or_none()
    )

    # Did we find a user?
    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"user not found for Id: {user_id}")


def create(user):
    """
    This function creates a new user in the Users structure
    based on the passed in user data

    :param user:  user to create in Users structure
    :return:        201 on success, 406 on user exists
    """
    email = user.get("email")
    username = user.get("username")
    password = user.get("password")
    user.pop('password', None)
    existing_user = (
        User.query.filter(User.email == email)
            .filter(User.username == username)
            .one_or_none()
    )

    # Can we insert this user?
    if existing_user is None:

        # Create a user instance using the schema and the passed in user
        schema = UserSchema()
        new_user = schema.load(user,
                               session=db.session)
        # Add the user to the database
        new_user.password = password
        db.session.add(new_user)
        db.session.commit()
        auth_token = encode_auth_token(new_user.user_id)
        # Serialize and return the newly created user in the response
        data = schema.dump(new_user)
        # generate the auth token
        data["auth_token"] = encode_auth_token(new_user.user_id).decode()

        return data, 201

    # Otherwise, nope, user exists already
    else:
        abort(409, f"user {email} {username} zaten var")


def update(user_id, user):
    """
    This function updates an existing user in the Users structure

    :param user_id:   Id of the user to update in the Users structure
    :param user:      user to update
    :return:            updated user structure
    """
    # Get the user requested from the db into session
    update_user = User.query.filter(
        User.user_id == user_id
    ).one_or_none()

    # Did we find an existing user?
    if update_user is not None:

        # turn the passed in user into a db object
        schema = UserSchema()
        user["user_id"] = user_id
        updated_user = schema.load(user, session=db.session)
        # Set the id to the user we want to update
        updated_user.user_id = update_user.user_id
        # merge the new object into the old and commit it to the db
        db.session.merge(updated_user)
        db.session.commit()

        # return updated user in the response
        data = schema.dump(updated_user)

        return data, 200

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"user not found for Id: {user_id}")


def delete(user_id):
    """
    This function deletes a user from the Users structure

    :param user_id:   Id of the user to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the user requested
    user = User.query.filter(User.user_id == user_id).one_or_none()

    # Did we find a user?
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return make_response(f"user {user_id} deleted", 200)

    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"user not found for Id: {user_id}")


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        from run import app
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        from run import app
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'
