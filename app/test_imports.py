# test_imports.py
try:
    from app.models import Base
    from app.db import engine
    from app.routers import task, user
    print("Импорты работают правильно!")
except ImportError as e:
    print(f"Ошибка импорта: {e}")
