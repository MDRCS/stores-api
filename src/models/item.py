from src.database.ORM import db


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('Store')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            "name": self.name,
            "price": self.price
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def getItemByName(cls, name):
        return Item.query.filter_by(name=name).first()  # LIMIT 1

    @staticmethod
    def getAll():
        return [item.json() for item in Item.query.order_by(Item.name).all()]
