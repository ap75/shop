from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from config import Config


# Створення Flask-додатку
app = Flask(__name__)
app.config.from_object(Config)

# Ініціалізація SQLAlchemy з додатком
db = SQLAlchemy(app)

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
