import pytest
from flask import current_app, g
from flask_migrate import upgrade
from flask_sqlalchemy import SQLAlchemy

from src.app import create_app


def get_db():
    if 'db' not in g:
        db = SQLAlchemy(current_app)

        g.db = db

    return g.db


def init_db():
    db = get_db()
    db.create_all()

    upgrade(directory='./migrations')

    return db


def clear_db():
    db = get_db()
    db.session.remove()
    db.reflect()
    db.drop_all()


@pytest.fixture
def app():
    app = create_app()

    with app.app_context():
        clear_db()
        init_db()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
