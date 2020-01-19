from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, limiter
from app.forms import RegisterForm
from datetime import datetime
from pylib import win_user
import os

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/home/")
def home():
    return render_template("home.html", active=0, head_menu=app.config["head_menu"])

@app.route("/user_reg/")
@app.route("/user_reg/register")
def user_reg():
    form = RegisterForm()
    if form.is_submitted() and form.validate() and form.submit.data:
        user_data={
        "deptartment": form.department.data
        "role": form.role.data
        "fname": form.first_name.data
        "lname": form.last_name.data
        "email": form.email.data
        "passw": form.password.data
        }
        user_data = win_user.create_user_settings(user_data)