from flask_restful import Resource, request
from flask_login import login_user

from clientapi.models import User


class LoginApi(Resource):
    def get(self):
        message = "Hello World!"
        # check whether employee exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email="asd@asd.com").first()
        if user is not None and user.verify_password("password"):
            # log employee in
            login_user(user)

        # when login details are incorrect
        else:
            message = "Invalid email or password."

        return {"message": message}

    def post(self):
        message = "Hello World!"

        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

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
