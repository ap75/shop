from extensions import db
from flask_login import UserMixin


# Модель категорії товарів
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    products = db.relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category {self.name}>"


# Модель товару
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship("Category", back_populates="products", lazy="joined")
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    picture = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"


# Модель користувача для авторизації
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Тут має бути хеш пароля

    def __repr__(self):
        return f"<User {self.username}>"
