# about apache
Install apache and libapache-mod-wsgi-py3
create a xy.wsgi file which calls the controller.py modul and loads the app
from it. 
Go to /etc/apache2/sites-availabel and create a virtual host described below:
    <virtualhost *:80> 
        ServerName my.titration

        WSGIDaemonProcess controller user=www-data group=www-data threads=5 home=/var/www/pHsim/
        WSGIScriptAlias / /var/www/pHsim/pH_sim.wsgi

        <directory /var/www/pHsim> 
            WSGIProcessGroup controller 
            WSGIApplicationGroup %{GLOBAL}
            WSGIScriptReloading On
            Order deny,allow 
            Require all granted
        </directory>
    </virtualhost> 

Then open /etc/hosts and add:
    127.0.0.1 my.titration

Then reload apache service and make site accessible
    sudo a2ensite my.titration
    sudo service apache2 reload
    sudo service apache2 restart

The application has to be saved using following path:
    /var/www/application

and the user and group www-data has to have read and write acces!

In the app use a @route(/)

Open a browser and enter my.titration
-> finish

## Make public
To make it accesible for public, you dont have to a2ensite youre page but also
a2dissite 000-default.conf file! to make it run just enter ip.
