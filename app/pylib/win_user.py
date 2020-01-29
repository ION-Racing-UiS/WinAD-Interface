import pywin32_system32
import win32api
from pyad import pyad, aduser, adobject, adgroup, addomain, adcontainer, adcomputer, adquery, adsearch
import os
import re
from pathlib import Path

ldap_server = "<server_fqdn>" # Fully qualified domain name of the ldap server
username = "<accountop_username>" # Account operations account
password = "<accountop_password>" # Password for the account above
topLevelDomain = "<yourdomain.suffix>" # Top level domain name
homeDrive = "<drive_letter>:" # User home drive letter
homeProfileDirectoryPrefix = "<unc_path_to_profile_share>" # UNC Share path for profiles
homeDirectorySuffix = ".V6" # Suffix to access the profile directory from homeDrive
scriptPath = "<script_name>" # path to script in \\<servername>\sysvol\<topLevelDomain>\scripts
physicalDeliveryOfficeName = "<office_name>" # Office name
company = "<your_companyname>" # Official Company name
userdomain = "<yourdomain>" # Just your domain name, ie. google, not google.com
domainsuffix = "<suffix>" # What top level domain you have, ie. .com, .net, .eu, dk, .no, .se
ous = [('<ou_name>', '<Ou_name>'), ('<ou_name2>', '<Ou_name2>')] # Organizational units list for the wtf form <type:list> of <type:tuple> or <type:str> and <type:str>
path = str(Path(__file__).absolute()) # Absolute path to this file within the filesystem.
local_admins = "<group_name>" # Group name for users so that they can be local admins

def create_user_settings(user_input):
    '''
    Returns a dict with the correct user settings for the domain\n
    Arguments:\n
    :param user_input: dict with the user data for user registration <type:dict>\n
    :keys    \"fname\", \"lname\", \"email\", \"passw\", \"department\", \"role\": <types:str>\n
    :values first name, last name, email, password, department, role <types:str>
    '''
    fname = user_input["fname"]
    lname = user_input["lname"]
    email = user_input["email"]
    passw = user_input["passw"]
    dept = user_input["department"]
    role = user_input["role"]
    sAMAccountName = get_username(fname, lname)
    userPrincipalName = get_userPrincipalName(sAMAccountName)
    return {
        'department': dept,
        'description': role,
        'displayName': get_name(fname, lname),
        'givenName': capitalize(fname),
        'homeDirectory': str(homeProfileDirectoryPrefix + sAMAccountName + homeDirectorySuffix),
        'homeDrive': homeDrive,
        'mail': email,
        'physicalDeliveryOfficeName': physicalDeliveryOfficeName,
        'profilePath': str(homeProfileDirectoryPrefix + sAMAccountName),
        'sn': lname,
        'scriptPath': scriptPath,
        'userPrincipalName': userPrincipalName,
        'sAMAccountName': sAMAccountName,
    } # 'cn' and 'name' keys have been removed as they cause exceptions when being updated.

def create_user(user_settings, password, q):
    '''
    Create a Windows Active Directory user with data supplied from a dict and password, q is the adquery object.\n
    Arguments:\n
    :param user_settings: User settings created by create_user_setting(user_data) <type:dict>\n
    :param password: Password for the user to be registerd <type:str>\n
    :param q: ADQuery object to be used for ad queries, add.config[\"adquery\"] <type:pyad.adquery.ADQuery>
    '''
    #ou_arg = str("OU=" + user_settings["department"] + ",DC=" + userdomain + ",DC=" + domainsuffix)
    dept = user_settings["department"].upper()
    #q = adquery.ADQuery()
    q.execute_query(
        attributes=["distinguishedName", "ou", "cn"], 
        where_clause="ou = '{}'".format(dept),
        base_dn=""
        )
    #ou_arg = q.get_single_result().get("distinguishedName")
    pyad.set_defaults(ldap_server=ldap_server, username=username, password=password)
    ou = adcontainer.ADContainer.from_cn(q.get_single_result().get("cn"))
    name = user_settings["name"]
    user = aduser.ADUser.create(
        name=name,
        container_object=ou,
        password=password,
        optional_attributes=user_settings
    )
    return user
    
