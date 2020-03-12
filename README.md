# DATA Bachelor 244116
 This is the repository for the bachelor thesis on a Web-interface for Windows Active Directory. This project reqires that `python_ldap` ([See below!](#requirements)) and `flask_ldap` are installed.
----

## Requirements
 In order to install all the reqirements for this app it is recommended to run:
 `<drive_letter>:\<path_to_repo>\>pip install -r requirements.txt` or
 `<drive_letter>:\<path_to_repo>\>python -m pip install -r requirements.txt`

 Due to issues with installing `python_ldap` on Windows Server 2016 and 2019 with `pip`, I have provided setup wheel file that I found at [lfd.uci.edu](https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-ldap "Link to download page") in the `/_requirements/` folder which can be installed by running:
 `<drive_letter>:\<path_to_repo>\_requirements\>pip install python_ldap-3.2.0-cp37-cp37m-win_amd64.whl` or
 `<drive_letter>:\<path_to_repo>\_requirements\>python -m pip install python_ldap-3.2.0-cp37-cp37m-win_amd64.whl`

 Below is the Context Problem Solution steps used in development.
 * [Sever Configuration](#server-configuration)
 * [HTTPS](#https)
 * [User registration](#user-registration)
 * [User login](#user-login)
----

## Context Problem Solution

### Server Configuration

* Context: Error 500 when trying to connect to the webserver
* Problem: According to forums this is due to missing permissions for the IIS user account.
* Solution: Create new user account for IIS or user existing one to set the right permissions
* Context: Portnumbers for different services running on the server
* Problem: Portnumber 80, 443 and 3306 are blocked firewall or access control lists
* Solution: Have to contact Theodor Ivesdal about this at a later stage.

### HTTPS

* Context: HTTPS/SSL/TLS
* Problem: IIS Runs HTTP protocol by default
* Solution: For development, use a self-signed certificate and verify SSL/TLS operation in browser or run `<drive_letter:\<path_to_app>\>python ionracing.py` and use the following when calling the app: `app.run(host=\"0.0.0.0\", port=443, ssl_context=\"adhoc\")`

### User registration

* Context: User Registration does not function. (Running from IIS server)
* Problem: Exception is thrown when fetching Organizational Unit from AD
* Solution: Run the script in a subshell with command line arguments
    * Context: User registration does not fuction properly (Running in a subshell)
    * Problem: User is registered, but not with any attributes
    * Solution: Avoid exception from first implementation, by using adquery on the server
        * Context: User registration broken (Using adquery)
        * Problem: Exception is thrown when using the result of the query to get OU with the correct 'distinguishedName'
        * Solution: Optimize subshell implementation (maybe)
            * Context: User registration does not function properly (Running from IIS server)
            * Problem: User is registered, but not with any attibutes (only username and ou, no password)
            * Solution: ~Try different webserver i.e. apache or running (any advice???). May possibly run the user registration in a different server on a seperate process?~ Use a hybrid solution where user is created with the subshell command, and the rest is handeled by `win_user.update_attributes()` and `win_user.join_group()`.
                * Context: User is registred, but not with any attributes.
                * Problem: An `CoInitialize` not called exception is thrown
                * Solution: Import pythoncom and call `CoInitialize()`
                    * Context: User is registerd, but not with any attributes.
                    * Problem: Error 500 when creating user from app running in IIS
                    * Solution: Run in dev server, import pythoncom and call `CoInitialize()`

* Context: Duplicate usernames need to be circumvented.
* Problem: To user with the same username cannot co-exist
* Solution: Implement a new username policy and do checks for existing username i AD

### User login

* Context: Need user login for user management and report writing
* Problem: Find modules that can offer AD authentication.
* Solution: Use flask-ldap for authentication.
    * Context: Errors when installing flask-ldap
    * Problem: Something to do with a missing c++ header file
    * Solution: Get setup wheel (.whl) file which has the missing file.

* Context: User is logged in, but `flask_login` does not actually log the user in.
* Problem: The issues arise when either logging in the user, or the `user_loader` method is no working correctly.
* Solution: Fix the `user_loader` method to get the user object correctly.
