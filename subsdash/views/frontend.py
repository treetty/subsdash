from flask import Blueprint, render_template, url_for, request

from subsdash.models import Answer
from subsdash.extensions import db


frontend = Blueprint('frontend', __name__)

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


@frontend.route("/")
@frontend.route("/<int:page>/")
def index(page=1):
    if page < 1:
        page = 1

    return render_template("index.html", page=page, subs=SUBS)


@frontend.route("/post_answer", methods=['POST'])
def post_answer():
    pid = 0
    answer_map = request.form.copy()
    for pid, ans in answer_map.iteritems():
        answer = Answer(pid, ans)
        db.session.add(answer)
        db.session.commit()
    return redirect(url_for(index)) # go to next page
