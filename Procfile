from app.app import create_app
app = create_app("production")

gunicorn wsgi:app --workers 16