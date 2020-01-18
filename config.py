import os

class Config(object):
    SECRET_KEY = "dev" or os.urandom(24).hex()
    