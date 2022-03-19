from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))     # size limitation
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # this proporty won't be related to database, it's just in the created object
        self.greeting_msg = 'hi'

    @classmethod
    def find_by_username(cls, username):
        # cls.query : query builder
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()