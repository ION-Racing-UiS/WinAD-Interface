from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pyad import pyad, aduser, adobject, adgroup, addomain, adcontainer, adcomputer, adquery, adsearch
global limiter


app = Flask(__name__)
Bootstrap(app=app)
app.config.from_object(Config)
app.config["head_menu"] = ["Home", "User_reg", "Systems", "Terms", "Contact", "Login"]
limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute", "5 per second"],)
app.config["adquery"] = adquery.ADQuery()


csrf = CSRFProtect(app)




from app import routes