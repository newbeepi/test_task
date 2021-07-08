from flask import render_template_string, render_template
from flask_security import auth_required

from sweater import app


@app.route("/")
@auth_required()
def home():
    return render_template_string("Hello {{ current_user.email }} {{ current_user.roles }}")


@app.route("/hello")
def hello():
    return render_template('index.html')