from flask import Flask, redirect, url_for, request, render_template, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from flask_admin.menu import MenuLink
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms_sqlalchemy.fields import QuerySelectField

from admin import admin
from config import Config
from extensions import db, login_manager
from forms import RegistrationForm, LoginForm
from models import Category, Product, User


# Створення Flask-додатку
app = Flask(__name__)
app.config.from_object(Config)

# Ініціалізація розширень
db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)

# Функція завантаження користувача
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    """Головна сторінка: список товарів."""
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash('Регистрация прошла успешно!', 'success')
        login_user(user)
        return redirect(url_for('admin.index'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Успішний вхід!', 'success')
            return redirect(url_for('admin.index'))

        flash('Невірний логін або пароль', 'danger')

    return render_template('login.html', form=form)

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
