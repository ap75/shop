from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    products = db.relationship('Product', backref='category', lazy=True, cascade="all, delete")

    def __repr__(self):
        return f"<Category {self.name}>"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(255))
