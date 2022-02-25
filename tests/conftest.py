import pytest
from click.testing import CliRunner

from app.settings import db
from app.main import create_app, init_db_command


flask_app = create_app()
flask_app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/flask_test"


@pytest.fixture
def app():
    db.drop_all()
    runner = CliRunner()
    runner.invoke(init_db_command)
    yield flask_app
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
