from flask import Flask, redirect, url_for, request, render_template, flash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import login_user, logout_user, current_user

from config import Config
from extensions import db, login_manager
from models import Category, Product, User


# Створення Flask-додатку
app = Flask(__name__)
app.config.from_object(Config)

# Ініціалізація розширень
db.init_app(app)
login_manager.init_app(app)

# Функція завантаження користувача
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Захист адмін-панелі
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))

# Додаємо Flask-Admin
admin = Admin(app, name="Адмінка магазину", template_mode="bootstrap4")
admin.add_view(AdminModelView(Category, db.session))
admin.add_view(AdminModelView(Product, db.session))
admin.add_view(AdminModelView(User, db.session))

# Сторінка входу
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Тут треба додати хешування
            login_user(user)
            return redirect(url_for("admin.index"))

        flash("Неправильний логін або пароль")

    return render_template("login.html")


# Сторінка виходу
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


# Створення таблиць, якщо їх ще немає
with app.app_context():
    db.create_all()  # Створення таблиць


if __name__ == "__main__":
    app.run(debug=True)
