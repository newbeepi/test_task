from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_security.models import fsqla
from flask_babelex import Babel


app = Flask(__name__)
Babel(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Secret key just for testing"
app.config['SECURITY_PASSWORD_SALT'] = "123948130912838129031290"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test6.db'

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)

admin = Admin(app, name='test_task', template_mode='bootstrap3')

