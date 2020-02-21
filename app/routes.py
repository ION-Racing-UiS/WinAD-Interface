from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, limiter
from app.forms import RegisterForm
from datetime import datetime
from app.pylib import win_user
from pyad import pyad, adcontainer, aduser, adgroup, adobject
import os
import time
import pythoncom
import pywin32_system32

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
        pythoncom.CoInitialize()
        user_data={
        "department": form.department.data,
        "role": form.role.data,
        "fname": form.first_name.data,
        "lname": form.last_name.data,
        "email": form.email.data,
        "passw": form.password.data
        }
        user_settings = win_user.create_user_settings(user_data)
        #os.system("python \"" + win_user.path + "\" \"" + user_data["fname"] + " " + user_data["lname"] + "\" \"" + user_data['passw'] + "\" \"" + user_data['department'] + "\" \"" + user_data['role'] + "\" \"" + user_data['email'] + "\"")
        #os.system("python \"" + win_user.path + "\" \"" + user_data["fname"] + " " + user_data["lname"] + "\" \"" + user_data["department"] + "\"")
        #win_user.create_user(user_settings, user_data["passw"])
        try:
            ou = adcontainer.ADContainer.from_cn(user_data["department"].upper())
        except:
            msg = "An error occoured when getting the organizational unit from the Domain Controller."
            return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Unsuccessful", msg=msg)
        try:
            user = aduser.ADUser.create(user_settings["sAMAccountName"], ou, user_data["passw"])
            time.sleep(3.0)
            print("User:\t" + str(aduser.ADUser.from_cn(user_settings['sAMAccountName'])))
        except:
            print("Unable to get user from AD")
            msg = "An error occoured when creating the user account " + user_settings["sAMAccountName"] + "."
            return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Unsuccessful", msg=msg)
        win_user.update_attributes(user_settings['sAMAccountName'], user_settings, user_data['passw'])
        win_user.join_group(user_settings['sAMAccountName'])
        msg = user_data["fname"] + ", your user account: " + user_settings["sAMAccountName"] + " should be created. If not please contact the system administrator."
        pythoncom.CoUninitialize()
        return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Succes", msg=msg)
    else:
        return render_template("user_reg.html", active=1, head_menu=app.config["head_menu"], form=form)

