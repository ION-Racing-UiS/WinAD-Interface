from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
global limiter


app = Flask(__name__)
app.config.from_object(Config)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["60 per minute", "5 per second"],)


csrf = CSRFProtect(app)




from app import routes