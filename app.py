from flask import Flask, render_template_string
from flask_security.models.fsqla import FsRoleMixin, FsUserMixin

from flask_sqlalchemy import SQLAlchemy

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_security import Security, SQLAlchemyUserDatastore, auth_required, \
    hash_password, current_user, RoleMixin, UserMixin
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test2.db'

db = SQLAlchemy(app)
fsqla.FsModels.set_db_info(db)

admin = Admin(app, name='test_task', template_mode='bootstrap3')


class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    address = db.relationship('Address', uselist=False, backref='item')


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    extend_existing=True,
)


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    full_address = db.Column(db.String(60), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # Username is important since shouldn't expose email to other users in most cases.
    username = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    # Flask-Security user identifier
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.username


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    db.create_all()

    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='end-user')

    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"), roles=['end-user'])

    if not user_datastore.find_user(email='admin@me.com'):
        user_datastore.create_user(email='admin@me.com', password=hash_password("password"), roles=['admin'])

    db.session.commit()


@app.route("/")
@auth_required()
def home():
    return render_template_string("Hello {{ current_user.email }} {{ current_user.roles }}")


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')


class UserView(ModelView):
    # Don't display the password on the list of Users
    column_exclude_list = ('password',)

    # Don't include the standard password field when creating or editing a User (but see below)
    form_excluded_columns = ('password',)

    # Automatically display human-readable names for the current and available Roles when creating or editing a User
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin') or current_user.has_role('end-user')


admin.add_view(UserView(Item, db.session))
admin.add_view(UserView(Address, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(AdminView(Role, db.session))

if __name__ == '__main__':
    app.run()
