import pywin32_system32
import win32api
from pyad import pyad, aduser, adobject, adgroup, addomain, adcontainer, adcomputer, adquery, adsearch

ldap_server = "<server_fqdn>"
username = "<accountop_username>"
password = "<accountop_password>"

domain = "<yourdomain.locality>"
homeDrive = "<drive_letter>:"
homeProfileDirectoryPrefix = "<unc_path_to_profile_share>"
homeDirectorySuffix = ".V6"
scriptPath = "<script_name>"
physicalDeliveryOfficeName = "<office_no>"
company = "<your_companyname>"

def create_user_settings(user_input):
    '''
    Returns a dict with the correct user setting for the domain\n
    
    Arguments:
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
        'homeDirectory': str(homeProfileDirectoryPrefix + sAMAccountName + homeDirectorySuffix)
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

def get_userPrincipalName(username, domain=domain):
    '''
    Get userPrincipalName for a user based on username and domain.
    get_userPrincipalName(\"g.lee\", \"rush.com\") 
    returns g.lee@rush.com\n

    Arguments:\n
    :param username: username of the user <type:str>\n
    :param domain:   domain of the user   <type:str>
    '''
    return str(username + "@" + domain)

def capitalize(string):
    '''
    Capitalize first letter of any input string.\n
    capitalize(\"alex\") returns \"Alex\"
    capitalize(\"Alex\") returns \"Alex\"\n
    :param string: string to capitalize <type:str>
    '''
    return str(string[0].upper() + string[1:])

def get_name(first_name, last_name):
    '''
    Assemble and capitalize first and last names into a full name/common name.\n
    get_name(\"Geddy\", \"Lee\") returns \"Geddy Lee\"
    :param first_name: first name <type:str>
    :param last_name:  last name  <type:str>
    '''
    return str(capitalize(first_name) + " " + capitalize(last_name))

def create_user(user_data):
    '''
    Create a Windows Active Directory user with data supplied from a dict.

    '''