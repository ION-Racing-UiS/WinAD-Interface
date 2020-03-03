from flask import render_template, flash, redirect, url_for, request, g, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from app import app, limiter, login_manager
from app.forms import RegisterForm, LoginForm
from datetime import datetime
from app.pylib import win_user, StringTools
from app.pylib.auth_user import User
from pyad import pyad, adcontainer, aduser, adgroup, adobject
from flask_ldap import ldap
import os
import time
import pythoncom
import pywin32_system32
import re

@login_manager.user_loader
def load_user(id):
    pythoncom.CoInitialize()
    try: 
        get_val = User.get(id)
        return User.get(id)
    except:
        return None

@app.before_request
def get_current_user():
    g.user = current_user

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
    '''
    Route for user register page.
    '''
    '''Regular expressions to allow all latin characthers and remove two or more sequential spaces.'''
    text_regexp = '[^\u0041-\u005A\u0061-\u007A\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u024F\u1E00-\u1EFF ]'
    space_regexp = '\s{2,}'
    form = RegisterForm()
    if form.is_submitted() and form.validate() and form.submit.data:
        pythoncom.CoInitialize()
        fname = re.sub(space_regexp, "", re.sub(text_regexp, "", form.first_name.data))
        lname = re.sub(space_regexp, "", re.sub(text_regexp, "", form.last_name.data))
        if fname[-1] == " ": # Remove trailing spaces at the end
            fname = fname[0:-1]
        if lname[-1] == " ": # Remove trailing spaces at the end
            lname = lname[0:-1]
        user_data={
        "department": form.department.data,
        "role": form.role.data,
        "fname": fname,
        "lname": lname,
        "email": form.email.data,
        "passw": form.password.data
        }
        user_settings = win_user.create_user_settings(user_data)
        if not win_user.name_check(user_settings["sAMAccountName"]):
            msg = "Your username: " + user_settings["sAMAccountName"]  + " already exists in the Active Directory database. Please contact a system administrator."
            pythoncom.CoUninitialize()
            return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Unsuccessful", msg=msg)
        #os.system("python \"" + win_user.path + "\" \"" + user_data["fname"] + " " + user_data["lname"] + "\" \"" + user_data['passw'] + "\" \"" + user_data['department'] + "\" \"" + user_data['role'] + "\" \"" + user_data['email'] + "\"")
        #os.system("python \"" + win_user.path + "\" \"" + user_data["fname"] + " " + user_data["lname"] + "\" \"" + user_data["department"] + "\"")
        #win_user.create_user(user_settings, user_data["passw"])
        try:
            ou = adcontainer.ADContainer.from_cn(user_data["department"].upper())
        except:
            msg = "An error occoured when getting the organizational unit from the Domain Controller."
            pythoncom.CoUninitialize()            
            return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Unsuccessful", msg=msg)
        try:
            user = aduser.ADUser.create(user_settings["sAMAccountName"], ou, user_data["passw"])
            time.sleep(3.0)
            print("User:\t" + str(aduser.ADUser.from_cn(user_settings['sAMAccountName'])))
        except:
            print("Unable to get user from AD, user non existent.")
            msg = "An error occoured when creating the user account " + user_settings["sAMAccountName"] + ". If the problem persists, don't include your middle name. Max length is 20 characters including periods."
            pythoncom.CoUninitialize()
            return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Unsuccessful", msg=msg)
        win_user.update_attributes(user_settings['sAMAccountName'], user_settings, user_data['passw'])
        win_user.join_group(user_settings['sAMAccountName'])
        pythoncom.CoUninitialize()
        msg = user_data["fname"] + ", your user account: " + user_settings["sAMAccountName"] + " should be created. If not please contact the system administrator."
        return render_template("regRes.html", active=1, head_menu=app.config["head_menu"], title="Succes", msg=msg)
    else:
        return render_template("user_reg.html", active=1, head_menu=app.config["head_menu"], form=form)

@app.route("/systems")
def systems():
    return render_template("no.html", active=2, head_menu=app.config["head_menu"])

@app.route("/terms")
def terms():
    return render_template("no.html", active=3, head_menu=app.config["head_menu"])

@app.route("/contact")
def contact():
    return render_template("contact.html", active=4, head_menu=app.config["head_menu"], url=request.url)

@app.route("/contact/<hostname>")
def contacthost(hostname):
    content = render_template("comp_issue.html", hostname=hostname)
    return render_template("contact.html", active=4, head_menu=app.config["head_menu"], host=content)

@app.route("/contact/<form_type>", methods=["POST"])
def form_type(form_type):
    url = StringTools.removeBetween(request.url+str("/"), StringTools.secondLastIndexOf(request.url+str("/"), "/"), StringTools.lastIndexOf(request.url+str("/"), "/"))
    return render_template(form_type + ".html", url=url)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for("appuser.home"))
    form = LoginForm()
    pythoncom.CoInitialize()
    if request.method == "POST" and form.validate() and form.is_submitted():
        username = form.username.data
        password = form.password.data
        try: # Try to authenticate the user and handle exceptions if they occour
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS: # Invalid username or password
            flash("Invalid username or password", "danger")
            return render_template("login.html", active=5, head_menu=app.config["head_menu"], form=form)
        except ldap.INVALID_DN_SYNTAX or ldap.INVALID_SYNTAX: # Syntax error
            flash("Invalid syntax for login", "danger")
            return render_template("login.html", active=5, head_menu=app.config["head_menu"], form=form)
        except pyad.invalidResults: # Unable to get the user from ldap_server
            flash("Invalid username or password", "danger")
            return render_template("login.html", active=5, head_menu=app.config["head_menu"], form=form)
        user = User(username)
        login_user(user)
        flash("You have been logged in.", 'success')
        return redirect(url_for("appuser_home"))
    if form.errors:
        flash(form.errors, 'danger')
    return render_template("login.html", active=5, head_menu=app.config["head_menu"], form=form)

@app.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated:
        flash("You are now logged out.", 'success')
    logout_user()
    return redirect(url_for("login"))

@app.route("/appuser_home")
@login_required
def appuser_home():
    return render_template("appuser_home.html", user=current_user)

@app.route("/show/<template_file>")
def show_template(template_file):
    return render_template(str(template_file)+".html")
