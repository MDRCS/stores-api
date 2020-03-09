from src.database.ORM import db

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.email)

    def json(self):
        return {
            "email": self.email
        }

    @classmethod
    def getByEmail(cls,email):
        return User.query.filter_by(email=email).first()

    @classmethod
    def getAll(cls):
        return [cls(*user).json() for user in User.query.order_by(User.email).all()]

    @staticmethod
    def getById(_id):
        return (User.query.filter_by(id=_id).first()).json()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()




