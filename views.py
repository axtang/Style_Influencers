from models import Base, User, Influencers, Styles
from functools import wraps
from flask import Flask, jsonify, request, url_for, abort, g, redirect, flash
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


# The following is for user creation, log-in, authentification
# and authorization processes.
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Style-Influencers Application"


# anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for x in range(32))login_session['state'] = state
    return render_template('login_template')


# Add @auth.verify_password decorator here
"""@auth.verify_password
def verify_password(username_or_token, password):
# Try to see if it's a username first
user_id = User.verify_auth_token
if user_id:
user = session.query(User).filter_by(id=user_id).one()
else:
user = session.query(User).filter_by(id=username_or_token).one()
# If user or password is not correct
if not user or not user.verify_password(password):
    return False
    """

# take in a google one-time use code
# exchange this auth-code for an access token
@app.route('/OAuth/<str:provider>', method=['POST'])
def gconnect():
    """ Handles the Google+ sign-in process on the server side.
    Server side function to handle the state-token and the one-time-code
    send from the client callback function following the seven steps of the
    Google+ sign-in flow. See the illustrated flow on
    https://developers.google.com/+/web/signin/server-side-flow.
    Returns:
        When the sign-in was successful, a html response is sent to the client
        signInCallback-function confirming the login. Otherwise, one of the
        following responses is returned:
        200 OK: The user is already connected.
        401 Unauthorized: There is either a mismatch between the sent and
            received state token, the received access token doesn't belong to
            the intended user or the received client id doesn't match the web
            apps client id.
        500 Internal server error: The access token inside the received
            credentials object is not a valid one.
    Raises:
        FlowExchangeError: The exchange of the one-time code for the
            credentials object failed.
    """
    # Confirm that the token the client sends to the server matches the
    # state token that the server sends to the client.
    # This roundship verification helps ensure that the user is making the
    # request and and not a maliciousscript.
    # Using the request.args.get-method, the code examines the state token
    # passed in and compares it to the state of the login session. If thesse
    # two do not match, a response message of an invalid state token is created
    # and returned to the client. No further authentication will occur on the
    # server side if there was a mismatch between these state token.
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # If the above statement is not true then I can proceed and collect the
    # one-time code from the server with the request.data-function.
    code = request.data

    # 5) The Server tries to exchange the one-time code for an access_token and
    # an id_token (credentials object).
    # 6) When successful, Google returns the credentials object. Then the
    # server is able to make its own API calls, which can be done while the
    # user is offline.
    try:
        # Create an oauth_flow object and add clients secret key information
        # to it.
        oauth_flow = flow_from_clientsecrets(
            'g_client_secrets.json', scope='')
        # Postmessage specifies that this is the one-time-code flow that my
        # server will be sending off.
        oauth_flow.redirect_uri = 'postmessage'
        # The exchange is initiated with the step2_exchange-function passing in
        # the one-time code as input.
        # The step2_exchange-function of the flow-class exchanges an
        # authorization (one-time) code for an credentials object.
        # If all goes well, the response from Google will be an object which
        # is stored under the name credentials.
        credentials = oauth_flow.step2_exchange(code)
    # If an error happens along the way, then this FlowExchangeError is thrown
    # and sends the response as an JSON-object.
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # After the credentials object has been received. It has to be checked if
    # there is a valid access token inside of it.
    access_token = credentials.access_token
    # If the token is appended to the following url, the Google API server can
    # verify that this is a valid token for use.
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    # Create a JSON get-request containing the url and access-token and store
    # the result of this request in a variable called result
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, send a 500 internal
    # server error is send to the client.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    # If the above if-statement isn't true then the access token is working.

    # Next, verify that the access token is used for the intended user.
    # Grab the id of the token in my credentials object and compare it to the
    # id returned by the google api server. If these two ids do not match, then
    # I do not have the correct token and should return an error.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Similary, if the client ids do not match, then my app is trying to use a
    # client_id that doesn't belong to it. So I shouldn't allow for this.
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if the user is already logged in
    # ! Credentials shouldn't been stored in the session
    # stored_credentials = login_session.get('credentials')
    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    # So assuming that none of these if-statements were true, I have a valid
    # access token and my user is successfully able to login to my server.
    # In this user's login_session, the credentials and the gplus_id are stored
    # to recall later (see check above).
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Use the google plus API to get some more information about the user.
    # Here, a message is send off to the google API server with the access
    # token requesting the user info allowed by the token scope and store it in
    # an object called data.
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    # Data should have all of the values listed on
    # https://developers.google.com/+/api/openidconnect/getOpenIdConnect#response
    # filled in, so long as the user specified them in their account. In the
    # following, the users name, picture and e-mail address are stored in the
    # login session.
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # If user doesn't exist, make a new one.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # 7) If the above worked, a html response is returned confirming the login
    # to the Client.
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '" style = "width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'])
    return output

# Create new user
def createNewUser(login_session):
	newUser = User(name=login_session['username'],
					email=login_session['email'],
					picture=login_session['picture'])
	session.add(newUser)
	session.commit()

	# users are identified by their email addresses
	user = session.query(User).filter_by(email=login_session['email']).one()

	return user.id

def getUserInfo(user_id):
	user = session.query(User).filter_by(id=user_id).one()
	return user

def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None


# Disconnect - revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
  access_token = login_session.get('access_token')
  if access_token is None:
    print('Access Token is None')
    response = make_response(json.dumps('Current user not connected'), 401)
    response.headers['Content-Type'] = 'application/json'
    return response
  print('In gdisconnect access token is %s', access_token)
  print('User name is: ')
  print(login_session['username'])
  url = 'https://accounts.google.com/o.oauth2/revoke?token=%s' % login_session['access_token']
  h = httplib2.http()
  result = h.request(url, 'GET')[0]
  print('result is ')
  print(result)
  if result['status'] == '200':
    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    response = make_response(json.dumps('Successfully disconnected.'), 200)
    response.headers['Content-Type'] = 'application/json'
    return response
  else:
    response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
    response.headers['Content-Type'] = 'application/json'
    return response


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
