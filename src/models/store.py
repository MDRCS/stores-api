import json
from src.database.ORM import db


class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('Item', lazy='dynamic')  # this is a list of items -> one to many  # lazy = dynamic mean the object items won't get created right now

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @staticmethod
    def getByName(name):
        return Store.query.filter_by(name=name).first().json()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
