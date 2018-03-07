from . import *

# Home page
@app.route('/')
@app.route('/home')
def Home():
	styles = session.query(Styles).order_by(asc(Styles.type))
	influencers = session.query(Influencers).order_by(asc(Influencers.name))
	return render_template('index.html')