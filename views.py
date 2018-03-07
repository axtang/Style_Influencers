from models import Base, User, Influencers, Styles
from functools import wraps
from flask import Flask, jsonify, request, url_for, abort, g, redirect, flash
from flask import Blueprints
from flask import render_template

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


# connect to database and create database session
engine = create_engine('sqlite:///styleInfluencers.db')
Base.metadata.bine = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


APPLICATION_NAME = "Style-Influencers Application"

# Home page
@app.route('/')
@app.route('/home')
def Home():
	styles = session.query(Styles).order_by(asc(Styles.type))
	influencers = session.query(Influencers).order_by(asc(Influencers.name))
	return render_template('index.html')

# Display all styles
@app.route('/styles', methods=['GET', 'POST'])
def showStyles(type):
	allStyles = session.query(Styles).order_by(asc(Styles.type)).all()
    oneStyle = session.query(Styles).filter_by(asc(allStyles_type)).one()
    print (style, influencers)
	creator = getUserID(type.user_id)
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicStyles.html',
								oneStyle=style.type,
								allStyles=styles,
								influencers=influencers
								)
	else:
		user = getUserInfo(login_session['user_id'])
		return render_template('styles.html',
								allStyles=styles,
								oneStyle=style.type,
								influencers=influencers)


# Display all influencers
@app.route('/influencers', methods=['GET', 'POST'])
def showInfluencers(blogName):
    influencers = session.query(Influencers).order_by(asc(Influencers.blogName)).all()
    influencer = session.query(Influencers).filter_by(asc(influencers_blogName)).one()
    print(influencers)
    creator = getUserID(type.user_id)
    if 'username' not in login_session or creator.id != login_session['user.id']:
        return render_template('publicInfluencers.html'
                                influencer=influencer.blogName,
                                influencers=influencers)
    else:
        return render_template('influencers.html',
                                influencer=influencer.blogName,
                                influencers=influencers)


# Display a specfic influencer based on a specific style
@app.route('/<string:styles_type>/<string:influencers_name>', methods=['GET', 'POST'])
def showStyleInfluencer(styles_type, influencers_name):
	styles = session.query(Styles).order_by(asc(Styles.type))
	style = session.query(Styles).filter_by(styles_type).one()
	influencer = session.query(Influencers).filter_by(Style=style).order_by(asc(name=influencers_name)).one()
    print(style, influencer)

	creator = getUserInfo(influencer.user_id)
	if 'username' not in login_session or creator.id != login_sessin['user_id']:
		return render_template('publicInfluencers.html',
								styles=styles.type,
								influencer=influencers.name)
	else:
		return render_template('influencers.html',
								styles=styles.type,
								influencer=influencers.name)


# Delete an influencer
@app.route('/influencers/<string:influencer_name>/delete', method=['GET', 'POST'])
@login_required
def deleteInfluencer(influencers_id, influencers_name):
    influencers = session.query(Influencers).filter_by(id=influencers_id).one()
    deletingInfluencer = session.query(Influencers).filter_by(name=influencers_name).one()
    creator = getUserInfo(deletingInfluencer.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You cannot delete this influencer. This influencer belongs to a different user.")
        return redirect(url_for('index.html'))
    if request.method == 'POST':
        session.delete(deletingInfluencer)
        session.commit()
        flash("You have successfully deleteed %s!" % deletingInfluencer_name)
        return redirect(url_for('index.html',
                                influencers_name=influencer.name))
    else:
        return redner_template('deleteInfluencer.html', influencer=deletingInfluencer)


# Influencers json file
@app.route('/styleInfluencers/influencers/JSON')
@login_required
def influencersJSON():
	infuencers = session.query(Influencers).all()
	return jsonify(influencers=[i.serialize for i in influencers])


# Style type json file
@app.route('/styleInfluencers/<string:styles_type>/influencers/JSON')
@login_required
def stylesInfluencersJSON(styles_type):
	style = session.query(Type).filter_by(type=styles_type).one()
	influencers = session.query(Influencers).filter_by(styles=styles).all()
	return jsonify(influencers=[i.serialize for i in influencers])


# Influencer based on style type json file
@app.route('/styleInfluencers/<string:styles_type>/<string:influencer_name>/JSON')
@login_required
def influencerStylesJSON():
	styles = session.query(Styles).filter_by(type=styles_type).one()
	influencer = session.query(Influencers).filter_by(blog_name=influencer_blogName, type=styles_type).one()
	return jsonify(influencers=[influencers.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
	app.debug = True
	# app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x xrange(32))
	app.run(host='0.0.0.0', port=5000)
