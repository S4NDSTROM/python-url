import string
import random

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from datetime import datetime

# Configure application
app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="username",
    password="password",
    hostname="",
    databasename="",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure use of SQLAlchemy
db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__ = 'url'
    id = db.Column(db.VARCHAR(5), primary_key=True)
    url = db.Column(db.TEXT, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

# Generates random string of length 4
def id_generator(size=4, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# specify domain
""" change if new domain """
domain = ""



@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response




@app.route("/", methods=["GET", "POST"])
def url():
    if request.method == "GET":
        return render_template("url.html")

    else:
        url=request.form.get("url_input")
        if len(url) < 12:
            return render_template("url.html", id = "Link already short!")
        elif len(url) > 500:
            return render_template("url.html", id = "Link way too long!")
        elif url.find(".") ==-1 or url.find(" ") !=-1:
            return render_template("url.html", id = "Link not valid!")


        else:
            url_id=id_generator()
            db_entry = Url(id=url_id,  url=url)

            db.session.add(db_entry)
            db.session.commit()

            link = domain + url_id
            return render_template("url.html", id=link)

@app.route("/<page_id>", methods=["GET"])
def page(page_id):
    url_in = page_id
    print(page_id)


    lookup = Url.query.filter_by(id=url_in).all()
    if not lookup:
        return render_template("url.html")
    else:
        s = lookup[0].url
        if s.find("http://") != 0 and s.find("https://") != 0:
            s = "http://" + s
        return redirect(s)

@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")
