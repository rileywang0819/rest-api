import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import ItemList, Item
from resources.store import Store, StoreList
from db import db


# ==================
#   Initialization
# ==================

app = Flask(__name__)

# the SQLAlchemy db lives at Heroku Postgres or the root folder of our project "/data.db"
heroku_db_uri = os.getenv("DATABASE_URL")
if heroku_db_uri and heroku_db_uri.startswith("postgres://"):
    heroku_db_uri = heroku_db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = heroku_db_uri if heroku_db_uri else 'sqlite:///data.db'
# turn off the flask_sqlalchemy extension's modification tracker (but not turn off the sqlalchemy's tracker)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'jose'     # should be secure in production case

api = Api(app)

jwt = JWT(app, authenticate, identity)


# ========================
#   Add Resource to API
# ========================

api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/stores/<string:name>')
api.add_resource(UserRegister, '/register')


if __name__ == '__main__':
    # link app with sqlalchemy integration
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(debug=True)
