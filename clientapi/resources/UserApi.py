from flask_restful import Resource
from flask_login import login_user
from flask import jsonify

from clientapi.models import User


class UserApi(Resource):
    def get(self, user_id):

        user = User.query.filter_by(user_id=user_id).first().as_dict()
        if user is not None:
            return jsonify(user=user)
        else:
            message = "Invalid user id."

        return {"message": message}

    def post(self):
        message = "Hello World!"
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by("email").first()
        if user is not None and user.verify_password("pass"):
            # log employee in
            login_user(user)

        # when login details are incorrect
        else:
            message = "Invalid email or password."

        return {"message": message}
