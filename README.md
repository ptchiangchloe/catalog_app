# Catalog Web Application Project

This is a project is built to manage a sport related catalog with user authentication from the flask framework. This is a modern MVC type application.

Flask is a very light weight external framework that helps you to build a MVC
framework easily.

As for the form authentication, I use the WTForms for validation.

In the production version, I use LAPP(Linux/Apache2/PostgreSQL/Python).
You can see the live version in http://52.36.14.158/

## URLS:

Home page - root/

Register page - root/register

Login page - root/login

Dashboard page- root/dashboard

Category items page- root/catalog/&lt;category&gt;/items

Single item page with description - root/catalog/&lt;item_id&gt;

Edit item page - root/catalog/edit_item/&lt;item_id&gt;

Delete item page - root/catalog/delete_item/&lt;item_id&gt;


## Built With softwares:

* [Python2.7](https://www.python.org) - The language used.
* [Flask](http://flask.pocoo.org) - A Python microframework based on Werkzeug, Jinja 2 and good intentions.
* [PostgreSQL](https://www.postgresql.org) - Open source object-relational database system.
* [psycopg2](http://initd.org/psycopg) - The PostgreSQL adapter for the Python programming language.
* [Git](https://git-scm.com)- Free and open source distributed version control system.
* [Github](https://git-scm.com) - A web-based version control repository.Lightsail
* [Lightsail](https://amazonlightsail.com) - Simple Virtual Private Servers on AWS.
* [Apache2](https://httpd.apache.org) - Most commonly used Web server on Linux systems.

## Development

### Prerequisites

This project is only for local development, so you should have a local server service such as VirtualBox.

### Installing

Install the Virtual Machine steps:
[Link](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

1. Install [vagrant virtual machine](https://github.com/udacity/fullstack-nanodegree-vm)

2. Download this project folder and place it in the virtual machine folder.

3. Run your local server in the vagrant folder
    ```
    vagrant up
    ```

4. Log into your local server
```
vagrant ssh
```

5. Once you get into the local server
```
cd /vagrant
```

6. In the catalog project folder,
```
sudo pip install wtforms
```
7. Run
```
python app.py
```

### Install PostgreSQL

in your local server(vagrant/virtualBox has intalled PostgreSQL.)

### Create Database
Connect psql command

1. Run
```
CREATE DATABASE myflaskapp
```

2.

```
\connect myflaskapp
```
   Create database tables in myflaskapp database(You need to use psql to connect the database.):

Create users table:
```
    CREATE TABLE users (
    id SERIAL PRIMARY KEY NOT NULL,
    name character varying(100),
    email character varying(100),
    username character varying(30),
    password character varying(100),
    register_date timestamp without time zone DEFAULT timezone('utc'::text, now())
);
```

Create items table:


```
CREATE TABLE items (
    id SERIAL PRIMARY KEY NOT NULL,
    title character varying(100),
    category character varying(100),
    description text,
    create_date timestamp without time zone DEFAULT timezone('utc'::text, now())
);
```

Create gplus user table:
```
CREATE TABLE gplus_user (
    name character(250) NOT NULL,
    email character(250) NOT NULL,
    picture character(250),
    id SERIAL PRIMARY KEY NOT NULL
);
```



## Linux Configuration
##### Create and configure the linux machine with Ubuntu distribution system.

  1. Update all currently installed packages.

  ```
  sudo apt-get update
  sudo apt-get upgrade
  ```
  2.  

  ```
  sudo nano /etc/ssh/sshd_config
  ```
  and then change ```Port 22``` to ```Port 2200``` , then save & quit.

  3. Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), HTTP (port 80), and NTP (port 123).

  ```
  sudo ufw allow 2200/tcp
  sudo ufw allow 80/tcp
  sudo ufw allow 123/udp
  sudo ufw enable
  ```
  4. Configure the local timezone to UTC
  ```sudo dpkg-reconfigure tzdata```


##### Install and secure Apache2 server with its Python mod_wsgi application handler to host the catalog app.

  1. Install Apache
  ```
  sudo apt-get install apache2
  ```
  2. Install mod_wsgi
  ```
  sudo apt-get install python-setuptools libapache2-mod-wsgi
  ```
  3. Restart Apache
  ```
  sudo service apache2 restart
  ```
##### Install and secure the PostgreSQL, create myflaskapp database to store application information in a scalable way.

  1. Install PostgreSQL
  ```
  sudo apt-get install postgresql
  ```
  2. Make sure there is no remote connection allowed

  ```
  sudo nano /etc/postgresql/9.5/main/pg_hba.conf
  ```

  3. Login in as user 'postgres'

    ```
    sudo su - postgres
    ```
  4. Get into postgreSQL shell

  ```
  psql
  ```

  5. Create a new database named catalog and create a new user named catalog in postgreSQL shell

  ```
  postgres=# CREATE DATABASE catalog;
  postgres=# CREATE USER catalog;

  ```

  6. Give new user 'catalog' limited permissions to catalog application database.

  ```
  ALTER ROLE catalog WITH Create DB;
  ```

  7. Quit postgreSQL
  ```
  postgres=# \q
  ```

  8. Exit from user "postgres"

  exit

##### Deploy and secure the catalog app in the Linux server.

  1. Install Git
  ```
  sudo apt-get install git
  ```

  2. clone 'catalog_app' to '/var/www/' directory from the master branch from Github repository.

  ```
  git clone https://github.com/ptchiangchloe/catalog_app.git
  ```

  3. Install following packages in order to run the app:

  ```(Since flask is a very light weight framework, so you need to install a lot of library manually)```

  ```
  sudo apt-get install python-pip
  ```

  ```
  sudo pip install flask
  ```

  ```
  sudo pip install wtforms
  ```

  ```
  sudo pip install passlib
  ```

  ```
  sudo pip install psycopg2
  ```

  ```
  sudo pip install bleach
  ```

  ```
  sudo pip install oauth2client
  ```

  ```
  sudo pip install requests
  ```

  4. Configure Python mod_wsgi application handler:

  ```
  sudo nano /etc/apache2/sites-enabled/000-default.conf
  ```

  ```
    <VirtualHost *:80>
        ServerAdmin ptchiang12@gmail.com
        DocumentRoot /var/www/catalog_app

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /var/www/catalog_app>
        WSGIProcessGroup catalog_app
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
        </Directory>
        <Directory /var/www/catalog_app/static/>
            Order allow,deny
            Allow from all
        </Directory>
        WSGIDaemonProcess catalog_app user=www-data group=www-data  threads=5
        WSGIScriptAlias / /var/www/catalog_app/catalog.wsgi
  </VirtualHost>

  ```
  5. Enable the virtual host:

   ```
   sudo a2ensite catalog_app
   ```

  6. Create the catalog.wsgi file in catalog_app directory :

  ```
  #! /usr/bin/python
  import sys
  import logging
  logging.basicConfig(stream=sys.stderr)
  sys.path.insert(0,"/var/www/catalog_app/")

  # home points to the home.py file
  from app import app as application
  application.secret_key = "somesecretsessionkey"
  ```

  7. Restart the Apache2 server
  ```
  sudo /etc/init.d/apache2 restart
  ```

## Third-party resources
[Install Apache and PostgreSQL for web server application](https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379/modules/357367901175461/lessons/4340119836/concepts/48159388430923
)

[Test the configuration](https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379/modules/357367901175461/lessons/4340119836/concepts/48018692630923
)

[Configure PostgreSQL](https://classroom.udacity.com/nanodegrees/nd004/parts/ab002e9a-b26c-43a4-8460-dc4c4b11c379/modules/357367901175461/lessons/4340119836/concepts/48018692630923
)

[Mod_wsgi for flask](http://flask.pocoo.org/docs/0.12/deploying/mod_wsgi/
)


## Authors

* **Hanyu Jiang** - *Initial work*

## Mentors

* **Steve Wooding** - *Udacity online mentor*
* **Harry Staley** - *Udacity online mentor*
* **Greg Berger** - *Udacity online mentor*
