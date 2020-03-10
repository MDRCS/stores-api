from src.database.ORM import db
from src.app import app

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()
