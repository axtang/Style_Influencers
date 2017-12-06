from models import Base, User, Influencers
from flask import Flask, jsonify, request, url_for, abort, g
from flask import render_template
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///styleInfluencers.db')

Base.metadata.bine = engine
DBSession = sessionmaker (bind = engine)
session = DBSession()

app = Flask(__name__)

# Add @auth.verify_password decorator here
@auth.verify_password
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

# Give a user with login credentials a token
@app.route('/token')
@app.login_required()
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify({'token': token.decode('ascii')})


@app.route('/users', methods = ['POST'])
def new_user():
	username = request.json.get('username')
	password = request.json.get('password')
	if username is None or password is None:
		print ("missing arguments")
		abort(400)
	return jsonify({'username': user.username})


@app.route('/resource')
@auth.login_required()
def get_resource():
	return josnify({'data':'Hello, %s!' % g.user.username})

# Home page
@app.route("/")
def hello():
	return render_template('index.html', name = string)

@app.route('/styles', methods = ['GET', 'POST'])
@auth.login_required()
def showAllInfluencers():
	if request.method == 'GET':
		influencers = session.query(Influencers).all()
		return josnify(influencers = [i.serialize for i in influencers])

	if request.methods == 'POST':
		name = request.json.get('name')
		description = request.json.get('description')
		blog_name = request.json.get('blog_name')
		newInfluencer = Influencers(name=name, blog=blog, picture=picture, description=description)
		session.add(newInfluencer)
		session.commit()
		return jsonify(newInfluencer.serialize)

@app.route('/influencers/<blog>')
@auth.login_required()
def showInfluencerBlog(blog):
	if blog == "":
		aBlog = session.query(Influencers).filter_by(blog_name).all()
		return jsonify(aBlog = [b.serialize for b in aBlog])

	if __name__ == '__main__':
		app.debug = True
		# app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x xrange(32))
		app.run(host='0.0.0.0', port = 5000)