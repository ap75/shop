from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, Select2Widget
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms_sqlalchemy.fields import QuerySelectField

from config import Config
from models import Category, Product, User, db


# Кастомна головна сторінка адмінки
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return super().index()


# Обмежений доступ до адмінки
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class UserAdmin(AdminModelView):
    column_list = ("username",)
    column_labels = {"username": "Логін"}
    form_overrides = {}


class CategoryAdmin(AdminModelView):
    column_labels = {"name": "Назва"}


# Обираємо категорію для товару
class ProductAdmin(AdminModelView):
    column_list = ("category", "name", "price")
    column_labels = {"category": "Категорія", "name": "Назва", "price": "Ціна"}
    form_columns = ["category", "name", "price", "picture", "description"]
    form_overrides = {"category": QuerySelectField, "picture": FileUploadField}
    form_args = {
        "category": {
            "query_factory": lambda: Category.query.all(),
            "get_label": "name",
            "allow_blank": False,
            "widget": Select2Widget(),
        },
        "picture": {
            "label": "Зображення",
            "base_path": Config.UPLOAD_FOLDER,
            "allowed_extensions": {"png", "jpg", "jpeg", "gif"},
        },
    }


# Створюємо об'єкт адмінки
admin = Admin(
    name="Адмінка магазину",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
)

admin.add_link(MenuLink(name="🏠 Перейти до магазину", url="/"))
# Додаємо моделі в адмінку
admin.add_view(CategoryAdmin(Category, db.session))
admin.add_view(ProductAdmin(Product, db.session))
admin.add_view(UserAdmin(User, db.session))
