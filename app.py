from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, UserMixin, login_required, current_user


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)


# Define models

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Active(db.Model):
    user_email = db.Column(db.String(255), db.ForeignKey(
        'user.email'), primary_key=True)
    active_page = db.Column(db.Integer())

    def __init__(self, email, page):
        self.user_email = email
        self.active_page = page


class Mapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page = db.Column(db.Integer)
    orig_id = db.Column(db.String(80), db.ForeignKey('product.id'))
    pc_id = db.Column(db.String(80), db.ForeignKey('product.id'))

    def __init__(self, page, orig_id, pc_id):
        self.page = page
        self.orig_id = orig_id
        self.pc_id = pc_id


class Product(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    name = db.Column(db.String(255))
    size = db.Column(db.Float(), nullable=True)
    uom = db.Column(db.String(40), nullable=True)
    brand = db.Column(db.String(120), nullable=True)

    def __init__(self, id, name, size, uom, brand):
        self.id = id
        self.name = name
        self.size = size
        self.uom = uom
        self.brand = brand


class Answer(db.Model):
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


# Routers
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/last_visit")
@login_required
def last_visit():
    last_pages = Active.query.filter_by(user_email=current_user.email)
    last_page = last_pages[-1].active_page
    return redirect(url_for('feedback', page=last_page))


@app.route("/feedback/<int:page>")
@login_required
def feedback(page=1):
    if page < 1:
        page = 1

    subs = Mapping.query.filter_by(page=page).all()
    if not subs:
        return redirect(url_for('index'))

    data = {"orig": {}, "pc_subs": []}

    orig_attr = Product.query.filter_by(id=subs[0].orig_id).all()[0]
    data["orig"] = {
        "prod_id": orig_attr.id,
        "prod_name": orig_attr.name,
        "size": orig_attr.size,
        "uom": orig_attr.uom,
        "brand": orig_attr.brand
    }

    pid_dict = {}
    prod_ids = []
    for sub in subs:
        prod_ids.append(sub.pc_id)
        pid_dict[sub.pc_id] = sub.id
    prod_attrs = Product.query.filter(Product.id.in_(prod_ids)).all()

    for prod_attr in prod_attrs:
        attr = {
            "prod_id": prod_attr.id,
            "prod_name": prod_attr.name,
            "size": prod_attr.size,
            "uom": prod_attr.uom,
            "brand": prod_attr.brand,
            "pid": pid_dict[prod_attr.id]
        }
        data["pc_subs"].append(attr)

    return render_template("feedback.html", page=page, subs=data)


@app.route("/post_answer/<int:page>/<email>", methods=['POST'])
def post_answer(page, email):
    answer_map = request.form.copy()
    for pid, ans in answer_map.iteritems():
        answer = Answer(pid, ans, email)
        db.session.add(answer)
        db.session.commit()
    next_page = page + 1
    user_active = Active(email, next_page)
    db.session.add(user_active)
    db.session.commit()
    return redirect(url_for('feedback', page=next_page))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)
