# DATA Bachelor 244116
 This is the repository for the bachelor thesis on a Web-interface for Windows Active Directory.

 Below is the Context Problem Solution steps used in development.

# Context Problem Solution

# Server Configuration

* Context: Error 500 when trying to connect to the webserver
* Problem: According to forums this is due to missing permissions for the IIS user account.
* Solution: Create new user account for IIS or user existing one to set the right permissions

* Context: Portnumbers for different services running on the server
* Problem: Portnumber 80, 443 and 3306 are blocked firewall or access control lists
* Solution: Have to contact Theodor Ivesdal about this at a later stage.

# HTTPS

* Context: HTTPS/SSL/TLS
* Problem: IIS Runs HTTP protocol by default
* Solution: For development, use a self-signed certificate and verify SSL/TLS operation in browser.

# User registration

* Context: User Registration does not function. (Running from IIS server)
* Problem: Exception is thrown when fetching Organizational Unit from AD
* Solution: Run the script in a subshell with command line arguments
    * Context: User registration does not fuction properly (Running in a subshell)
    * Problem: User is registered, but not with any attributes
    * Solution: Avoid exception from first implementation, by using adquery on the server
        * Context: User registration broken (Using adquery)
        * Problem: Exception is thrown when using the result of the query to get OU with the correct 'distinguishedName'
        * Solution: Optimize subshell implementation run (maybe) run properly
            * Context: User registration does not function properly (Running from IIS server)
            * Problem: User is registered, but not with any attibutes
            * Solution: Try different webserver i.e. apache or running (any adice???). May possibly run the user registration in a different server on a seperate process?

