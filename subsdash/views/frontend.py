from flask import Blueprint, render_template, url_for

frontend = Blueprint('frontend', __name__)

SUBS = {
    "orig": {
        "prod_id": "20083526001_KG",
        "prod_name": "ROYAL GALA APPLES",
        "size": "1",
        "uom": "ea"
    },
    "pc_subs": [
        {
            "prod_id": "20039956001_KG",
            "prod_name": "MCINTOSH APPLES",
            "size": "1",
            "uom": "ea"
        },
        {
            "prod_id": "20061287001_KG",
            "prod_name": "JAZZ APPLES",
            "size": "1",
            "uom": "ea"
        }
    ]
}

@frontend.route("/")
@frontend.route("/<int:page>/")
def index(page=1):
    if page < 1:
        page = 1

    return render_template("index.html", page=page, subs=SUBS)
