from flask import render_template, flash, redirect, url_for, request
from werkzeug.utils import secure_filename
from app import app, limiter
from app.forms import *
from datetime import datetime
import os

@app.route("/")
def landing():
    return render_template("landing.html")