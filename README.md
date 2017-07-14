# Catalog Project

This is a project is built to manage a sport related catalog with user authentication from the flask framework. This is a modern MVC type application.

Flask is a very light weight external framework that helps you to build a MVC
framework easily.

As for the form authentication, I use the WTForms for validation.


### Prerequisites

This project is only for local development, so you should have a local server service such as VirtualBox.

### Installing

Install the Virtual Machine steps:
[Link](https://classroom.udacity.com/nanodegrees/nd004/parts/8d3e23e1-9ab6-47eb-b4f3-d5dc7ef27bf0/modules/bc51d967-cb21-46f4-90ea-caf73439dc59/lessons/5475ecd6-cfdb-4418-85a2-f2583074c08d/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)

Install pip
```sudo apt-get install python-pip```

Place your project folder in VirtualBox/vagrant folder

Run your local server
```vagrant up```

Log into your local server

```vagrant ssh```

Once you get into the local server

```cd /vagrant```

Go to the project folder

Then install flask framework

```pip install flask```


## Built With

* [Python2.7](https://www.python.org/) - The language used
* [PostgreSQL](https://www.postgresql.org/) - Dependency Management
* [psycopg2](http://initd.org/psycopg/) - The PostgreSQL adapter for the Python programming language

## Authors

* **Hanyu Jiang** - *Initial work*
