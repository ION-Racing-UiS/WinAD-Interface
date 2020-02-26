import ldap
import win_user
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from pyad import pyad, aduser, adgroup, addomain, adcomputer, adcontainer, adsearch, adquery
import pythoncom

def get_ldap_connection():
    conn = ldap.initialize("ldap://" + win_user.ldap_server + ":389/")
    return conn

class User():
    username = str

    def __init__(self, username, password):
        self.username = username
    
    @staticmethod
    def try_login(username, password):
        pyad.set_defaults(ldap_server=win_user.ldap_server, username=win_user.username, password=win_user.password)
        pythoncom.CoInitialize()
        dn = aduser.ADUser.from_cn(username).dn
        pythoncom.CoUninitialize()
        conn = get_ldap_connection()
        conn.simple_bind_s(
            dn,
            password
        )
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.username)