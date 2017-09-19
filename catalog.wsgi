#! /usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog_app/")

# home points to the home.py file
from app import app as application
application.secret_key = "somesecretsessionkey"
