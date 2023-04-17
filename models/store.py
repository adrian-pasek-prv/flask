from db import db

# Define a schema of stores table
class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    # Specify columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Create a relationship to stores but set it to lazy=dynamic so that it will
    # show items when we tell it to
    items = db.relationship('ItemModel', back_populates='store', lazy='dynamic', cascade='all, delete') # cascade means delete all items if we delete store