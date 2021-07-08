from sweater import app, db, admin
from sweater.adminviews import UserView, AdminView
from sweater.models import User, Role, Item, Node# , Edge
import sweater.routes

from flask_security import Security, SQLAlchemyUserDatastore, hash_password


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


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

admin.add_view(UserView(Item, db.session))
admin.add_view(UserView(Node, db.session))
#admin.add_view(UserView(Edge, db.session))
admin.add_view(UserView(User, db.session))
admin.add_view(AdminView(Role, db.session))

if __name__ == '__main__':
    app.run()
