# pH Simulation tool

With this python (web) application it is possible to titrate any acid/base
mixture. A user can give several acid and base concentrations and volumes
into a _beaker_. Additionally ther can be added some water to dilute the
sample if needed. Then, the sample can be titrated with an acid/base of
choice (pKs, Conz., Vol.). As result, the titration curve is calculated and
displayed as bokeh plot. The user can choose if he want to overlay the plot 
or display a new figure. The figure can be saved as png file.

------------------------------------------------------------------------------------

## Disadvantages

It works but the fomatting of the input form is bad. The dilution during the
titration is not calculated, so the titration is in a constant volume mode what
is not perfect but the amount of used titrant untill equivalence is correct.
Also the formatting of static help.html file is not nice.

## Requirements

Install apache2, flask, flask-wtf and libapache-mod-wsgi-py3
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
    (sudo service apache2 restart)

The application has to be saved using following path:
    /var/www/application

and the user and group www-data has to have read and write acces!

In the app use a @route(/)

Open a browser and enter my.titration
-> finish

## Make public
To make it accesible for public, you not only have to a2ensite your page but also
a2dissite 000-default.conf file! to make it run just enter ip.
