from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, limiter
from app.forms import RegisterForm
from datetime import datetime
from app.pylib import win_user
from pyad import pyad, adcontainer, aduser
import os
import time

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/r/", methods=["POST"])
def r():
    time.sleep(3.2)
    return url_for("home")

@app.route("/home/", methods=["GET", "POST"])
def home():
    return render_template("home.html", active=0, head_menu=app.config["head_menu"])

@app.route("/user_reg/")
@app.route("/user_reg/register", methods=["POST"])
def user_reg():
    form = RegisterForm()
    if form.is_submitted() and form.validate() and form.submit.data:
        user_data={
        "deptartment": form.department.data,
        "role": form.role.data,
        "fname": form.first_name.data,
        "lname": form.last_name.data,
        "email": form.email.data,
        "passw": form.password.data
        }
        user_settings = win_user.create_user_settings(user_data)
        user = win_user.create_user(user_settings, user_data["passw"], app.config["adquery"])
        msg = user_data["fname"] + ", your user account: " + user_settings["sAMAccountName"] + " should be created. If not please contact the system administrator."
        return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Succes", msg=msg)
    else:
        return render_template("user_reg.html", active=1, head_menu=app.config["head_menu"], form=form)
