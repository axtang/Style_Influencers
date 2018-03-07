from models import Base, User, Influencers, Styles
from Controllers import *
from functools import wraps
from flask import Flask, jsonify, request, url_for, abort, g, redirect, flash
from flask import Blueprints
from flask import render_template, abort

# For the anti-forgery state token
import random
import string
from flask import session as login_session

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, asc

from flask.ext.httpauth import HTTPBasicAuth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

APPLICATION_NAME = "Style-Influencers Application"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
	app.debug = True
	# app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x xrange(32))
	app.run(host='0.0.0.0', port=5000)
