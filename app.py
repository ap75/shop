from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config
from extensions import db, login_manager


# Створення Flask-додатку
app = Flask(__name__)
app.config.from_object(Config)

# Ініціалізація розширень
db.init_app(app)
login_manager.init_app(app)

# Імпортуємо моделі після ініціалізації db
from models import Category, Product

# Створення таблиць, якщо їх ще немає
with app.app_context():
    db.create_all()  # Створення таблиць

with app.app_context():
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    print("Таблиці в базі даних:", inspector.get_table_names())  # Перевіряємо таблиці

# Ініціалізація Flask-Admin
admin = Admin(app, name="Адмінка магазину", template_mode="bootstrap4")

# Додаємо моделі до адмін-панелі
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))

if __name__ == "__main__":
    app.run(debug=True)
