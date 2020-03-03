import ldap
from app.pylib import win_user
from flask_wtf import Form
from flask_login import UserMixin
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
from pyad import pyad, aduser, adgroup, addomain, adcomputer, adcontainer, adsearch, adquery
import pythoncom

def get_ldap_connection():
    conn = ldap.initialize("ldap://" + win_user.ldap_server + ":389/")
    return conn

class User(UserMixin):
    def __init__(self, username):
        u = aduser.ADUser.from_cn(username)
        self.guid = u.get_attribute('objectGUID')[0].tobytes().hex()
        self.username = u.get_attribute('cn')[0]

    def __repr___(self):
        return '<User %s>' % self.username
    
    @staticmethod
    def try_login(username, password):
        '''
        Attemps to authenticate the user with the ldap/active directory server.\n
        Arguments:\n
        :param username: Username for the user <type:str>\n
        :param password: Password for the user <type:str>
        '''
        pyad.set_defaults(ldap_server=win_user.ldap_server, username=win_user.username, password=win_user.password)
        dn = aduser.ADUser.from_cn(username).dn
        conn = get_ldap_connection()
        conn.simple_bind_s(
            dn,
            password
        )
    
    def get_id(self):
        return str(self.guid)

    def get(id):
        '''
        Return a user by username\n
        Arguments:\n
        :param id: Username of the user <type:str>
        '''
        return User(username=id)