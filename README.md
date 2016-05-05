## Trustwave Login Changer ##

### Summary ###
Change the login credentials for apps in Trustwave App Scanner Enterprise

### Requirements ###
* Python 2.7
* [requests](http://docs.python-requests.org/en/latest/user/install/#install)
* [docopt](http://docopt.org/)

### Usage ###
````
main.py testconnection                 # Test connection to Trustwave API
````
````
main.py newpassword <new-password>     # Set new password for all apps
````
````
main.py -h                             # Help menu
````

### Trustwave API Access ###
To use the Trustwave API, add your IP to the App Scanner API Clients list in both dev and prod.
In Trustwave, go to Administration > Server Settings > App Scanner API Clients and click the "Add New IP Restriction" button. Set your IP as both the start address and end address.

### Who do I talk to? ###

* Repo owner Andrew Roman <andreweroman@gmail.com>
* Repo contributor Rutvik Patel <rbpatel7@asu.edu>