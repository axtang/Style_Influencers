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


# anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))login_session['state'] = state
    return render_template('login_template')


# take in a google one-time use code
# exchange this auth-code for an access token


# Add Flask login_decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


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


# Add a style
@app.route('/styles/new', methods=['GET', 'POST'])
@login_required
def newStyle():
	if request.method == 'POST':
		newStyle = Styles(
			type = request.form['type'],
			user_id = login_session['user_id'])
		print(newStyle)
		session.add(newStyle)
		flash('You have successfully added %s as a new style!' % newStyle.type)
        session.commit()
		return redirect(url_for('index.html'))
	else:
		return render_template('newStyle.html')


# Edit a style
@app.route('/styles/<string:styles_type>/edit', method=['GET', 'POST'])
@login_required
def editStyle(styles_type):
	editStyle = session.query(Styles).filter_by(type=styles_type).one()
	creator = getUserInfo(editStyle.user_id)
	user = getUserInfo(login_session['user_id'])

	# if the style was not associated with the user
	if creator.id != login_session['user_id']:
		flash("Sorry, you cannot edit this style.")
		return redirect(url_for('index.html'))
	else:
		# edit the style
		if request.method == 'POST':
			if request.form['type']:
				editStyle.type = request.form['type']
			session.add(editStyle)
			session.commit()
			flash('You have successfully edited a style!')
			return redirect(url_for('index.html'))
		else:
			return render_template('editStyle.html',
									styles=editStyle,
									style=style)


# Delete a style type
@app.route('/styles/<string:styles_type>/delete', method=['GET', 'POST'])
@login_required
def deleteStyle(styles_id, styles_type):
	styles = session.query(Styles).filter_by(id=styles_id).one()
	deletingStyle = session.query(Styles).filter_by(type=styles_type).one()
	creator = getUserInfo(deletingStyle.user_id)
	user = getUserInfo(login_session['user_id'])
	if creator.id != login_session['user_id']:
		flash("You cannot delete this style. This Style belongs to a different user.")
		return redirect(url_for('index.html'))
	if request.method == 'POST':
		session.delete(deletingStyle)
		session.commit()
		flash("You have successfully deleted %s!" % deletingStyle_type)
		return redirect(url_for('index.html',
								styles_type=styles.type))
	else:
		return render_template('deleteStyle.html',
								style=deletingStyle)


# Add a new influencer
@app.route('/influencers/new', methods=['GET', 'POST'])
@login_required
def newInfluencer(influencer_id):
    if request.method == ['POST']:
        newInfluencer= Influencer(
            name = request.form['name'],
            country = request.form['country'],
            blogName = request.form['blogName'],
            description = request.form['description'],
            picture = requet.form['picture'])
        print (newInfluencer)
        session.add(newInfluencer)
        flash('You have sucessfully added %s as a new influencer!' % newInfluencer.name)
        session.commit()
        return redirect(url_for('index.html'))
    else:
        return render_template('newInfluencer.html')


# Edit an influencer
@app.route('/influencers/<string:influencers_name>/edit', method=['GET'], ['POST'])
@login_required
def editInfluencers(influencers_name):
    editInfluencer = session.query(Influencers).filter_by(name=influencer_name).one()
    creator = getUserinfo(editInfluencer.user_id)
    user = getUserInfo(login_session['user_id'])

    # if the influencer was not associated with the user
    if creator.id != login_session['user_id']:
        flash("Sorry, you cannot eit this influencer.")
        return redirect(url_for('index.html'))
    else:
        # edit the influencer
        if request.method == 'POST':
            if request.form['name']:
                editInfluencer.name = request.form['name']
            session.add(editInfluencer)
            session.commit()
            flash('You have successfully edited an influencer!')
            return redirect(url_for('index.html'))
        else:
            return render_template('editInfluencer.html',
                                    influencers=editInfluecers,
                                    influencer=influencer)


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


# Styles and influencers json file
@app.route('/styleInfluencers/JSON')
@login_required
def allStyleInfluencersJSON():
	styles = session.query(Styles).all()
	styles_dict = [s.serializes for s in styles]
	for s in range(len(styles_dict)):
		categories = [c.serialize for c in session.query(Type).filter_by(styles_id=styles_dict[c]["id"]).all()]

		if categories:
			styles_dict[c]["type"] = categories


# Styles json file
@app.route('/styleInfluencers/styles/JSON')
@login_required
def stylesJSON():
	styles = session.query(Styles).all()
	styles_dict = [s.serialize for s in styles]
	for s in range(len(styles_dict)):
		type = [i.serialize for i in session.query(Type).filter_by(styles_id=styles_dict[s]["id"]).all()]
		if type: 
			type_dict[c]["type"] = type
	return jsonify(Styles=styles_dict)


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
