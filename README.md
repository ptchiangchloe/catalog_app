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

1. Install [vagrant virtual machine](https://github.com/udacity/fullstack-nanodegree-vm)

2. Download this project folder and place it in the virtual machine folder.

3. Run your local server in the vagrant folder
    ```vagrant up```

4. Log into your local server ```vagrant ssh```

5. Once you get into the local server
```cd /vagrant```

6. In the catalog project folder, ```sudo pip install wtforms```
7. Run ```python app.py```




## Built With

* [Python2.7](https://www.python.org/) - The language used
* [PostgreSQL](https://www.postgresql.org/) - Dependency Management
* [psycopg2](http://initd.org/psycopg/) - The PostgreSQL adapter for the Python programming language

## Authors

* **Hanyu Jiang** - *Initial work*
