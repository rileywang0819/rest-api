import sqlite3

from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This filed cannot be blank!")
    parser.add_argument('password', type=str, required=True, help="This filed cannot be blank!")

    def post(self):
        data = UserRegister.parser.parse_args()
        
        # avoid username duplication
        username = data['username']
        result = UserModel.find_by_username(username)

        if not result:
            new_user = UserModel(**data)
            new_user.save_to_db()

            return {"message": "User created successfully."}, 201
        
        else:
            return {"message": f"This name has already existed. Please change another name."}, 400
