from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


# Define models

# Users
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))

# Subs
class Mapping(db.Model):
	__tablename__ = 'mapping'
	id = db.Column(db.Integer, primary_key=True)
	orig_id = db.Column(db.Integer(), db.ForeignKey('product.id'))
	pc_id = db.Column(db.Integer(), db.ForeignKey('product.id'))

	def __init__(self, orig_id, pc_id):
		self.orig_id = orig_id
		self.pc_id = pc_id


class Product(db.Model):
	__tablename__ = 'product'
	id = db.Column(db.Integer, primary_key=True)
	prod_id = db.Column(db.String(80), unique=True)
	prod_name = db.Column(db.String(255))
	prod_size = db.Column(db.Integer(), nullable=True)
	prod_uom = db.Column(db.String(40), nullable=True)
	prod_brand = db.Column(db.String(120), nullable=True)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    answer = db.Column(db.String(4), nullable=True)
    user_email = db.Column(db.String(255), db.ForeignKey('user.email')) 

    def __init__(self, pid, answer, user_email):
        self.pid = pid
        self.answer = answer
        self.user_email = user_email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Sample Data
SUBS = {
    "orig": {
        "prod_id": "20083526001_KG",
        "prod_name": "ROYAL GALA APPLES",
        "size": "1",
        "uom": "ea",
        "brand": "no brand"
    },
    "pc_subs": [
        {
            "prod_id": "20039956001_KG",
            "prod_name": "MCINTOSH APPLES",
            "size": "1",
            "uom": "ea",
            "pid": 2,
            "brand": "no name"
        },
        {
            "prod_id": "20061287001_KG",
            "prod_name": "JAZZ APPLES",
            "size": "1",
            "uom": "ea",
            "pid": 3,
            "brand": "no name"
        }
    ]
}


# Routers
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/feedback/<int:page>")
@login_required
def feedback(page=1):
    if page < 1:
        page = 1

    return render_template("feedback.html", page=page, subs=SUBS)


@app.route("/post_answer/<int:page>/<uid>", methods=['POST'])
def post_answer(page, uid):
    answer_map = request.form.copy()
    for pid, ans in answer_map.iteritems():
        answer = Answer(pid, ans, uid)
        db.session.add(answer)
        db.session.commit()
    page_next = page+1
    return redirect(url_for('feedback', page=page_next))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
