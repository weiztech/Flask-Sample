from os import environ

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_smorest import Api

from depot.manager import DepotManager

HOST = environ.get("FLASK_HOST") or "http://localhost"
PORT = environ.get("FLASK_PORT") or 5000

app = Flask(__name__)
app.config["HOST"] = f"{HOST}:{PORT}"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root@localhost/flask_sample"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["API_TITLE"] = "Sample API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
app.config["OPENAPI_URL_PREFIX"] = "/doc"
app.config["OPENAPI_REDOC_PATH"] = "/redoc"
app.config["OPENAPI_REDOC_URL"] = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_VERSION"] = "3.24.2"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/"
app.config["OPENAPI_RAPIDOC_PATH"] = "/rapidoc"
app.config["OPENAPI_RAPIDOC_URL"] = "https://unpkg.com/rapidoc/dist/rapidoc-min.js"

api = Api(app)


# Order matters: Initialize SQLAlchemy before Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)


DepotManager.configure('images', {
    'depot.storage_path': './media/images/'
})