def get_username(first_name, last_name):
    '''
    Get username for a user based on first and last name\n
    get_username(\"Neil\", \"Peart\")
    returns n.peart\n
    Arguments:\n
    :param first_name: first name of the user <type:str>\n
    :param last_name:  last name of the user  <type:str>
    '''
    return str(first_name[0].lower() + "." + last_name.lower())

def get_userPrincipalName(username, topLevelDomain=topLevelDomain):
    '''
    Get userPrincipalName for a user based on username and domain.
    get_userPrincipalName(\"g.lee\", \"rush.com\") 
    returns g.lee@rush.com\n
    Arguments:\n
    :param username: username of the user <type:str>\n
    :param topLevelDomain:   domain of the user   <type:str>
    '''
    return str(username + "@" + topLevelDomain)

def capitalize(string):
    '''
    Capitalize first letter of any input string.\n
    capitalize(\"alex\") returns \"Alex\"
    capitalize(\"Alex\") returns \"Alex\"\n
    Arguments:\n
    :param string: string to capitalize <type:str>
    '''
    return str(string[0].upper() + string[1:])

def get_name(first_name, last_name):
    '''
    Assemble and capitalize first and last names into a full name/common name.\n
    get_name(\"geddy\", \"lee\") returns \"Geddy Lee\"
    Arguments:\n
    :param first_name: first name <type:str>
    :param last_name:  last name  <type:str>
    '''
    return str(capitalize(first_name) + " " + capitalize(last_name))

def get_last_index_of(string, charachter=" "):
    '''
    Returns the last index of a specific charachter by looping backwards through a string.\n
    Arguments:\n
    :param string: string that you want to find the index in <type:str>\n
    :param charachter: the charachter you you want to find the last index of <type:chr|str>

    '''
    for i in range(len(string)-1, 0, -1):
        if string[i] == " ":
            return i
    else:
        return None

def split_name(name, index):
    '''
    Returns a tupple of two strings by splitting the string at a given index.
    I.e split_name(\"Alex Lifeson\", 4) will return (\"Alex\", \"Lifeson\")\n
    Arguments:\n
    :param name: Name or string to split at the given index <type:str>\n
    :param index: Index of where to split <name> at <type:int>
    '''
    return name[:index], name[index + 1:]
    

if __name__=="__main__":
    if len(os.sys.argv) == 6:
        pyad.set_defaults(ldap_server=ldap_server, username=username, password=password)
        user_data = {
            'name': os.sys.argv[1],
            'passw': os.sys.argv[2],
            'department': os.sys.argv[3],
            'role': os.sys.argv[4],
            'email': os.sys.argv[5]
        }
        print(user_data['name'])
        user_data['fname'], user_data['lname'] = split_name(user_data['name'], get_last_index_of(user_data['name'], charachter=" "))
        user_settings = create_user_settings(user_data)
        sAMAccountName = get_username(user_data['fname'], user_data['lname'])
        ou = adcontainer.ADContainer.from_dn(str("OU=" + user_data["department"].upper() + ", DC=" + userdomain.upper() + ", DC=" + domainsuffix.upper()))
        print(str(ou))
        user = aduser.ADUser.create(sAMAccountName, ou, user_data["passw"])
        user = aduser.ADUser.from_cn(sAMAccountName)
        group = adgroup.ADGroup.from_cn(local_admins)
        group.add_members([user])
        print(str(user))
        user.set_user_account_control_setting("DONT_EXPIRE_PASSWD", True)
        for key in user_settings.keys():
            print(str(key))
            user.update_attribute(str(key), str(user_settings[key]))
        print(str(user_data))
        print(str(user_settings))
    else:
        print("Usage: win_user.py \"First_name Last_name\" \"Password\" \"Department\" \"Role\" \"Mail\"")

