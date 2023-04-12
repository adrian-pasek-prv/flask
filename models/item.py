from db import db

# Define a schema of items table
class ItemModel(db.Model):
    __tablename__ = 'items'
    
    # Specify columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), unique=False, nullable=False) # ForeignKey allows to map store_id to stores table
    # Create a relationship to stores table so that it will populate stores data here
    store = db.relationship('StoreModel', back_populates='items')