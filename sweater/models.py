from . import db

from flask_security import UserMixin, RoleMixin


class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    address = db.relationship('Node', uselist=False, backref=db.backref('item'))

    def __repr__(self):
        return self.name


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
    extend_existing=True,
)


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


class Node(db.Model):
    __tablename__ = "Node"
    node_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(80))
    number = db.Column(db.String(20))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), default=None)
    father_id = db.Column(db.Integer, db.ForeignKey('Node.node_id'))
    father_node = db.relationship('Node', remote_side=[node_id], uselist=False)

    def to_highest_node(self):
        x = self
        res = []
        while father := x.father_node:
            x = father
            res += [x]
        return res

    def __repr__(self):
        res = self.to_highest_node()[::-1] + [self]
        return ' '.join(x.type + ' ' + x.number for x in res)


#
# class Edge(db.Model):
#
#     lower_id = db.Column(db.Integer, db.ForeignKey('Node.node_id'), primary_key=True)
#     higher_id = db.Column(db.Integer, db.ForeignKey('Node.node_id'), primary_key=True)
#
#     lower_adress = db.relationship(
#         'Node', backref=db.backref('lower_edges'), primaryjoin=lower_id == Node.node_id
#     )
#
#     higher_adress = db.relationship(
#         'Node', backref=db.backref('higher_edges'), primaryjoin=higher_id == Node.node_id
#     )
#
#     def __init__(self, lower_node, higher_node):
#         self.lower_adress = lower_node
#         self.higher_adress = higher_node
