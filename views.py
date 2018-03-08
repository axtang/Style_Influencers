
from flask import Flask
from Controllers import *

app = Flask(__name__)

APPLICATION_NAME = "Style-Influencers Application"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
	app.debug = True
	# app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x xrange(32))
	app.run(host='0.0.0.0', port=5000)
