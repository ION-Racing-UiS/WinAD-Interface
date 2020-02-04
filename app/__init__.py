from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pyad import pyad, aduser, adobject, adgroup, addomain, adcontainer, adcomputer, adquery, adsearch
import datetime
import sys
global limiter


app = Flask(__name__)
Bootstrap(app=app)
app.config.from_object(Config)
app.config["head_menu"] = ["Home", "User_reg", "Systems", "Terms", "Contact", "Login"]
limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute", "5 per second"],)
#app.config["adquery"] = adquery.ADQuery()
csrf = CSRFProtect(app)
csrf.init_app(app)
today = datetime.date.today()
month = ""
day = ""
year = str(today.year)[-2:]
if len(str(today.month)) < 2:
    month = "0" + str(today.month)
else:
    month = str(today.month)
if len(str(today.day)) < 2:
    day = "0" + str(today.day)
else:
    day = str(today.day)
log_name = "u_ex" + year + month + day+".txt"
print(log_name)
try:
    sys.stdout = open("../../logs/LogFiles/WCSVC1/"+log_name, 'a')
except:
    sys.stdout = open("../../logs/LogFiles/WCSVC1/"+log_name, 'w')
print("Starting flask server")




from app import routes