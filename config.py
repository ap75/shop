import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Шлях до бази даних (SQLite)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'shop.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = (
        False  # Вимикаємо відстеження змін для покращення продуктивності
    )

    # Секретний ключ для безпеки сесій
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "Таємний_Ключ_Захисту_Фласк_2025!"
    )

    # Налаштування для завантаження файлів
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
