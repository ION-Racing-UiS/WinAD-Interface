import pywin32_system32
import win32api
from pyad import pyad, aduser, adobject, adgroup, addomain, adcontainer, adcomputer, adquery, adsearch
from ionracing import __init__

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
        'cn': get_name(fname, lname),
        'department': dept,
        'displayName': get_name(fname, lname),
        'givenName': capitalize(fname),
        'homeDirectory': str(homeProfileDirectoryPrefix + sAMAccountName + homeDirectorySuffix),
        'homeDrive': homeDrive,
        'mail': email,
        'name': get_name(fname, lname),
        'physicalDeliveryOfficeName': physicalDeliveryOfficeName,
        'profilePath': str(homeProfileDirectoryPrefix + sAMAccountName),
        'sAMAccountName': sAMAccountName,
        'sn': lname,
        'userAccountControl': 66048,
        'userPrincipalName': userPrincipalName
    }

def create_user(user_settings, password, q):
    '''
    Create a Windows Active Directory user with data supplied from a dict and a password.

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
    ou = adcontainer.ADContainer.from_dn(q.get_single_result().get("distinguishedName"))
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
